# note that there is a problem with all 3 bigwig files for four hours treatment of A549 cells with dexamethasone
# this is the link to the bad dataset: https://www.encodeproject.org/experiments/ENCSR748MVX/
import numpy as np
import sys
import os
import deeptools.getScorePerBigWigBin as score_bw
from deeptools.correlation import Correlation
from os import listdir
from os.path import isfile, join
# from DNA.settings import BASE_DIR
import json
import requests
from os import path
import random

import os
import glob

labels_list = []
bw_files = []
bw_labels = []
np_array = None
listUnnested = []
BASE_DIR = '/usr/src/app/'
print('BASE_DIR')
print(BASE_DIR)
# BASE_DIR = os.path.join(BASE_DIR, 'januModule')

def process_labels_and_corr(input_files):
    # Use the Spearman correlation for comparison, it is less susceptible to
    # outliers than Pearson correlation
    method = 'spearman'

    # os.path.join(BASE_DIR,'/sites/svpython/pyconnectWdl/januModule/treatment-data/files/0h/R1.bigwig')
    os.system('pwd')
    os.system('ls -lat')
    # order of bw_files matter - it is vital that the bw_labels correspond to the bw_files element by element in the lists
    for i in range(len(input_files)):
        bw_files.append(input_files[i])

    print("************BW FILES ALERT*************")
    print(bw_files)
    # bw_files = ['1.bigwig', '2.bigwig', '3.bigwig']

    # os.chdir(BASE_DIR)
    # exp_folder = os.path.join(BASE_DIR,'/sites/svpython/pyconnectWdl/januModule/treatment-data/files/0h/R1.bigwig')
    # list_big_files = glob.glob('*.bigwig')
    # print("bigwig files found: " + str(list_big_files))
    '''
    for f_name in list_big_files:
        # bw_files.append(path.join(exp_folder, f_name))
        bw_files.append(f_name)
    '''
    print("bigwig files found/paths: " + str(bw_files))

    # Generate the local bigWig file paths and cell line labels

    bw_labels = ['1 - ENCFF075MCN', '2 - ENCFF231NTN', '3 - ENCFF415GFH']

    print("LABELS ALERT")
    print(bw_labels)

    # labels_list_final = []
    # listUnnested_final = []

    imagename, labels_list_final, listUnnested_final = get_labels_and_correlation(
        bw_files,
        # chrs_to_skip,
        method=method,
        fileset_name='A549 cells treated with 100 nM dexamethasone',
        labels=bw_labels,
        output_dir=BASE_DIR
    )

    print("labels list final")
    print(labels_list_final)
    print("list unnested final")
    print(listUnnested_final)

    return imagename, labels_list_final, listUnnested_final

def get_labels_and_correlation(
        bw_files,
        # chrs_to_skip,
        bin_size=10000,
        method='pearson',
        fileset_name='result',
        blacklist=None,
        labels=bw_labels,
        output_dir=BASE_DIR
):
    my_listUnnested = []
    # my_labels_list = []
    assert method in ('pearson', 'spearman'), 'Invalid correlation method'
    # Autogenerate labels from filename if not provided
    if not labels:
        labels = [filename.split('/')[-1].split('.')[0] for filename in bw_files]
    # Generate a name for the unique combination
    test_name = fileset_name + '_' + method
    if blacklist:
        blacklist_title = 'Blacklisted'
        test_name += '_blacklisted'
    else:
        blacklist_title = ''
    image_name = test_name + '.png'
    # Bin the bigwig data in 10kb increments
    num_reads_per_bin = score_bw.getScorePerBin(
        bw_files,
        bin_size,
        # chrsToSkip=chrs_to_skip,
        blackListFileName=blacklist
    )
    # Write to npz file
    print("right before npz")
    os.system('pwd')
    os.system('ls -lat')
    print('svo')
    print(output_dir)
    print(test_name)
    filename = output_dir + test_name + '.npz'
    print( filename )
    print('svo.. ')
    with open(filename, "wb") as f:
        np.savez_compressed(f, matrix=num_reads_per_bin, labels=labels )
    # Compute the correlations
    corr = Correlation( filename, method, labels=labels)
    np_array = corr.compute_correlation()
    print("ALERT CORR")
    print(np_array)

    listNested = np_array.tolist()

    def removeNestings(listNest):
        for i in listNest:
            if type(i) == list:
                print(str(i) + "is: " + str(type(i)))
                removeNestings(i)
                print(str(i) + "is after: " + str(type(i)))
            else:
                print(str(i) + "is finally " + str(type(i)))
                my_listUnnested.append(i)

    removeNestings(listNested)

    print("FINAL CORRELATION VALUES")
    print(my_listUnnested)

    with open("corrScores.txt", "w") as f:
        f.write(str(my_listUnnested))

    plot_title = '{}{} Correlation of {}'.format(
        blacklist_title,
        method.capitalize(),
        fileset_name
    )
    # Create a png file of correlation heatmap
    image_path = output_dir + image_name
    corr.plot_correlation(image_path, plot_title=plot_title)

    # return np_ar
    my_labels_list = labels
    return image_path, my_labels_list, my_listUnnested

def get_chips_generated_array(experimentName, corrList, chps_generated_labels_list):
    length_labels_list = len(chps_generated_labels_list)
    print(length_labels_list)

    # chps_generated_array = np.array([])
    chps_generated_array = []

    rowsNumber = length_labels_list
    colsNumber = length_labels_list

    labelRow = chps_generated_labels_list
    labelCol = chps_generated_labels_list

    for i in range(len(corrList)):
        for j in range(rowsNumber):
            x = j + 1
            for k in range(colsNumber):
                y = k + 1
                corrInterList = [x, y, corrList[i], experimentName, labelRow[j], labelCol[k]]
                if i != len(corrList) - 1:
                    i = i + 1
                print("corr inter list")
                print(corrInterList)
                # chps_generated_array = np.append(chps_generated_array, corrInterList)
                chps_generated_array.append(corrInterList)
                print("x value: " + str(x))
                print("y value: " + str(y))
                print("append")
                print(chps_generated_array)

                if x == rowsNumber and y == colsNumber:
                    break
            else:
                continue
            break
        else:
            continue
        break

    print(len(chps_generated_array))
    return chps_generated_array


def main(args):
    process_labels_and_corr(sys.argv[1:])

"""
info_svusers()
    bulk_fetch()
    bulk_add()
"""

"""
if __name__ == "__main__":
    main()
"""

if __name__ == '__main__':
    main(sys.argv[1:])

