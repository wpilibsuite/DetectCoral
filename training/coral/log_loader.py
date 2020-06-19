#adapted from program by Tom Runia

import shutil
import numpy as np
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from tensorboard.backend.event_processing.event_accumulator import EventAccumulator

def plot_tensorflow_log(path):

    plt.style.use('dark_background')

    tf_size_guidance = {
        'compressedHistograms': 10,
        'images': 1,
        'scalars': 1000,
        'histograms': 1
    }

    accumulator = EventAccumulator(path, tf_size_guidance)
    accumulator.Reload()

    try:
        precision = accumulator.Scalars('DetectionBoxes_Precision/mAP')
        recall = accumulator.Scalars('DetectionBoxes_Recall/AR@100')
    except:
        shutil.copyfile('gui/static/placeholder.png','gui/static/plott.png')
        return

    steps = len(precision)

    x = np.arange(steps)
    y = np.zeros([steps, 2])

    for i in xrange(steps):
        y[i, 0] = precision[i][2]
        y[i, 1] = recall[i][2]

    plt.plot(x, y[:,0], color='C1', label='precision', linewidth=3)
    plt.plot(x, y[:,1], color='C3',label='recall', linewidth=3)

    plt.xlabel("Steps")

    legend_elements = [Line2D([0], [0], color='C1', lw=4, label='precision'),
                       Line2D([0], [0], color='C3', lw=4, label='recall')]

    plt.legend(handles=legend_elements, loc='upper right', frameon=True)
    plt.savefig('/tensorflow/models/research/gui/static/plott.png')
