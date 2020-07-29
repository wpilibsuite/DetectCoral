def get_total():
    a = ""
    with open("/opt/ml/model/map.pbtxt", 'r') as f:
        for i in f.readlines():
            a += i
    return a.count("id")
