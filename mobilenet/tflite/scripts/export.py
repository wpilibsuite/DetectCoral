import subprocess, shutil, tarfile, glob, os, datetime
from os.path import join
import parse_hyperparams

model_dir = '/opt/ml/model/'
first_export = 'output_tflite_graph.tflite'
second_export = 'output_tflite_graph_edgetpu.tflite'


def logstatus(message):
    print(message)
    with open('status.txt', 'w') as status:
        status.write(message)


def main(epoch, output_name):
    output_path = "/opt/ml/model/"

    logstatus('converting model to tflite')
    subprocess.check_call("./convert_checkpoint_to_edgetpu_tflite.sh --checkpoint_num %s" % (epoch), shell=True)
    shutil.copy(join(model_dir, first_export), join(output_path, 'unoptimized.tflite'))

    logstatus('compiling model for edgetpu')
    subprocess.check_call("edgetpu_compiler %s -o %s" % (join(model_dir, first_export), output_path), shell=True)

    logstatus('compressing model to tar')
    with tarfile.open(join(output_path, output_name + '.tar.gz'), 'w:gz') as model:
        model.add(join(output_path, second_export), arcname='model.tflite')
        model.add('/opt/ml/model/map.pbtxt', arcname='map.pbtxt')
        model.add(join(output_path, 'unoptimized.tflite'), arcname='unoptimized.tflite')

    logstatus('Finished! Get your model.')


if __name__ == "__main__":
    data = parse_hyperparams.parse("/opt/ml/model/hyperparameters.json")

    main(data["epochs"], data["name"])
