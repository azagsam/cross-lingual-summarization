import json
import os

for n, file in enumerate(os.listdir('data/sta-subset-json')):
    with open('data/sta-subset-json/' + file) as f:
        f = json.load(f)
        article_sent = f['article']
        abstract_sent = f['abstract']

        with open('/home/ales/Documents/magisterij/utils/rouge2-1.2.1-runnable/projects/sta/reference/sta{}_reference1.txt'.format(n), 'a') as ref:
            for a in article_sent:
                ref.write(a)
                ref.write('\n')

        with open('/home/ales/Documents/magisterij/utils/rouge2-1.2.1-runnable/projects/sta/system/sta{}_system1.txt'.format(n), 'a') as system:
            for a in abstract_sent:
                system.write(a)
                system.write('\n')