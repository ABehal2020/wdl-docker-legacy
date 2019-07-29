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
import numpy

link_name = ''

def sort_json(file_path):
    # file_path = './ENCSR193NSH.json'
    i = 1
    global link_name
    link_name = 'exp' + str(i)

    def nameDir():
        i = i + 1
        link_name = 'exp' + str(i)

    if path.exists(link_name) == True:
        nameDir()

    try:
        with open(file_path, 'r') as json_metadata:
            # data is dictionary object; json.load converts from JSON to dictionary format
            data = json.load(json_metadata)
    except Exception as e:
        print(e)
    finally:
        json_metadata.close()

    files = data['files']
    allFiles = dict()

    for afile in files:
        label = afile['accession']
        s3_location = afile['cloud_metadata']['url']
        accession_dict = dict()
        accession_dict['label'] = label
        accession_dict['s3_location'] = s3_location
        file_name = accession_dict['s3_location'].split('/')[-1]
        accession_dict['file_name'] = file_name
        ext = file_name.split('.')[-1]
        accession_dict['file_ext'] = ext
        accession_dict['isBigWig'] = (ext == 'bigWig')
        allFiles[label] = accession_dict

    print(allFiles)

    return get_BigWigFiles(allFiles)

def get_BigWigFiles(filesList):
    urls = []
    fileNames = []
    for k in list(filesList.keys()):
        if filesList[k]['isBigWig'] == True:
            urls.append(filesList[k]['s3_location'])
            fileNames.append(filesList[k]['label'])

    with open('%s.txt' % link_name, "w") as f:
        for i in urls:
            print(i)
            f.write('%s\n' % i)

    '''
    print(x)
    with open('download-meta.txt', "w") as f:
        for i, j in zip(urls, fileNames):
            f.write('%s\n' % i)
            f.write('%s\n' % j)
    '''

    with open('download-meta.txt', "w") as f:
        for i in urls:
            f.write('%s ' % i)
            continue
        f.write('\n')
        for j in fileNames:
            f.write('%s ' % j)

    print("link name: " + link_name)

    return fileNames, urls, link_name

def main(args):
    sort_json(sys.argv[1])

if __name__ == '__main__':
    main(sys.argv[1:])