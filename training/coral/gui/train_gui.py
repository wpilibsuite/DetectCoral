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
ckptpath = 'learn/ckpt/'
mountpath = '/opt/ml/model/'
model_output = join(mountpath,'finished-models')
trainjob = {'process' : None, 'tensorboard' : None}
exportjob = {'process' : None}
tag_list = []
current_epoch = 0
selected_data = 'none'
lightmode = False

for directory in ['checkpoints','datasets','finished-models']:
    if not os.path.exists(join(mountpath,directory)):
        os.mkdir(join(mountpath,directory))

@app.route("/", methods=['GET', 'POST'])
@app.route("/home", methods=['GET', 'POST'])
def home():
    global trainjob, exportjob, current_epoch, lightmode

    datasets = glob.glob(join(mountpath,'datasets/*.tar'))
    datasets.append(reserve_dataset_path)

    ckpts = os.listdir(join(mountpath,'checkpoints'))
    ckpts += [dir for dir in os.listdir(ckptpath) if os.path.isdir(join(ckptpath,dir))]

    inprogress = False
    if trainjob['process'] or exportjob['process']:
        inprogress = True

    if request.method == 'POST':
        
        if 'switchcolor' in request.form:
            lightmode = [True,False][lightmode] #toggle
            return redirect(url_for('home'))

        with open('status.txt','w') as status:
            status.write('starting the train job')

        if trainjob['tensorboard']:
            if trainjob['tensorboard'].poll is None:
                trainjob['tensorboard'].terminate()
        if trainjob['process']:
            if trainjob['process'].poll() is None:
                trainjob['process'].terminate()
                
        trainjob = {
            'process' : None,
            'checkpoint' : request.form['pretrainedmodel'],
            'dataset' : request.form['dataset'],
            'epochs' : request.form['train_steps'],
            'batch_size' : request.form['batch_size'],
            'eval_period' : request.form['eval_period'],
            'name' : request.form['name'],
            'tensorboard' : None
        }
        
        if trainjob['checkpoint'] not in os.listdir(ckptpath):
            shutil.copytree(join(mountpath,'checkpoints',trainjob['checkpoint']), join(ckptpath,trainjob['checkpoint']))

        if 'tboard' in request.form:
            trainjob['tensorboard'] = subprocess.Popen(['tensorboard','--logdir','learn/train'])

        shutil.rmtree('learn/train/', ignore_errors=True)
        os.mkdir('learn/train/')
        exportjob = {'process' : None}
        trainjob['process'] = subprocess.Popen(['python','train.py',
            '-ptm', trainjob['checkpoint'],
            '-b', trainjob['batch_size'],
            '-dsp', trainjob['dataset'],
            '-ep', trainjob['eval_period'],
            '-n', trainjob['name'],
            '-s', trainjob['epochs']])

        return redirect(url_for('train'))

    return render_template('prepare.html',pretrainedmodels=ckpts,datasets=datasets,lightmode=lightmode, inprogress=inprogress)

@app.route("/training", methods=['GET', 'POST'])
def train():
    global trainjob, exportjob, current_epoch, tag_list, selected_data, lightmode

    if request.method == "POST":

        if 'switchcolor' in request.form:
            lightmode = [True,False][lightmode] #toggle

        if 'finish' in request.form and exportjob['process'] is None:
            trainjob['process'].terminate()
            exportjob['process'] = subprocess.Popen(['python','export.py',
                '-s',str(current_epoch),
                '-n',trainjob['name'],
                '-o',model_output])
            trainjob['process'] = None
            with open('status.txt','w') as status:
                status.write('stopping the train job, starting the export to the mounted directory.')

        if 'graphselect' in request.form:
            selected_data = request.form['graphselect']

        if 'copy' in request.form:
            copy_checkpoint(current_epoch, trainjob['name'])

    with open('status.txt', 'r') as status:
        state = status.readlines()

    if trainjob['process'] is not None:

        ckpts = glob.glob('learn/train/model.ckpt-*.meta')
        if len(ckpts) != 0:
            current_epoch = max([int(re.split('learn/train/model.ckpt-|.meta',ckpt)[1]) for ckpt in ckpts])
        else:
            current_epoch = 0

        log = glob.glob('learn/train/eval_0/*')
        log_loader.plot_tensorflow_log(log, selected_data, lightmode)
        tag_list = log_loader.retrieve_tags()

    state.append('epoch %s out of %s'%(current_epoch, int(trainjob['epochs'])))
    return render_template('training.html', content=state, data=tag_list, selected_data=selected_data, lightmode=lightmode)

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=5000)
