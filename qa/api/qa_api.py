import sys
sys.path.append('../')
from es.es_model import ES_Model
from flask_restful import Resource
from model.order import order_by_word2vector

ES_INIT = False
INPUT_FILE = '../data/qa_scratch_seg.txt'
STOP_WORDS = '../data/stopwords.txt'
INDEX_NAME = 'qa_system'

es_model = ES_Model(INPUT_FILE, INDEX_NAME, STOP_WORDS, ES_INIT)
#根据用户输入的问题及前端传来的问题ID，检索出最相近的问题或该问题ID的子问题
class Questions(Resource):
    def get(self, question, id):
        es_result = es_model.get_topn_sims_q(str(question), id)
        result = order_by_word2vector(es_result, str(question))
        return result

#根据用户输入的问题，问题ID，精确匹配出回答
class Answer(Resource):
    def get(self, question, id):
        result = es_model.get_answer_by_id(str(question), id)
        return result

class QuestionsAndAnswers(Resource):
    def get(self, question):
        es_result = es_model.get_topn_sims_anwser(str(question))
        result = order_by_word2vector(es_result, question)
        return result

#用户追加专有字典接口
class UserWords(Resource):
    def put(self,word):
        try:
            with open('../data/userwords.txt','a+',encoding='utf-8') as f:
                f.write(word)
                f.write('\n')
        except Exception as e:
            return str(e),400
        return 'success',201
#用户追加停用词接口
class StopWords(Resource):
    def put(self,word):
        try:
            with open('../data/stopwords.txt','a+',encoding='utf-8') as f:
                f.write(word)
                f.write('\n')
        except Exception as e:
            return str(e),400
        return 'success',201





