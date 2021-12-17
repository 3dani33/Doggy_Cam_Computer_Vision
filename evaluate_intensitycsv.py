"""
Evaluate the CSV File generated by `run_algorithm.py`
read csv file and calculates mean over all annotated 1's and mean over all annotated 0's"""

import numpy as np
import os
from numpy.core.fromnumeric import size
import plac
import matplotlib.pyplot as plt
import file_handler


@plac.pos('file', 'the CSV-File to be analized')
@plac.opt('algorithm', 'Algorithm name, for example dummy_v1', type=str)

def calculate_means(file, algorithm):


    filename = os.path.basename(file)
    print('Analyzing file: {}'.format(filename))

    if(algorithm):
        print('loading algorithm data...')
        algorithm_files, video_files = file_handler.scan_algortihm_files(algorithm)
        algorithm_data = file_handler.load_algorithm_data(algorithm_files)
        

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
    
    if(algorithm):
        ref_array = np.zeros(len(array))
        for i in range(len(algorithm_data[0]['result'])):
            if(array[i,0] > algorithm_data[0]['result'][i]):
                ref_array[i] = -1
            elif(algorithm_data[0]['result'][i] > array[i,0]):
                ref_array[i] = 1
    

    print('{} frames skipped due to empty intensity. {} were active frames, {} were passive frames'.format(len(array)+emptyfalse+emptytrue, emptytrue, emptyfalse))

    print('active mean: {}, passive mean: {}'.format(truesum/truecounter, falsesum/falsecounter))

    print('the middle-threshold would be at {}'.format(truesum/truecounter - falsesum/falsecounter))

    print('minimal active value: {}'.format(mintrue))

    print('Printing Histograms...')


    f, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(20,20))

    ax1.hist(np.delete(array.T,0,0).T,log=True, bins=100)
    ax1.set_title('Histogram of intensities')
    ax1.set_ylabel('number of frames')
    ax1.set_xlabel('Intensity')
    
    ax2.hist(norm, log=True, bins=100)
    ax2.set_xlabel('normalized intensities')
    ax2.set_ylabel('number of frames')
    ax2.set_title('normalized histogram')

    ax3.hist(falsearray,log=True, bins=100)
    ax3.set_title('Histogram of alle frames annotated as \'no movement\'')
    ax3.set_xlabel('normalized intensities')
    ax3.set_ylabel('number of frames')

    
    ax4.hist(falsearray, bins=100, log=True, label='No moevement')
    ax4.hist(truearray, bins=100, log=True, label='Movement')
    
    ax4.set_title('Overlayed with the Histogram dor all frames annotated as \'movement\'')
    ax4.set_xlabel('normalized intensities')
    ax4.set_ylabel('number of frames')
    ax4.legend()

    plt.show()

    
    if(algorithm):
        plt.figure(figsize=(20,20))
        plt.plot(array[:,0], label='Annotation')
        plt.plot(algorithm_data[0]['result'], label='Algorithm result')
        plt.ylim([0,10])
        plt.xlabel('Framenumber')
        plt.ylabel('Movement')
        plt.legend(loc='upper right')

        plt.show()

        plt.figure(figsize=(20,20))
        plt.plot(ref_array)
        plt.xlabel('Framenumber')
        plt.title('False-positives and False-negatives \n\n 1 = False-positive, -1 = False-negative')

        plt.show()


if __name__ == '__main__':
	plac.call(calculate_means)