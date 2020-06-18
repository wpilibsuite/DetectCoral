  
from flask import Flask, render_template, redirect, url_for, request
import subprocess, glob, argparse, os
import log_loader
app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

#the available models/link maps etc should soon be in a container-wide json or something
pretrainedmodels=['mobilenet_v2_ssd']
reserve_dataset_path = '/opt/ml/input/data/training/full_data.tar'
mountpath = '/opt/ml/model/'

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
    global trainjob, epochs, eval_period, current_eval

    if request.method == "POST":
        if 'name' in request.form:
            with open('status.txt','w') as status:
                status.write('starting the train job')

            if 'tboard' in request.form:
                subprocess.Popen(['tensorboard','--logdir','learn/train'])

            epochs, eval_period, current_eval = request.form['train_steps'], request.form['eval_period'], 0

            trainjob = subprocess.Popen(['python','train.py',
                            '-n',request.form['name'],
                            '-s',request.form['train_steps'],
                            '-b',request.form['batch_size'],
                            '-ptm',request.form['pretrainedmodel'],
                            '-dsp',request.form['dataset'],
                            '-ep',request.form['eval_period']])

        # if 'finished' in request.form:
        #     trainjob.terminate()
            

        with open('status.txt', 'r') as status:
            state = status.readlines()

        log = glob.glob('learn/train/eval_0/*')
        if len(log) != 0:
            log = log[0]
            current_eval = log_loader.plot_tensorflow_log(log)
        current_epoch = int(current_eval)*int(eval_period)
        state.append('epoch %s out of %s'%(current_epoch, epochs))

        return render_template('training.html', content=state)

    else:
        return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=5000)
