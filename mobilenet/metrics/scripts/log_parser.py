from __future__ import print_function
import glob
import time
import json
from collections import OrderedDict

from tensorboard.backend.event_processing.event_accumulator import EventAccumulator


class EvalJSONifier:
    """
    Thread for converting evaluation binaries to json
    """

    def __init__(self, last_epoch):
        """
        Initializes the thread
        Args:
            last_epoch: the epoch to kill the thread on
        """
        self.tf_size_guidance = {
            'compressedHistograms': 10,
            'images': 1,
            'scalars': 1000,
            'histograms': 1
        }
        self.log_path = "/opt/ml/model/train/eval_0/*"
        self.last_epoch = last_epoch
        self.precision = OrderedDict()

    def start(self):
        """
        Returns:
            None
        """
        accumulator = None
        log = []
        step = -1
        last_saved_epoch = -1
        while step != self.last_epoch:
            if len(log) != 0 and accumulator is None:
                accumulator = EventAccumulator(log[0], self.tf_size_guidance)
            if accumulator is not None:
                accumulator.Reload()
                mAP = accumulator.Scalars("DetectionBoxes_Precision/mAP")
                for entry in mAP:
                    self.precision[int(entry.step)] = float(entry.value)
                if last_saved_epoch != int(mAP[-1].step):
                    last_saved_epoch = int(mAP[-1].step)
                    with open("/opt/ml/model/metrics.json", 'w') as file:
                        json.dump({"precision": self.precision}, file)
            else:
                log = glob.glob(self.log_path)
            time.sleep(10)
