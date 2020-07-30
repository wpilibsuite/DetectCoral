import cv2
import numpy as np
import tensorflow as tf


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
            label_map = []
            for obj in self.file:
                obj = [i for i in obj.split('\n') if i]
                i = int(obj[1].split()[1]) - 1
                name = obj[2].split()[1][1:-1]
                label_map.append(name)
            self.file = label_map

    def get_labels(self):
        return self.file


from time import time


def test_video(video_path, interpreter, input_details, output_details, labels):
    flag = True
    frames = 0
    height = input_details[0]['shape'][1]
    width = input_details[0]['shape'][2]
    input_mean = 127.5
    input_std = 127.5
    print(output_details)

    video = cv2.VideoCapture(video_path)
    imW = video.get(cv2.CAP_PROP_FRAME_WIDTH)
    imH = video.get(cv2.CAP_PROP_FRAME_HEIGHT)
    fps = video.get(cv2.CAP_PROP_FPS)
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter("/opt/ml/model/inference.avi", fourcc, fps, (int(imW), int(imH)))

    floating_model = (input_details[0]['dtype'] == np.float32)
    while (video.isOpened()):
        start = time()
        # Acquire frame and resize to expected shape [1xHxWx3]
        ret, frame = video.read()
        if ret is None:
            break
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_resized = cv2.resize(frame_rgb, (width, height))
        input_data = np.expand_dims(frame_resized, axis=0)

        # Normalize pixel values if using a floating model (i.e. if model is non-quantized)
        if floating_model:
            input_data = (np.float32(input_data) - input_mean) / input_std

        # Perform the actual detection by running the model with the image as input
        interpreter.set_tensor(input_details[0]['index'], input_data)
        interpreter.invoke()

        # Retrieve detection results
        boxes = interpreter.get_tensor(output_details[0]['index'])[0]  # Bounding box coordinates of detected objects
        classes = interpreter.get_tensor(output_details[1]['index'])[0]  # Class index of detected objects
        scores = interpreter.get_tensor(output_details[2]['index'])[0]  # Confidence of detected objects
        if flag:
            print("Classes", classes)
            flag = False

        # Loop over all detections and draw detection box if confidence is above minimum threshold
        for i in range(len(scores)):
            if ((scores[i] > .5) and (scores[i] <= 1.0)):
                # Get bounding box coordinates and draw box
                # Interpreter can return coordinates that are outside of image dimensions, need to force them to be within image using max() and min()
                ymin = int(max(1, (boxes[i][0] * imH)))
                xmin = int(max(1, (boxes[i][1] * imW)))
                ymax = int(min(imH, (boxes[i][2] * imH)))
                xmax = int(min(imW, (boxes[i][3] * imW)))

                cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), (10, 255, 0), 4)

                # Draw label
                try:
                    object_name = labels[int(classes[i])]  # Look up object name from "labels" array using class index
                    label = '%s: %d%%' % (object_name, int(scores[i] * 100))  # Example: 'person: 72%'
                    label_size, base = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)  # Get font size
                    label_ymin = max(ymin, label_size[1] + 10)  # Make sure not to draw label too close to top of window
                    cv2.rectangle(frame, (xmin, label_ymin - label_size[1] - 10),
                                  (xmin + label_size[0], label_ymin + base - 10),
                                  (255, 255, 255), cv2.FILLED)  # Draw white box to put label text in
                    cv2.putText(frame, label, (xmin, label_ymin - 7), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0),
                                2)  # Draw label text
                except:
                    print(classes, scores)


        # All the results have been drawn on the frame, so it's time to display it.
        if frames % 50 == 0:
            print("Completed", frames, "frames. FPS:", (1 / (time() - start)))
        frames += 1
        out.write(frame)
        video.release()
        cv2.destroyAllWindows()


def main(video_path):
    parser = PBTXTParser("/opt/ml/model/map.pbtxt")
    parser.parse()
    labels = parser.file

    interpreter = tf.contrib.lite.Interpreter(
        model_path="/tensorflow/models/research/learn/models/output_tflite_graph.tflite")
    interpreter.allocate_tensors()

    # Get model details
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
    test_video(video_path, interpreter, input_details, output_details, labels)

    print("Done.")
    # Clean up
