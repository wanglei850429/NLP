from gensim.models.word2vec import LineSentence, Word2Vec
import jieba
from scipy.linalg import norm
import gensim
import numpy as np

import sys
sys.path.append('../')
from utils.utils import Utils


OUTFILE1 = '../data/yuliao.csv'
OUTFILE2 = '../data/yuliao.txt'
stop_words_file = '../data/stopwords.txt'
INFILE1 = '../data/new_kuaixue_qa.csv'
OUTFILE3 = '../word2vec/question.word2vec'

def preprocess_gen_1(input, output):
    foutput = open(output, 'w', encoding='utf-8')
    with open(input, "r", encoding='utf-8') as f:
        for line in f:
            sentence1 = line.rstrip().split('|')
            foutput.write(sentence1[1] +'\n')
    foutput.close()


def preprocess_gen_2(input, output, stopwords, max_limit=100):
    space = ' '
    i = 0
    f_txt = open(output, 'w', encoding='utf-8')
    f_csv = open(input, 'r', encoding='utf-8')
    for text in f_csv:
        words_list = [x for x in jieba.cut(text, cut_all=False) if x not in stopwords]
        f_txt.write(space.join(words_list))


def save_model(input, output):
    content = open(input, 'r', encoding='utf-8')
    model = Word2Vec(LineSentence(content), sg=0, size=64, window=5, min_count=5, workers=9)
    #model.wv.save(output)
    model.wv.save_word2vec_format(output, binary=True)
    #print(model.wv.vocab)
    
def generate_model(file, stop_words_file, model_file):
    stopwords = Utils.get_stop_words(stop_words_file,'utf-8')
    #preprocess_gen_1(file, OUTFILE1)
    preprocess_gen_2(OUTFILE1, OUTFILE2, stopwords, 1000000)
    save_model(OUTFILE2, model_file)

def load_model(model_file):
    model = gensim.models.KeyedVectors.load_word2vec_format(model_file, binary=True)
    return model

def vector_similarity(s1, s2, model):
    # 取停顿词
    stopwords = Utils.get_stop_words(stop_words_file, 'utf-8')
    def sentence_vector(s):
        #words = jieba.lcut(s)
        Utils.load_user_words()
        words = [x for x in jieba.cut(s, cut_all=False) if x not in stopwords]
        words = list(filter(lambda x:not x.isdigit(),words))
        words = [word.lower().strip() for word in words]
        v = np.zeros(64)
        for word in words:
            #print(word)
            if word not in model.wv.vocab:
                continue
            else:
                #print(v)
                v += model[word]
        v /= len(words)
        return v
    
    v1, v2 = sentence_vector(s1), sentence_vector(s2)
    #余弦相似度(Cosine Similarity)
    return np.dot(v1, v2) / (norm(v1) * norm(v2))
