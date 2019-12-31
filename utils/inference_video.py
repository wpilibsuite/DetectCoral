import numpy as np
from time import time
import json
import sys
from edgetpu.detection.engine import DetectionEngine
from PIL import Image
from PIL import ImageDraw
from cscore import CameraServer, VideoSource, UsbCamera, MjpegServer
from networktables import NetworkTablesInstance
import argparse
import cv2

class PBTXTParser:
    def __init__(self, path):
        self.path = path
        self.file = None

    def parse(self):
        with open(self.path, 'r') as f:
            self.file = ''.join([i.replace('item', '') for i in f.readlines()])
            blocks = []
            obj = ""
            for i in self.file:
                if i == '}':
                    obj += i
                    blocks.append(obj)
                    obj = ""
                else:
                    obj += i
            self.file = blocks
            label_map = {}
            for obj in self.file:
                obj = [i for i in obj.split('\n') if i]
                i = int(obj[1].split()[1]) - 1
                name = obj[2].split()[1][1:-1]
                label_map.update({i: name})
            self.file = label_map

    def get_labels(self):
        return self.file


def log_object(obj, labels):
    print('-----------------------------------------')
    if labels:
        print(labels[obj.label_id])
    print("score = {:.3f}".format(obj.score))
    box = obj.bounding_box.flatten().tolist()
    print("box = [{:.3f}, {:.3f}, {:.3f}, {:.3f}]".format(*box))


def main(video):

    cap = cv2.VideoCapture(video)
    out = cv2.VideoWriter("output.avi",cv2.VideoWriter_fourcc(*'MJPG'),cap.get(cv2.CAP_PROP_FPS),(320,240))
    print("Initializing ML engine")
    engine = DetectionEngine("model.tflite")
    parser = PBTXTParser("map.pbtxt")
    parser.parse()
    labels = parser.get_labels()

    start = time()

    print("Starting ML mainloop")
    while True:
        t, img = cap.read()
        img = cv2.resize(img, (320, 240))
        frame = Image.fromarray(img)
        draw = ImageDraw.Draw(frame)

        # Run inference.
        ans = engine.detect_with_image(frame, threshold=0.5, keep_aspect_ratio=True, relative_coord=False, top_k=10)

        boxes = []
        names = []

        # Display result.
        if ans:
            for obj in ans:
                log_object(obj, labels)
                if labels:
                    names.append(labels[obj.label_id])
                box = [round(i,3) for i in obj.bounding_box.flatten().tolist()]
                boxes.extend(box)
                # Draw a rectangle.
                draw.rectangle(box, outline='green')
            out.write(frame)

        else:
            print('No object detected!')
            out.write(frame)
        print("FPS: {:.1f}".format(1 / (time() - start)))

        start = time()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--video", type=str, required=True, help="Path to unlabeled video.")
    args = parser.parse_args()
    main(args.video)
