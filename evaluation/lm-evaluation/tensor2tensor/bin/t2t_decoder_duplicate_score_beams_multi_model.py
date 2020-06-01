# coding=utf-8
# Copyright 2019 The Tensor2Tensor Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

r"""Decode from trained T2T models.

This binary performs inference using the Estimator API.

Example usage to decode from dataset:

  t2t-decoder \
      --data_dir ~/data \
      --problem=algorithmic_identity_binary40 \
      --model=transformer
      --hparams_set=transformer_base

Set FLAGS.decode_interactive or FLAGS.decode_from_file for alternative decode
sources.
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
from tensor2tensor.bin import t2t_trainer
from tensor2tensor.data_generators import problem  # pylint: disable=unused-import
from tensor2tensor.data_generators import text_encoder
from tensor2tensor.utils import decoding
from tensor2tensor.utils import registry
from tensor2tensor.utils import trainer_lib
from tensor2tensor.utils import usr_dir

import itertools
import operator

import tensorflow as tf

flags = tf.flags
FLAGS = flags.FLAGS

# Additional flags in bin/t2t_trainer.py and utils/flags.py
flags.DEFINE_string("checkpoint_path", None,
                    "Path to the model checkpoint. Overrides output_dir.")
flags.DEFINE_bool("keep_timestamp", False,
                  "Set the mtime of the decoded file to the "
                  "checkpoint_path+'.index' mtime.")
flags.DEFINE_bool("decode_interactive", False,
                  "Interactive local inference mode.")
flags.DEFINE_integer("decode_shards", 1, "Number of decoding replicas.")
flags.DEFINE_string("score_file", "", "File to score. Each line in the file "  # ALES
                                      "must be in the format input \t target.")
flags.DEFINE_bool("decode_in_memory", False, "Decode in memory.")
flags.DEFINE_bool("disable_grappler_optimizations", False,
                  "Disable Grappler if need be to avoid tensor format errors.")


def reformat(s):
    s = s.lower().split()
    s = "_".join(s)
    s = " ".join([char for char in s])
    return s


def reformat2(s):
    s = s.replace(" ", "")
    s = s.replace("_", " ")
    return s


def calculate_loss(line,
                   encoders,
                   targets_ph,
                   sess,
                   losses):
    targets_numpy = encoders["targets"].encode(
        line) + [text_encoder.EOS_ID]
    feed = {targets_ph: targets_numpy}
    np_loss = sess.run(losses["training"], feed)
    return np_loss


def word_elimination(lines,
                     encoders,
                     targets_ph,
                     sess,
                     losses,
                     top_k=5,
                     min_sent_length=3):
    line_length = len(lines[0][0].split("_"))
    print("Line length: {}".format(line_length))

    results = {}
    if line_length <= min_sent_length:
        for line, _ in lines:
            results[line] = calculate_loss(line, encoders, targets_ph, sess, losses)
        results = sorted(results.items(), key=operator.itemgetter(1))
        return results[:top_k]

    else:
        for line, _ in lines:
            line = [word.strip() for word in line.split("_")]
            new_lines = itertools.combinations(line, len(line) - 1)
            for line in new_lines:
                line = " _ ".join(line)
                results[line] = calculate_loss(line, encoders, targets_ph, sess, losses)
        results = sorted(results.items(), key=operator.itemgetter(1))
        return results[:top_k] + word_elimination(results[:top_k],
                                                  encoders,
                                                  targets_ph,
                                                  sess,
                                                  losses,
                                                  top_k=5,
                                                  min_sent_length=min_sent_length
                                                  )


def word_incrementation(lines,
                        encoders,
                        targets_ph,
                        sess,
                        losses,
                        max_sent_length,
                        vocab,
                        top_k=5):
    line_length = len(lines[0][0].split("_"))
    print("Line length: {}".format(line_length))

    results = {}
    if line_length >= max_sent_length:
        for line, _ in lines:
            for word in vocab:
                tmp_line = line + " _ " + word
                tmp_line[line] = calculate_loss(line, encoders, targets_ph, sess, losses)
        results = sorted(results.items(), key=operator.itemgetter(1))
        return results[:top_k]

    else:
        for line, _ in lines:
            for word in vocab:
                tmp_line = line + " _ " + word
                results[tmp_line] = calculate_loss(tmp_line, encoders, targets_ph, sess, losses)
        results = sorted(results.items(), key=operator.itemgetter(1))
        return results[:top_k] + word_incrementation(results[:top_k],
                                                     encoders,
                                                     targets_ph,
                                                     sess,
                                                     losses,
                                                     max_sent_length,
                                                     vocab)


def create_hparams():
    return trainer_lib.create_hparams(
        FLAGS.hparams_set,
        FLAGS.hparams,
        data_dir=os.path.expanduser(FLAGS.data_dir),
        problem_name=FLAGS.problem)


def create_decode_hparams():
    decode_hp = decoding.decode_hparams(FLAGS.decode_hparams)
    decode_hp.shards = FLAGS.decode_shards
    decode_hp.shard_id = FLAGS.worker_id
    decode_in_memory = FLAGS.decode_in_memory or decode_hp.decode_in_memory
    decode_hp.decode_in_memory = decode_in_memory
    decode_hp.decode_to_file = FLAGS.decode_to_file
    decode_hp.decode_reference = FLAGS.decode_reference
    return decode_hp


def decode(estimator, hparams, decode_hp):
    """Decode from estimator. Interactive, from file, or from dataset."""
    if FLAGS.decode_interactive:
        if estimator.config.use_tpu:
            raise ValueError("TPU can only decode from dataset.")
        decoding.decode_interactively(estimator, hparams, decode_hp,
                                      checkpoint_path=FLAGS.checkpoint_path)
    elif FLAGS.decode_from_file:
        decoding.decode_from_file(estimator, FLAGS.decode_from_file, hparams,
                                  decode_hp, FLAGS.decode_to_file,
                                  checkpoint_path=FLAGS.checkpoint_path)
        if FLAGS.checkpoint_path and FLAGS.keep_timestamp:
            ckpt_time = os.path.getmtime(FLAGS.checkpoint_path + ".index")
            os.utime(FLAGS.decode_to_file, (ckpt_time, ckpt_time))
    else:
        decoding.decode_from_dataset(
            estimator,
            FLAGS.problem,
            hparams,
            decode_hp,
            decode_to_file=FLAGS.decode_to_file,
            dataset_split="test" if FLAGS.eval_use_test_set else None,
            checkpoint_path=FLAGS.checkpoint_path)


def score_file(filename):
    """Score each line in a file and return the scores."""
    # Prepare model.
    hparams = create_hparams()
    encoders = registry.problem(FLAGS.problem).feature_encoders(FLAGS.data_dir)
    has_inputs = "inputs" in encoders

    # Prepare features for feeding into the model.
    if has_inputs:
        inputs_ph = tf.placeholder(dtype=tf.int32)  # Just length dimension.
        batch_inputs = tf.reshape(inputs_ph, [1, -1, 1, 1])  # Make it 4D.
    targets_ph = tf.placeholder(dtype=tf.int32)  # Just length dimension.
    batch_targets = tf.reshape(targets_ph, [1, -1, 1, 1])  # Make it 4D.
    if has_inputs:
        features = {"inputs": batch_inputs, "targets": batch_targets}
    else:
        features = {"targets": batch_targets}

    # Prepare the model and the graph when model runs on features.
    model = registry.model(FLAGS.model)(hparams, tf.estimator.ModeKeys.EVAL)
    _, losses = model(features)
    saver = tf.train.Saver()

    with tf.Session() as sess:  # SOLUTION SOLUTION SOLUTION SOLUTION
        # Load weights from checkpoint.
        if FLAGS.checkpoint_path is None:
            ckpts = tf.train.get_checkpoint_state(FLAGS.output_dir)
            ckpt = ckpts.model_checkpoint_path
        else:
            ckpt = FLAGS.checkpoint_path
        saver.restore(sess, ckpt)

        # # DELETE THAT Run the language model on each line.
        # with tf.gfile.Open(filename) as f:
        #     lines = f.readlines()

        DIR_FOR_DECODE = os.environ['DIR_FOR_DECODE']
        DIR_TO_DECODE = os.environ['DIR_TO_DECODE']

        import json
        import copy

        for model in os.listdir(DIR_FOR_DECODE):
            decode_from = os.path.join(DIR_FOR_DECODE, model)
            decode_to = os.path.join(DIR_TO_DECODE, model)
            for file in os.listdir(decode_from):
                print(file)
                full_path = os.path.join(decode_from, file)

                # open a file and correct sentences
                with open(full_path) as f:
                    article = json.load(f)
                    file_copy = copy.deepcopy(article)

                    for sentence, values in article.items():
                        lm_loss = []
                        for hypo in values['hypotheses']:
                            hypo = reformat(hypo)
                            loss = calculate_loss(hypo, encoders, targets_ph, sess, losses)
                            lm_loss.append(float(loss))
                        file_copy[sentence]['lm_loss'] = lm_loss

                        f.close()

                # save corrected text
                with open(os.path.join(decode_to, file), 'w') as new_file:
                    json.dump(file_copy, new_file, ensure_ascii=False)
                new_file.close()


def main(_):
    tf.logging.set_verbosity(tf.logging.INFO)
    trainer_lib.set_random_seed(FLAGS.random_seed)
    usr_dir.import_usr_dir(FLAGS.t2t_usr_dir)

    if FLAGS.score_file:
        filename = os.path.expanduser(FLAGS.score_file)
        if not tf.gfile.Exists(filename):
            raise ValueError("The file to score doesn't exist: %s" % filename)
        results = score_file(filename)
        # if not FLAGS.decode_to_file:
        #     raise ValueError("To score a file, specify --decode_to_file for results.")
        # write_file = tf.gfile.Open(os.path.expanduser(FLAGS.decode_to_file), "w")
        # for sentence, score in results:
        #     write_file.write(sentence + "\t" + "SCORE:" + "%.6f\n" % score)
        # write_file.close()
        return

    hp = create_hparams()
    decode_hp = create_decode_hparams()
    run_config = t2t_trainer.create_run_config(hp)
    if FLAGS.disable_grappler_optimizations:
        run_config.session_config.graph_options.rewrite_options.disable_meta_optimizer = True

    # summary-hook in tf.estimator.EstimatorSpec requires
    # hparams.model_dir to be set.
    hp.add_hparam("model_dir", run_config.model_dir)

    estimator = trainer_lib.create_estimator(
        FLAGS.model,
        hp,
        run_config,
        decode_hparams=decode_hp,
        use_tpu=FLAGS.use_tpu)

    decode(estimator, hp, decode_hp)


if __name__ == "__main__":
    tf.logging.set_verbosity(tf.logging.INFO)
    tf.app.run()
