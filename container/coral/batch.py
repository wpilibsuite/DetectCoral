import json
import sys
"""
By Grant Perkins, 2019

Gets the number of training steps from SageMaker
"""
if __name__ == "__main__":
    with open("/opt/ml/input/config/hyperparameters.json", 'r') as f:
        try:
            print(json.load(f)["batch_size"])
        except:
            print(32)
