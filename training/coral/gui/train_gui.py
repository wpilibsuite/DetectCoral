  
from flask import Flask, render_template, redirect, url_for, request
import subprocess, glob, argparse, os, re, shutil
import log_loader
app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

#the available models/link maps etc should soon be in a container-wide json or something
pretrainedmodels=['mobilenet_v2_ssd']
reserve_dataset_path = '/opt/ml/input/data/training/full_data.tar'
mountpath = '/opt/ml/model/'
trainjob = None
exportjob = None

def list_datasets():
    datasets = [reserve_dataset_path]
    datasets += glob.glob(os.path.join(mountpath,'*.tar'))
    return datasets

@app.route("/", methods=['GET', 'POST'])
@app.route("/home", methods=['GET', 'POST'])
def home():
    return render_template('prepare.html',pretrainedmodels=pretrainedmodels,datasets=list_datasets())

@app.route("/training", methods=['GET', 'POST'])
def train():
    global trainjob, epochs, eval_period, current_epoch, output_name, current_epoch, exportjob

    if request.method == "POST":
        if 'name' in request.form and trainjob is None:
            with open('status.txt','w') as status:
                status.write('starting the train job')

            if 'tboard' in request.form:
                subprocess.Popen(['tensorboard','--logdir','learn/train'])

            shutil.rmtree('learn/train', ignore_errors=True)
            shutil.copyfile('gui/static/placeholder.png','gui/static/plott.png')

            current_epoch = 0
            exportjob = None
            epochs = int(request.form['train_steps'])
            output_name = request.form['name']
            eval_period = int(request.form['eval_period'])

            trainjob = subprocess.Popen(['python','train.py',
                '-ptm',request.form['pretrainedmodel'],
                '-b',request.form['batch_size'],
                '-dsp',request.form['dataset'],
                '-ep',request.form['eval_period'],
                '-n',request.form['name'],
                '-s',request.form['train_steps']])
            
        if 'finish' in request.form and exportjob is None:
            trainjob.terminate()
            trainjob = None
            exportjob = subprocess.Popen(['python','export.py','-s',str(current_epoch),'-n',output_name,'-o',mountpath])
            with open('status.txt','w') as status:
                status.write('stopping the train job, starting the export to the mounted directory.')

        with open('status.txt', 'r') as status:
            state = status.readlines()

        log = glob.glob('learn/train/eval_0/*')
        if len(log) != 0:
            log = log[0]
            log_loader.plot_tensorflow_log(log)

        ckpts = glob.glob('learn/train/model.ckpt-*.meta')
        if len(ckpts) != 0:
            current_epoch = max([int(re.split('learn/train/model.ckpt-|.meta',ckpt)[1]) for ckpt in ckpts])
        
        state.append('epoch %s out of %s'%(current_epoch, epochs))

        return render_template('training.html', content=state)

    else:
        return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=5000)
