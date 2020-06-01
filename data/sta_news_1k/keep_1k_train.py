import os

KEEP = 1000
for i, file in enumerate(os.listdir('train')):
    num = os.path.splitext(file)
    if int(num[0]) < KEEP:
        print(num)
        continue
    else:
        os.remove(os.path.join('train', file))
