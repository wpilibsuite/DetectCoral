import parse_meta

if __name__ == "__main__":
    a = ""
    with open("/opt/ml/input/data/training/map.pbtxt",'r') as f:
        for i in f.readlines():
            a+=i
    print(a.count('id'))
