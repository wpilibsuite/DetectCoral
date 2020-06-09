import os, shutil, fileinput, tarfile
import labels, sedModule, modularized_model_main

import subprocess #<< the goal is to get rid of the need for this

research_dir = '/tensorflow/models/research'

classes = labels.get()

sedModule.replaceWords('NUM_CLASSES',str(classes), "pipeline.config")

TRAIN_STEPS = 1000
BATCH_SIZE = 32

sedModule.replaceWords('BATCH_SIZE_PARAM',str(BATCH_SIZE), "pipeline.config")

shutil.copy('pipeline.config', '/tensorflow/models/research/learn/ckpt/pipeline.config')

shutil.rmtree('/tensorflow/models/research/learn/train', ignore_errors=True)
os.mkdir('/tensorflow/models/research/learn/train')

modularized_model_main.main(
    pipeline_config_path='/tensorflow/models/research/learn/ckpt/pipeline.config',
    model_dir='/tensorflow/models/research/learn/train',
    num_train_steps=TRAIN_STEPS)

#here we should write the class tags of 
# /opt/ml/input/data/training/Raw Data/meta.json to a labelmap file.
with open('labels.txt', 'w') as labelfile:
    labelfile.writelines(['0 powercell'])

print('\nconverting checkpoint to tflite')
subprocess.check_call("./convert_checkpoint_to_edgetpu_tflite.sh --checkpoint_num %s" % (str(TRAIN_STEPS)), shell=True)
shutil.copy('learn/models/output_tflite_graph.tflite', '/opt/ml/model/unoptimized.tflite')

print('\ncompiling model for edge TPU')
subprocess.check_call("edgetpu_compiler ./learn/models/output_tflite_graph.tflite -o /opt/ml/model/", shell=True)

shutil.copy('/opt/ml/input/data/training/map.pbtxt', '/opt/ml/model/map.pbtxt')

subprocess.call('tar -czf /opt/ml/model/model.tar.gz /opt/ml/model/output_tflite_graph_edgetpu.tflite /opt/ml/model/map.pbtxt /opt/ml/model/unoptimized.tflite', shell=True)

print('All done.')