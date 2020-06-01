from tqdm import tqdm


def useless():
    for line in tqdm(open("output/language-model-tokenized.txt")):
        chars = [char if char is not " " else "_" for char in list(line.strip())[:-2]]  # remove punctuation and last /check again
        # print(" ".join(chars).lower())
        full_line = " ".join(chars).lower()
        with open("output/language-model-characters-test-multiprocess.txt", 'a') as f:
            f.write(full_line)
            f.write("\n")


from multiprocessing import Pool

def f(x):
    return x*x

if __name__ == '__main__':
    p = Pool(3)
    print(p.map(useless, [1, 2]))