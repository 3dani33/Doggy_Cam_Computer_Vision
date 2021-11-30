"""
Evaluate the CSV File generated by `run_algorithm.py`
read csv file and calculates mean over all annotated 1's and mean over all annotated 0's"""

import numpy as np
import os
from numpy.core.fromnumeric import size
import plac
import matplotlib.pyplot as plt


@plac.pos('file', 'the CSV-File to be analized')

def calculate_means(file):


    filename = os.path.basename(file)
    print('Analyzing file: {}'.format(filename))

    array = np.loadtxt(open(file, 'rb'), delimiter=',')

    norm = array[:,1]/max(array[:,1])

    truecounter = 0
    truearray = []
    truesum = 0
    emptytrue = 0

    falsecounter = 0
    falsearray = []
    falsesum = 0
    emptyfalse = 0
    
    mintrue = array[0,1]
    j = 0
    while(True):
        mintrue = array[j,1]
        if(array[j,1] != 0):
            break
        j +=1
        
    for i in range(len(array)):
        if(array[i,1] == 0):
            if(array[i,0] == 1 ):
                emptytrue += 1
            elif(array[i,0] == 0):
                emptyfalse += 1
        elif(array[i,0]) == 1:
            truecounter += 1
            truearray = np.insert(truearray, len(truearray), norm[i])
            truesum += array[i,1]
            if(array[i,1]<mintrue):
                mintrue = array[i,1]
        elif(array[i,0]) == 0:
            falsecounter += 1
            falsearray = np.insert(falsearray, len(falsearray), norm[i])
            falsesum += array[i,1]

    print('{} frames skipped due to empty intensity. {} were active frames, {} were passive frames'.format(len(array)+emptyfalse+emptytrue, emptytrue, emptyfalse))

    print('active mean: {}, passive mean: {}'.format(truesum/truecounter, falsesum/falsecounter))

    print('the middle-threshold would be at {}'.format(truesum/truecounter - falsesum/falsecounter))

    print('minimal active value: {}'.format(mintrue))

    print('Printing Histograms...')


    f, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(20,20))

    ax1.hist(np.delete(array.T,0,0).T)
    ax1.set_title('Histogram of intensities')
    ax1.set_ylabel('number of frames')
    ax1.set_xlabel('Intensity')
    
    ax2.hist(norm)
    ax2.set_xlabel('normalized intensities')
    ax2.set_ylabel('number of frames')
    ax2.set_title('normalized histogram')

    ax3.hist(falsearray)
    ax3.set_title('Histogram of alle frames annotated as \'no movement\'')
    ax3.set_xlabel('normalized intensities')
    ax3.set_ylabel('number of frames')

    ax4.hist(falsearray, label='No moevement')
    ax4.hist(truearray, label='Movement')
    ax4.set_title('Overlayed with the Histogram dor all frames annotated as \'movement\'')
    ax4.set_xlabel('normalized intensities')
    ax4.set_ylabel('number of frames')
    ax4.legend()

    plt.show()


if __name__ == '__main__':
	plac.call(calculate_means)