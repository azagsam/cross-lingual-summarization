import os

for i, file in enumerate(os.listdir('val')):
    file = os.path.join('val', file)
    os.rename(file, 'val/{}.json'.format(i))
