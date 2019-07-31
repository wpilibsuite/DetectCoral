import json
import argparse
import glob

def get_labels():
    f = None
    for file in glob.glob("**/**/meta.json"):
        f = file
    with open(f, 'r') as meta:
        return [label["title"] for label in json.loads(meta.readlines()[0])["classes"]]

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-out', '--output_pbtxt', help='define the output pbtxt file', type=str, required=True)
    args = parser.parse_args()
    with open(args.output_pbtxt, 'w+') as pbtxt:
        for i, label in enumerate(get_labels()):
            pbtxt.write("item {\n\nid: %s\n\nname: \"%s\"\n}\n\n"% (i+1, label))
