  
from flask import Flask, render_template, redirect, url_for, request
import subprocess
app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
@app.route("/home", methods=['GET', 'POST'])
def home():
    return render_template('prepare.html')

@app.route("/training", methods=['GET', 'POST'])
def train():
    if request.method == "POST":
        if 'name' in request.form:
            with open('status.txt','w') as status:
                status.write('starting the train job')

            subprocess.Popen(['python','train.py',
                            '-n',request.form['name'],
                            '-s',request.form['train_steps'],
                            '-b',request.form['batch_size']])

        with open('status.txt', 'r') as status:
            lines = status.readlines()
            state = lines[0]
        return render_template('training.html', content=state)

    else:
        return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=5000)
