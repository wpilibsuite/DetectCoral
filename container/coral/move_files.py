import os, shutil

def main():
    checkpoints = {}
    for (dirpath, dirnames, filenames) in os.walk("./learn/train/"):
        for file in filenames:
            key = file[:15]
            if key not in checkpoints.keys():
                checkpoints.update({key: [file]})
            else:
                tmp = checkpoints[key]
                tmp.append(file)
                checkpoints.update({key: tmp})
    os.mkdir("evals")
    for key in checkpoints.keys():
        os.mkdir("./evals/"+key)
        for file in checkpoints[key]:
            shutil.copy("./learn/train/"+file, "./evals/"+key)

if __name__ == "__main__":
    main()