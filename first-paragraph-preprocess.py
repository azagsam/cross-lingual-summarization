"""
Script adds two average sentences to first paragraph for heuristic test
"""

with open('data/sta-first-paragraph.txt') as file:
    add = ' V Cannesu bo od 14. do 25. maja potekal 72. mednarodni filmski festival, ki velja za najbolj glamuroznega na svetu. ' \
          'Uvedla ga bo premiera zombie komedije The Dead Don\'t Die ameriškega režiserja Jima Jarmuscha. '
    for txt in file.readlines():
        with open('preprocessed/sta-first-paragraph-add-text.txt', 'a') as newfile:
            newfile.write(txt.strip() + add + '\n')

