  
from flask import Flask, render_template, redirect, url_for, request
import subprocess, glob, argparse, os
app = Flask(__name__)

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
    if request.method == "POST":
        if 'name' in request.form:
            with open('status.txt','w') as status:
                status.write('starting the train job')

            subprocess.Popen(['python','train.py',
                            '-n',request.form['name'],
                            '-s',request.form['train_steps'],
                            '-b',request.form['batch_size'],
                            '-ptm',request.form['pretrainedmodel'],
                            '-dsp',request.form['dataset']])

        with open('status.txt', 'r') as status:
            state = status.readlines()[0]

        return render_template('training.html', content=state)

    else:
        return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=5000)
