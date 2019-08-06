#!/usr/bin/python
from flask import Flask,make_response
from flask_restful import reqparse, Api
import sys
import os
import time
sys.path.append('../')
from api.qa_api import Questions,Answer,QuestionsAndAnswers,UserWords,StopWords

app = Flask(__name__)
#供elasticsearch ik插件监听调用，如用户更新了停用词表，ES监听并调用此接口完成热更新
@app.route("/update/stop_word")
def updateStopWord():
    resp = make_response()
    resp.headers['Last-Modified'] = str(time.ctime(os.path.getmtime('../data/stopwords.txt')))
    resp.headers['ETag'] = str(time.ctime(os.path.getmtime('../data/stopwords.txt')))
    resp.headers['content_type'] = 'text/plain;charset=utf-8'
    stopwords=''
    if os.path.exists('../data/stopwords.txt'):
        with open('../data/stopwords.txt', 'r', encoding='utf-8') as f:
            stopwords = f.read()
    resp.response = stopwords
    return resp
#供elasticsearch ik插件监听调用，如用户更新了专有词表，ES监听并调用此接口完成热更新
@app.route("/update/user_word")
def updateUserWord():
    resp = make_response()
    resp.headers['Last-Modified'] = str(time.ctime(os.path.getmtime('../data/userwords.txt')))
    resp.headers['ETag'] = str(time.ctime(os.path.getmtime('../data/userwords.txt')))
    resp.headers['content_type'] = 'text/plain;charset=utf-8'
    userwords=''
    if os.path.exists('../data/userwords.txt'):
        with open('../data/userwords.txt', 'r', encoding='utf-8') as f:
            userwords = f.read()
    resp.response = userwords
    return resp

if __name__ == '__main__':
    api = Api(app)
    api.add_resource(Questions, '/QA/q/<question>/<id>')
    api.add_resource(Answer, '/QA/a/<question>/<id>')
    api.add_resource(UserWords, '/QA/user_word/<word>')
    api.add_resource(StopWords, '/QA/stop_word/<word>')
    # api.add_resource(QuestionsAndAnswers, '/QA/a/<question>')

    parser = reqparse.RequestParser()
    parser.add_argument('arg', type=str)
    
    app.config.update(RESTFUL_JSON=dict(ensure_ascii=False))
    app.run(debug=True)