import os


def replace_words(old_word, new_word, file):
    fin = open(os.path.join(os.getcwd(), file), "rt")
    lines = fin.readlines()
    fin.close()
    fout = open(os.path.join(os.getcwd(), file), "wt")
    for line in lines:
        line = line.replace(old_word, new_word)
        fout.write(line)
    fout.close()
