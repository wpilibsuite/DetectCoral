from train import logstatus
import subprocess, shutil, tarfile
from os.path import join

model_dir = 'learn/models/'
first_export = 'output_tflite_graph.tflite'
second_export = 'output_tflite_graph_edgetpu.tflite'

def main(epoch, output_path, output_name):

    logstatus('converting model to tflite')
    subprocess.check_call("./convert_checkpoint_to_edgetpu_tflite.sh --checkpoint_num %s" % (str(epoch)), shell=True)
    shutil.copy(join(model_dir,first_export), join(output_path,'unoptimized.tflite'))

    logstatus('compiling model for edgetpu')
    subprocess.check_call("edgetpu_compiler ./%s -o %s"%(join(model_dir,first_export), output_path), shell=True)

    logstatus('compressing model to tar')
    with tarfile.open(join(output_path,output_name),'w:gz') as model:
        model.add(join(output_path,second_export),arcname='model.tflite')
        model.add('/opt/ml/input/data/training/map.pbtxt',arcname='map.pbtxt')
        model.add(join(output_path,'unoptimized.tflite'),arcname='unoptimized.tflite')

    logstatus('Finished! Get your model.')


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-s','--step',type=int, required=True)
    parser.add_argument('-n', '--output_name',type=str, default='model')
    parser.add_argument('-o', '--output_path',type=str, default='/opt/ml/model/')
    args = parser.parse_args()

    main(args.step,args.output_path,'%s.tar.gz'%(args.output_name))