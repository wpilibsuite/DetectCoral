from os import walk

class Average:
    def __init__(self, value):
        self._value = value
        self.name = None
    def get(self):
        return self._value

    def __str__(self):
        return "{}: {}".format(self.name, self._value)

class Precision(Average):
    def __init__(self, value):
        super(Precision, self).__init__(value)
        self.name = "Average Precision"

class Recall(Average):
    def __init__(self, value):
        super(Recall, self).__init__(value)
        self.name = "Average Recall"

class CheckpointAccuracy:
    def __init__(self, checkpoint_nb):
        self.number = checkpoint_nb
        self.lines = []

    def __repr__(self):
        precision = []
        recall = []
        for line in self.lines:
            if type(line) == Precision:
                precision.append(line.get())
            else:
                recall.append(line.get())
        precision = sum(precision) / len(precision)
        recall = sum(recall) / len(recall)
        accuracy = (precision * recall * 100) / (precision + recall)
        return "    Checkpoint {} accuracy: {:.3f}%".format(self.number, accuracy)

def parse_line(line):
    if "Precision" in line or "Recall" in line:
        metric_type = Precision if "Precision" in line else Recall
        value = float(line[-6:-1])
        return metric_type(value)
    else:
        return 0

def main():
    checkpoints = []
    checkpoint_nbs = []
    f = []
    for (dirpath, dirnames, filenames) in walk("./learn/train/"):
        for file in filenames:
            if file.endswith(".meta"):
                checkpoint_nbs.append(int(file[file.find('-')+1:file.rfind('.')]))
    checkpoint_nbs = checkpoint_nbs[1:]
    checkpoint_nbs.append(-1)
    print(*checkpoint_nbs)

    with open("output.txt", 'r') as file:
        lines = file.readlines()
        i = 0
        checkpoint = CheckpointAccuracy(checkpoint_nbs[i])
        for line in lines:
            line = parse_line(line)
            if len(checkpoint.lines) == 12:
                checkpoints.append(checkpoint)
                i += 1
                checkpoint = CheckpointAccuracy(checkpoint_nbs[i])
            if type(line) != int:
                checkpoint.lines.append(line)
    print("\nResults of training:")
    print(*checkpoints,sep='\n')
    print(end="\nCheckpoint {} will be converted.".format(checkpoint_nbs[-2]))


if __name__ == "__main__":
    main()