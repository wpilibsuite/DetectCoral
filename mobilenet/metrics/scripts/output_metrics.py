import subprocess

import log_parser
import parse_hyperparams

def main():
    # tensorboard runs at http://localhost:6006
    subprocess.Popen(['tensorboard', '--logdir', '/opt/ml/model/train'])
    data = parse_hyperparams.parse("/opt/ml/model/hyperparameters.json")
    TRAIN_STEPS = data["epochs"]
    parser = log_parser.EvalJSONifier(TRAIN_STEPS)
    parser.start()

if __name__ == "__main__":
    main()