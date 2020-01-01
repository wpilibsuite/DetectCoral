import numpy as np
from time import time
import json
import sys
from edgetpu.detection.engine import DetectionEngine
from PIL import Image, ImageDraw, ImageFont
from cscore import CameraServer, VideoSource, UsbCamera, MjpegServer
from networktables import NetworkTablesInstance


def parseError(str, config_file):
    """Report parse error."""
    print("config error in '" + config_file + "': " + str, file=sys.stderr)


def read_config(config_file):
    """Read configuration file."""
    team = -1

    # parse file
    try:
        with open(config_file, "rt", encoding="utf-8") as f:
            j = json.load(f)
    except OSError as err:
        print("could not open '{}': {}".format(config_file, err), file=sys.stderr)
        return team

    # top level must be an object
    if not isinstance(j, dict):
        parseError("must be JSON object", config_file)
        return team

    # team number
    try:
        team = j["team"]
    except KeyError:
        parseError("could not read team number", config_file)

    # cameras
    try:
        cameras = j["cameras"]
    except KeyError:
        parseError("could not read cameras", config_file)

    return team


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


def main(config):
    team = read_config(config)
    WIDTH, HEIGHT = 320, 240
    font = ImageFont.truetype('usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 15)

    print("Connecting to Network Tables")
    ntinst = NetworkTablesInstance.getDefault()
    ntinst.startClientTeam(team)

    """Format of these entries found in WPILib documentation."""
    nb_objects_entry = ntinst.getTable("ML").getEntry("nb_objects")
    boxes_entry = ntinst.getTable("ML").getEntry("boxes")
    object_classes_entry = ntinst.getTable("ML").getEntry("object_classes")

    print("Starting camera server")
    cs = CameraServer.getInstance()
    camera = cs.startAutomaticCapture()
    camera.setResolution(WIDTH, HEIGHT)
    cvSink = cs.getVideo()
    img = np.zeros(shape=(HEIGHT, WIDTH, 3), dtype=np.uint8)
    output = cs.putVideo("MLOut", WIDTH, HEIGHT)

    print("Initializing ML engine")
    engine = DetectionEngine("model.tflite")
    parser = PBTXTParser("map.pbtxt")
    parser.parse()
    labels = parser.get_labels()

    start = time()

    print("Starting ML mainloop")
    while True:
        t, img = cvSink.grabFrame(img)
        frame = Image.fromarray(img)
        draw = ImageDraw.Draw(frame)

        # Run inference.
        ans = engine.detect_with_image(frame, threshold=0.5, keep_aspect_ratio=True, relative_coord=False, top_k=10)
        nb_objects_entry.setNumber(len(ans))

        boxes = []
        names = []

        # Display result.
        if ans:
            for obj in ans:
                log_object(obj, labels)
                if labels:
                    names.append(labels[obj.label_id])
                box = [round(i, 3) for i in obj.bounding_box.flatten().tolist()]
                boxes.extend(box)
                # Draw a rectangle.
                draw.rectangle(box, outline='green')
                x, y, _, _ = box
                draw.text((x, y - 30), labels[obj.label_id + 1] + "  " + str(obj.score), 'green', font)

            output.putFrame(np.array(frame))

        else:
            print('No object detected!')
            output.putFrame(img)
        boxes_entry.setDoubleArray(boxes)
        object_classes_entry.setStringArray(names)
        print("FPS: {:.1f}".format(1 / (time() - start)))

        start = time()


if __name__ == '__main__':
    config_file = "/boot/frc.json"
    main(config_file)
