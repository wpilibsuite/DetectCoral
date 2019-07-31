from os import walk
import json
import glob, os
import random


base="/opt/ml/input/data/training"
f = []
for file in glob.glob("**/**/**/**/*.json"):
    f.append(file)
# print(len(f))
random.shuffle(f)
evals = len(f) // 10
train_jsons = f[evals:]
eval_jsons = f[:evals]

def make_csv(csv_path, files):
    with open(csv_path, "w+") as csv:
        csv.write("filename,width,height,class,xmin,ymin,xmax,ymax\n")
        i = 0
        for filename in files:
            
            if i % 100 == 0:pass
#                 print(100*i/len(files), '% done')
            i += 1
            path = base + '/' + filename
            filename = filename.split('/')
#             print(filename)
#             break
            filename[3] = 'img'
            filename[4] = filename[4][:-5]
            with open(path, 'r') as file:
                line = json.loads(file.readlines()[0])
                for obj in line["objects"]:

                    p1, p2 = obj["points"]["exterior"]
                    x1, x2 = sorted([p1[0], p2[0]])
                    y1, y2 = sorted([p1[1], p2[1]])
                    
                    entry = ['/'.join(filename), line["size"]["width"], line["size"]["height"], obj["classTitle"], x1, y1, x2, y2]
                    csv.write(",".join(map(str, entry)) + '\n')
        
make_csv("/opt/ml/input/data/training/tmp/train.csv", train_jsons)
make_csv("/opt/ml/input/data/training/tmp/eval.csv", eval_jsons)
