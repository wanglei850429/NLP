import sys
sys.path.append('../')

from model.word2vect import load_model, vector_similarity
from utils.utils import Utils

MODEL_FILE = '../data/question.word2vec.bin'
DEBUG = False
word_vector_model = load_model(MODEL_FILE)
def order_by_word2vector(es_result, question,n=5):
    if DEBUG:
        for i in es_result:
            print('---------------------------------------------------------')
            print('问题: %s' % (i['_source']['question']))
            print('答案:%s' % (i['_source']['anwser']))

    #根据已经学习好的词向量，对结果进行重排序
    order_result = []
    for key,i in es_result['result2'].items():
        record = []
        if word_vector_model:
            v = vector_similarity(question, i['title'], word_vector_model)
            record.append(i['index'])
            record.append(i['title'])
            record.append(v)
            order_result.append(record)
        else:
            break
    if len(order_result) > 0 :
        sorted(order_result,key=lambda x:x[2],reverse=True)
        
    if DEBUG:
        print('\n---------------------------------------------------------')
        print('词向量重排后的结果：')
        for i in order_result:
            print('---------------------------------------------------------')
            print('问题: %s' % (i[0]))
            print('答案:%s' % (i[1]))
            print('相似度:%f' % (i[2]))
    return order_result[:n]