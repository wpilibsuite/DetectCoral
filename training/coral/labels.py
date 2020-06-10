def get():
    a = ""
    with open("/opt/ml/input/data/training/map.pbtxt", 'r') as f:
        for i in f.readlines():
            a += i
    return a.count("id")
