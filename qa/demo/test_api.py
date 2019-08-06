#!/usr/bin/python
import sys
sys.path.append('../')

from api.qa_api import QuestionsAndAnswers

if __name__ == "__main__":
    qa = QuestionsAndAnswers()
    qa.get("offcie2010 下载")