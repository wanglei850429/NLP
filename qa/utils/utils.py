import gensim
import jieba
import os

class Utils():
    user_dict_modify_time=None
    stop_word_modify_time=None
    stopwords = []
    @classmethod
    def load_baidubaike_model(cls):
        #词向量：https://pan.baidu.com/s/1ff-SdH9YWURDtsdIZ3iaYQ，提取码：56ly
        model_file = './word2vec/news_12g_baidubaike_20g_novel_90g_embedding_64.bin'
        model = gensim.models.KeyedVectors.load_word2vec_format(model_file, binary=True)
        return model

    @classmethod
    def get_stop_words(cls,file='../data/stopwords.txt', encoding='utf-8'):
        if cls.stop_word_modify_time != os.path.getmtime(file):
            cls.stop_word_modify_time = os.path.getmtime(file)
            cls.stopwords=[]
            with open(file,'r',encoding=encoding) as fp:
                for line in fp.readlines():
                    cls.stopwords.append(line.strip())
                return cls.stopwords
        else:
            return cls.stopwords

    @classmethod
    def load_user_words(cls,file='../data/userwords.txt', encoding='utf-8'):
        if cls.user_dict_modify_time != os.path.getmtime(file):
            jieba.load_userdict(file)
            cls.user_dict_modify_time = os.path.getmtime(file)

    @classmethod
    def take_third(cls,elem):
        return elem[2]

