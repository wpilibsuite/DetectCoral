import subprocess, shutil, tarfile, glob, os, datetime
from os.path import join

model_dir = 'learn/models/'
first_export = 'output_tflite_graph.tflite'
second_export = 'output_tflite_graph_edgetpu.tflite'


def logstatus(message):
    print(message)
    with open('status.txt', 'w') as status:
        status.write(message)


def copy_checkpoint(epoch, name):
    export_time = datetime.datetime.now().strftime('%c').replace(' ', '-').replace(':', '-')
    checkpoint_files = glob.glob('learn/train/model.ckpt-%s*' % (epoch))
    os.mkdir('/opt/ml/model/checkpoints/%s-%s/' % (name, export_time))
    for path in checkpoint_files:
        shutil.copyfile(path, '/opt/ml/model/checkpoints/%s-%s/%s' % (
        name, export_time, os.path.basename(path).replace('-%s' % (epoch), '', 1)))


def main(epoch, output_path, output_name):
    copy_checkpoint(epoch, output_name)
    if not os.path.exists(output_path):
        os.mkdir(output_path)
    export_time = datetime.datetime.now().strftime('%c').replace(' ', '-').replace(':', '-')
    output_path = join(output_path, '%s-%s' % (output_name, export_time))
    os.mkdir(output_path)

    logstatus('converting model to tflite')
    subprocess.check_call("./convert_checkpoint_to_edgetpu_tflite.sh --checkpoint_num %s" % (epoch), shell=True)
    shutil.copy(join(model_dir, first_export), join(output_path, 'unoptimized.tflite'))

    logstatus('compiling model for edgetpu')
    subprocess.check_call("edgetpu_compiler ./%s -o %s" % (join(model_dir, first_export), output_path), shell=True)

    logstatus('compressing model to tar')
    with tarfile.open(join(output_path, output_name + '.tar.gz'), 'w:gz') as model:
        model.add(join(output_path, second_export), arcname='model.tflite')
        model.add('/opt/ml/input/data/training/map.pbtxt', arcname='map.pbtxt')
        model.add(join(output_path, 'unoptimized.tflite'), arcname='unoptimized.tflite')

    logstatus('Finished! Get your model.')


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--step', type=int, required=True)
    parser.add_argument('-n', '--output_name', type=str, default='model')
    parser.add_argument('-o', '--output_path', type=str, default='/opt/ml/model/')
    args = parser.parse_args()

    main(args.step, args.output_path, args.output_name)
