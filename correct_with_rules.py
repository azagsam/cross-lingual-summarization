import copy
import json
import os
import string
import argparse


def remove_all_punctuations(text):
    return [word for word in text if word not in string.punctuation]


def remove_repeating_punctuations(text):
    removed_punctuation = []
    for previous, current in zip(text, text[1:]):
        if previous in string.punctuation and current in string.punctuation:
            continue
        else:
            removed_punctuation.append(previous)
    return removed_punctuation


def remove_repeating_n_grams(text, n_gram=3):
    if n_gram == 0:
        return text
    else:
        corrected_text = []
        for ind, word in enumerate(text):
            current_ngram = corrected_text[-n_gram:]
            next_ngram = text[ind:ind + n_gram]
            if current_ngram == next_ngram:
                continue
            else:
                corrected_text.append(word)
        return remove_repeating_n_grams(corrected_text, n_gram - 1)


def remove_repeating_trigrams(text):
    while True:
        corrected_text = []
        for ind, word in enumerate(text):
            current_ngram = corrected_text[-3:]
            next_ngram = text[ind:ind + 3]

            if ind + 3 >= len(text):
                if set(current_ngram) == set(next_ngram):
                    return corrected_text
                else:
                    corrected_text += next_ngram
                    return corrected_text

            elif set(current_ngram) == set(next_ngram):
                text = corrected_text + text[ind + 3:]
                break

            else:
                corrected_text.append(word)

def clean_text(data_dir, dump_dir, punct=True, trigrams=True, n_grams=True):
    for i, file in enumerate(os.listdir(data_dir)):
        if i % 100 == 0:
            print(i)
        if 'log' in file:
            continue

        #file_num = int(file.split('.')[0])
        #print(file_num)
        
        # evaluate small sample
        #if int(file.split('.')[0]) > 100:
        #    continue 
        
        full_path = os.path.join(data_dir, file)

        # open a file and correct sentences
        with open(full_path) as f:
            article = json.load(f)
            file_copy = copy.deepcopy(article)

            for sentence, values in article.items():
                cleaned_text = []
                for hypo in values['hypotheses']:
                    sent = hypo.split()

                    # remove punctuation from the sentence
                    if punct:
                        sent = remove_repeating_punctuations(sent)

                    # run the remove_repeated_n_grams function several times
                    if n_grams:
                        for n in range(10):
                            sent = remove_repeating_n_grams(sent)

                    # remove repeating trigrams
                    # if trigrams:
                    #    sent = remove_repeating_trigrams(sent)

                    # append sentence
                    cleaned_text.append(" ".join(sent))

                file_copy[sentence]['hypotheses'] = cleaned_text

        # save corrected text
        with open(os.path.join(dump_dir, file), 'w') as new_file:
            json.dump(file_copy, new_file, ensure_ascii=False)


if __name__ == '__main__':
    for model in os.listdir('models'):
        print(model)
        data_dir = os.path.join('models', model, 'exported_beams')
        dump_dir = os.path.join('post_processing', 'rule_corrected', model)
        os.makedirs(dump_dir, exist_ok=True)
        print('Directories are created!')
        clean_text(data_dir, dump_dir)
