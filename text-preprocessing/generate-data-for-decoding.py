import random

file = open("output/split_characters/language-model-characters-test.txt").readlines()

first_words = []
for i in range(100):
    n = random.choice(file).strip()
    tokens = n.split('_')
    num_of_words = random.randint(1, 15)
    try:
        example = '_'.join(tokens[:num_of_words])
    except IndexError:
        example = '_'.join(tokens[:num_of_words])
    first_words.append(example)

first_characters = []
for i in range(100):
    n = random.choice(file).strip()
    num_of_characters = random.randint(1, 100)
    try:
        first_characters.append(n[:num_of_characters])
    except IndexError:
        first_characters.append(n)

for words, characters in zip(first_words, first_characters):
    with open('output/split_characters/decode-this.txt', 'a') as f:
        f.write(words)
        f.write('\n')
        f.write(characters)
        f.write('\n')
