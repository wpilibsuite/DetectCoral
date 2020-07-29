import subprocess
import tarfile
from os.path import join

import parse_hyperparams


def main():
    model_dir = "/opt/ml/model/"
    unoptimized = "/tensorflow/models/research/learn/models/output_tflite_graph.tflite"
    second_export = "output_tflite_graph_edgetpu.tflite"
    data = parse_hyperparams.parse(model_dir + "hyperparameters.json")

    epoch = data["epochs"]
    output_name = data["name"]
    subprocess.check_call("./convert_checkpoint_to_edgetpu_tflite.sh --checkpoint_num %s" % epoch, shell=True)
    subprocess.check_call("edgetpu_compiler %s -o %s" % (unoptimized, model_dir), shell=True)

    with tarfile.open(join(model_dir, output_name + ".tar.gz"), 'w:gz') as model:
        model.add(join(model_dir, second_export), arcname="model.tflite")
        model.add(model_dir + "map.pbtxt", arcname="map.pbtxt")
        model.add(unoptimized, arcname="unoptimized.tflite")


if __name__ == "__main__":
    main()
