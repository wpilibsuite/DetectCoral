import matplotlib as mpl
mpl.use('Agg')
import log_loader
from flask import Flask, render_template, redirect, url_for, request
import subprocess, glob, argparse, os, re, shutil, datetime
from export import copy_checkpoint
from os.path import join
app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

#the available models/link maps etc should soon be in a container-wide json or something
reserve_dataset_path = '/opt/ml/input/data/training/full_data.tar'
mountpath = '/opt/ml/model/'
model_output = join(mountpath,'finished-models')
trainjob = None
exportjob = None
tag_list = []
current_epoch = 0
selected_data = 'none'

for directory in ['checkpoints','datasets','finished-models']:
    if not os.path.exists(join(mountpath,directory)):
        os.mkdir(join(mountpath,directory))

@app.route("/", methods=['GET', 'POST'])
@app.route("/home", methods=['GET', 'POST'])
def home():

    datasets = glob.glob(join(mountpath,'datasets/*.tar'))
    datasets.append(reserve_dataset_path)

    ckpts = os.listdir(join(mountpath,'checkpoints'))
    ckpts += [dir for dir in os.listdir('learn/ckpt/') if os.path.isdir('learn/ckpt/%s'%(dir))]

    return render_template('prepare.html',pretrainedmodels=ckpts,datasets=datasets)

@app.route("/training", methods=['GET', 'POST'])
def train():
    global trainjob, epochs, eval_period, current_epoch, output_name, current_epoch, exportjob, tag_list, selected_data, pretrainedmodels

    if request.method == "POST":
        if 'name' in request.form and trainjob is None:

            current_epoch = 0
            exportjob = None
            epochs = int(request.form['train_steps'])
            output_name = request.form['name']
            eval_period = int(request.form['eval_period'])
            checkpoint = request.form['pretrainedmodel']

            if checkpoint not in os.listdir('learn/ckpt/'):
                if checkpoint not in os.listdir(join(mountpath,'checkpoints')):
                    return redirect(url_for('home'))
                shutil.copytree(join(mountpath,'checkpoints',checkpoint), 'learn/ckpt/%s'%(checkpoint))

            with open('status.txt','w') as status:
                status.write('starting the train job')

            if 'tboard' in request.form:
                subprocess.Popen(['tensorboard','--logdir','learn/train'])

            shutil.rmtree('learn/train', ignore_errors=True)
            shutil.copyfile('gui/static/placeholder.png','gui/static/plott.png')

            trainjob = subprocess.Popen(['python','train.py',
                '-ptm', checkpoint,
                '-b',request.form['batch_size'],
                '-dsp',request.form['dataset'],
                '-ep',request.form['eval_period'],
                '-n',request.form['name'],
                '-s',request.form['train_steps']])

        if 'finish' in request.form and exportjob is None:
            trainjob.terminate()
            trainjob = None
            exportjob = subprocess.Popen(['python','export.py','-s',str(current_epoch),'-n',output_name,'-o',model_output])
            with open('status.txt','w') as status:
                status.write('stopping the train job, starting the export to the mounted directory.')

        if 'graphselect' in request.form:
            selected_data = request.form['graphselect']

        if 'copy' in request.form:
            copy_checkpoint(current_epoch, output_name)

    if trainjob:
        with open('status.txt', 'r') as status:
            state = status.readlines()

        log = glob.glob('learn/train/eval_0/*')
        if len(log) != 0:
            log_loader.plot_tensorflow_log(log[0], selected_data)
            tag_list = log_loader.retrieve_tags()
        ckpts = glob.glob('learn/train/model.ckpt-*.meta')
        if len(ckpts) != 0:
            current_epoch = max([int(re.split('learn/train/model.ckpt-|.meta',ckpt)[1]) for ckpt in ckpts])

    elif exportjob:
        with open('status.txt', 'r') as status:
            state = status.readlines()

    state.append('epoch %s out of %s'%(current_epoch, epochs))
    return render_template('training.html', content=state, data=tag_list, selected_data=selected_data)

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=5000)
