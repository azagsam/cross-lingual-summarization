# Instructions

# full paths
export USR_DIR=/home/ales/Documents/magisterij/tensor2tensor/my_trained_model/lm/trainer
export PROBLEM=language_model_char
export DATA_DIR=/home/ales/Documents/magisterij/tensor2tensor/my_trained_model/data/data_dir
export TMP_DIR=/home/ales/Documents/magisterij/tensor2tensor/my_trained_model/data/tmp_dir
export OUT_DIR=/home/ales/Documents/magisterij/tensor2tensor/my_trained_model/model
export INF_DIR=/home/ales/Documents/magisterij/tensor2tensor/my_trained_model/inference
export MODEL=transformer
export HPARAMS=transformer_base

# setup env variables
export USR_DIR=./lm/trainer
export PROBLEM=language_model_char
export DATA_DIR=./data/data_dir
export TMP_DIR=./data/tmp_dir
export OUT_DIR=./model
export INF_DIR=./inference
export MODEL=transformer
export HPARAMS=transformer_base

# get perplexity for each line
--t2t_usr_dir=./lm/trainer
--problem=language_model_char
--data_dir=./data/data_dir
--model=transformer
--hparams_set=transformer_base
--output_dir=./model
--score_file=./inference/decode-this.txt
--decode_to_file=./inference/score.txt

# get perplexity for each line
--t2t_usr_dir=./lm/trainer
--problem=language_model_char
--data_dir=./data/data_dir
--model=transformer
--hparams_set=transformer_big_single_gpu
--output_dir=/home/ales/Documents/magisterij/language-model-t2t/big_model2
--score_file=./inference/decode-this.txt
--decode_to_file=./inference/score.txt


t2t-decoder \
  --t2t_usr_dir=$USR_DIR \
  --data_dir=$DATA_DIR \
  --problem=$PROBLEM \
  --model=$MODEL \
  --hparams_set=$HPARAMS \
  --output_dir=$OUT_DIR \
  --decode_hparams="extra_length=512,beam_size=12,alpha=0.6,batch_size=1,return_beams=True" \
  --decode_from_file=$DECODE_FILE \
  --decode_to_file=$OUTPUT_FILE \
  --decode_interactive=True

t2t-decoder \
  --t2t_usr_dir=$USR_DIR \
  --problem=$PROBLEM \
  --data_dir=$DATA_DIR \
  --model=$MODEL \
  --hparams_set=$HPARAMS \
  --output_dir=$OUT_DIR \
  --decode_hparams="extra_length=512,beam_size=12,alpha=0.6,batch_size=1,return_beams=True" \
  --decode_interactive=True

t2t-eval \
  --t2t_usr_dir=$USR_DIR \
  --problem=$PROBLEM \
  --model=$MODEL \
  --hparams_set=$HPARAMS \
  --data_dir=$DATA_DIR \
  --output_dir=$OUT_DIR \
  --eval_use_test_set=True \
  --eval_steps=5 \
  --decode_hparams="extra_length=512,beam_size=12,alpha=0.6,batch_size=1,return_beams=True"


# run on server
python3 t2t_decoder_duplicate.py \
  --t2t_usr_dir=/home/azagar/myfiles/language-model-t2t-big-transformer_big_single_gpu/lm/trainer \
  --problem=language_model_char \
  --data_dir=/home/azagar/myfiles/language-model-t2t-big-transformer_big_single_gpu/data/data_dir \
  --model=transformer \
  --hparams_set=transformer_big_single_gpu \
  --output_dir=/home/azagar/myfiles/language-model-t2t-big-transformer_big_single_gpu/model \
  --score_file=/home/azagar/myfiles/language-model-t2t-big-transformer_big_single_gpu/inference/decode-this.txt \
  --decode_to_file=/home/azagar/myfiles/language-model-t2t-big-transformer_big_single_gpu/inference/score.txt

# evaluate beams
export DIR_FOR_DECODE=~/myfiles/vecmap/data/post_processing/rule_corrected/no_punct
export DIR_TO_DECODE=~/myfiles/vecmap/data/post_processing/lm_evaluated/no_punct
python t2t_decoder_duplicate_score_beams.py \
  --t2t_usr_dir=/home/azagar/myfiles/language-model-t2t-big-transformer_big_single_gpu/lm/trainer \
  --problem=language_model_char \
  --data_dir=/home/azagar/myfiles/language-model-t2t-big-transformer_big_single_gpu/data/data_dir \
  --model=transformer \
  --hparams_set=transformer_big_single_gpu \
  --output_dir=/home/azagar/myfiles/language-model-t2t-big-transformer_big_single_gpu/model \
  --score_file=/home/azagar/myfiles/language-model-t2t-big-transformer_big_single_gpu/inference/decode-this.txt \
  --decode_to_file=/home/azagar/myfiles/language-model-t2t-big-transformer_big_single_gpu/inference/score.txt


export DIR_FOR_DECODE=~/myfiles/vecmap/data/post_processing/rule_corrected
export DIR_TO_DECODE=~/myfiles/vecmap/data/post_processing/lm_evaluated
python t2t_decoder_duplicate_score_beams_multi_model.py \
  --t2t_usr_dir=/home/azagar/myfiles/language-model-t2t-big-transformer_big_single_gpu/lm/trainer \
  --problem=language_model_char \
  --data_dir=/home/azagar/myfiles/language-model-t2t-big-transformer_big_single_gpu/data/data_dir \
  --model=transformer \
  --hparams_set=transformer_big_single_gpu \
  --output_dir=/home/azagar/myfiles/language-model-t2t-big-transformer_big_single_gpu/model \
  --score_file=/home/azagar/myfiles/language-model-t2t-big-transformer_big_single_gpu/inference/decode-this.txt \
  --decode_to_file=/home/azagar/myfiles/language-model-t2t-big-transformer_big_single_gpu/inference/score.txt


python t2t_decoder_duplicate_score_beams_df.py \
  --t2t_usr_dir=/home/azagar/myfiles/language-model/language-model-t2t-big-transformer_big_single_gpu/lm/trainer \
  --problem=language_model_char \
  --data_dir=/home/azagar/myfiles/language-model/language-model-t2t-big-transformer_big_single_gpu/data/data_dir \
  --model=transformer \
  --hparams_set=transformer_big_single_gpu \
  --output_dir=/home/azagar/myfiles/language-model/language-model-t2t-big-transformer_big_single_gpu/model \
  --score_file=/home/azagar/myfiles/language-model/language-model-t2t-big-transformer_big_single_gpu/inference/decode-this.txt \
  --decode_to_file=/home/azagar/myfiles/language-model/language-model-t2t-big-transformer_big_single_gpu/inference/score.txt
