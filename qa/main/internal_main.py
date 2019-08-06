#!/usr/bin/python
import sys
sys.path.append('../')
from preprocess import preprocess
#from es_model import *
from es import es_model
from utils.utils import Utils
from model import word2vect
import os
import time

LOAD_DATA = False
INDEX_NAME = 'qa'
PREPROCESS = False

GENERATE_VECT = True
TOPN = 20
org_input_file = '../data/kuaixue_org.csv'
input_file = '../data/kuaixue_p.csv'

stop_words_file = '../data/stopwords.txt'
my_vect_file = '../data/question.word2vec.bin'

if __name__ == "__main__":
    if PREPROCESS:
        preprocess.preprocess(org_input_file, input_file)

    if GENERATE_VECT:
        word2vect.generate_model(input_file,stop_words_file, my_vect_file)
        
    if LOAD_DATA:
        if  os.path.exists(input_file):
            es_mode = es_model.ES_Model(input_file, INDEX_NAME, stop_words_file ,True)
        else:
            print("Input file is not exist")
    else:
        #es_mode = es_model.ES_Model(input_file, INDEX_NAME, stop_words_file ,False)
        pass