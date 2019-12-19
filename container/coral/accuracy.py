class Average:
    def __init__(self, value):
        self._value = value
        self.name = None
    def get(self):
        return self._value

    def __str__(self):
        return f"{self.name}: {self._value}"

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
    with open("output.txt", 'r') as file:
        lines = file.readlines()
        checkpoint_nb = 0
        checkpoint = CheckpointAccuracy(checkpoint_nb)
        for line in lines:
            if len(checkpoint.lines) == 12:
                checkpoints.append(checkpoint)
                checkpoint_nb += 1
                checkpoint = CheckpointAccuracy(checkpoint_nb)
            line = parse_line(line)
            if type(line) != int:
                checkpoint.lines.append(line)
    print("\nResults of training:")
    print(*checkpoints,sep='\n')
    print(end="\nCheckpoint {} will be converted.".format(len(checkpoints) - 1))


if __name__ == "__main__":
    main()