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
import string
import random
from os import path
import random
from parse import *

uniq = ''.join(random.choices(string.ascii_letters + string.digits, k=16))

def create_download_folder(enc_link_name):
    # os.mkdir('/usr/src/app/files/' + uniq + '/' + enc_link_name)
    print("uniq id: " + uniq)
    print("link name: " + enc_link_name)
    print("download folder created")

def create_output_folder(enc_link_name):
    # os.mkdir('/usr/src/app/graphs/' + uniq + '/' + enc_link_name)
    print("output folder created")

def download_file(file_name, s3_url, enc_link_name):
    # os.mkdir('/usr/src/app/januModule/treatment-data/' + enc_link_name)
    # file_path = '/usr/src/app/files/' + uniq + '/' + str(file_name) + '.bigwig'
    file_path = file_name + '.bigwig'
    try:
        r = requests.get(s3_url, allow_redirects=True)
        # print('content-dispositiins')
        # print(r.headers.get('content-disposition'))
        with open(file_path, 'wb') as f:
            f.write(r.content)
        print("")
        print("")
    except Exception as error:
        print("error")
        print(error)
        # return
    # finally:
        # f.close()

# testing requests api for wdl script
def download_end():
    file_path = 'instructions'
    s3_url = 'http://25.io/toau/audio/sample.txt'
    try:
        r = requests.get(s3_url, allow_redirects=True)
        # print('content-dispositiins')
        # print(r.headers.get('content-disposition'))
        with open(file_path, 'wb') as f:
            f.write(r.content)
        print("end file downloaded successfully")
    except Exception as error:
        print("error - end file not downloaded")
        print(error)


def download_all_files(downloadMeta):
    g = open(downloadMeta, "r")
    urls = g.readline().split(' ')
    fileNames = g.readline().split(' ')
    g.close()
    '''
    for i in urls:
        if i == '[backslash n]':
            urls.remove('[backslash n]')
    for j in fileNames:
        if j == '':
            fileNames.remove('')
    '''
    print(urls)
    print(fileNames)

    lenFiles = len(fileNames)
    lenUrls = len(urls)

    for i, j in zip(range(lenFiles), range(lenUrls)):
        # print("i: " + str(fileNames[i]))
        # print("j: " + str(urls[j]))
        urlCheck = urls[j].split(':')[0]
        if urlCheck == 'https':
            download_file(fileNames[i], urls[j], link_name)
            print("downloaded %s" % fileNames[i])

'''
dev main below

def main(args):
    # sort_json(sys.argv[1])
    create_download_folder(link_name)
    # download_all_files(sys.argv[2])
    create_output_folder(link_name)
'''

# wdl main
def main(args):
    create_download_folder(link_name)
    # download_file("ENCFF075MCN", "https://encode-public.s3.amazonaws.com/2018/03/06/c2206997-d760-4f5a-a403-175e7779e2ed/ENCFF075MCN.bigWig", link_name)
    download_all_files(sys.argv[1])
    # download_end()
    create_output_folder(link_name)

if __name__ == '__main__':
    main(sys.argv[1:])

