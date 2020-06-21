#adapted from program by Tom Runia

import shutil
import numpy as np
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from tensorboard.backend.event_processing.event_accumulator import EventAccumulator
accumulator = False

def retrieve_tags():
    if accumulator:
        return [i.encode('ascii') for i in accumulator.Tags()['scalars']]
    else:
        return []

def plot_tensorflow_log(log, tag1):
    global accumulator

    plt.style.use('dark_background')

    tf_size_guidance = {
        'compressedHistograms': 10,
        'images': 1,
        'scalars': 1000,
        'histograms': 1
    }
    
    if len(log) != 0:
        accumulator = EventAccumulator(log[0], tf_size_guidance)
        accumulator.Reload()
        if tag1 in retrieve_tags():
            data1 = accumulator.Scalars(tag1)
                
            steps = len(data1)
            x = np.arange(steps)
            y = np.zeros([steps, 2])

            for i in xrange(steps):
                y[i, 0] = data1[i][2]
                # y[i, 1] = data2[i][2]
            plt.plot(x, y[:,0], color='C1', label=tag1, linewidth=3)

            plt.xlabel("Steps")
            legend_elements = [Line2D([0], [0], color='C1', lw=4, label=tag1)]
            plt.legend(handles=legend_elements, loc='upper right', frameon=True)

            plt.savefig('/tensorflow/models/research/gui/static/plott.png')

            plt.clf()
            plt.cla()
            plt.close()
            return
            
    shutil.copyfile('gui/static/placeholder.png','gui/static/plott.png')


