from os import walk

class Precision:
    def __init__(self, value, num):
        self.value = value
        self.name = "Average Precision"
        self.num = num
    
    def __str__(self):
        return "    Precision at epoch {}: {:.1f}%".format(self.num, self.value*100)

def parse_line(line, index):
    if "Precision" in line:
        value = float(line[-6:-1])
        return Precision(value, index)
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
     
    checkpoint_nbs.sort()
    checkpoint_max = max(checkpoint_nbs)
    
    checkpoint_max = 1000
    i = 0
    
    if checkpoint_max > 100:
        checkpoint_nbs = [i for i in range(100, checkpoint_max, 100)]
        checkpoint_nbs.append(checkpoint_max)
        

        with open("output.txt", 'r') as file:
            lines = file.readlines()
            for line in lines:
                try:
                    index = checkpoint_nbs[i]
                except IndexError:
                    break
                parsed = parse_line(line, index)
                if type(parsed) == Precision and "IoU=0.50      | area=   all " in line:
                    i+=1
                    checkpoints.append(parsed)
        print("\nResults of training:")
        print(*checkpoints,sep='\n')
        print(end="\nCheckpoint {} will be converted.".format(checkpoint_max))
    else:
        print(end="\nWPILib advises that you train for more epochs. 500+ is recommended.")


if __name__ == "__main__":
    main()