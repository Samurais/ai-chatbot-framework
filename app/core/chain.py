#!/usr/bin/env python
# -*- coding: utf-8 -*-
#===============================================================================
#
# Copyright (c) 2017 <> All Rights Reserved
#
#
# File: /Users/hain/ai/ai-chatbot-framework/app/core/chain.py
# Author: Hai Liang Wang
# Date: 2018-01-24:14:01:29
#
#===============================================================================

"""
   
"""
from __future__ import print_function
from __future__ import division

__copyright__ = "Copyright (c) 2017 . All Rights Reserved"
__author__    = "Hai Liang Wang"
__date__      = "2018-01-24:14:01:29"


import os
import sys
curdir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(curdir)
sys.path.append(os.path.join(curdir, os.path.pardir, os.path.pardir))

if sys.version_info[0] < 3:
    reload(sys)
    sys.setdefaultencoding("utf-8")
    # raise "Must be using Python 3"

import pycrfsuite
import sequenceLabeler
from nltk import word_tokenize
from app.core.nlp import posTagger

'''
load story json
'''
import json
STORY_OBJECT_FILE = os.path.join(curdir, "data.json")
STORY_OBJECT = dict()
def _load_story_json():
    global STORY_OBJECT
    with open(STORY_OBJECT_FILE, "r") as fin:
        STORY_OBJECT = json.loads(fin.read())
        print(">> loaded story json ...")
_load_story_json()

assert "_id" in STORY_OBJECT, "_id not found"
assert "storyName" in STORY_OBJECT, ""
assert "labeledSentences" in STORY_OBJECT, "labeledSentences not found"
assert "intentName" in STORY_OBJECT, "intentName not found"
assert "parameters" in STORY_OBJECT, "parameters not found"

id = STORY_OBJECT["_id"]
storyName = STORY_OBJECT["storyName"]
labeledSentences = STORY_OBJECT["labeledSentences"]
intentName = STORY_OBJECT["intentName"]
parameters = STORY_OBJECT["parameters"]
model_file = '%s/model_files/sequenceLabeler.%s.model' % (os.path.join(curdir, os.path.pardir, os.path.pardir), id)


import unittest

# run testcase: python /Users/hain/ai/ai-chatbot-framework/app/core/chain.py Test.testExample
class Test(unittest.TestCase):
    '''
    
    '''
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_load_story_json(self):
        print("test_load_story_json")
        for x in STORY_OBJECT:
            print("key: %s" % x)

    def test_sequenceLabeler_predict(self):
        print("test_sequenceLabeler_predict")
        global id
        global model_file
        sentence = "I want to book a cab from Beijing"
        tokenizedSentence = word_tokenize(sentence)
        taggedToken = posTagger(sentence)
        tagger = pycrfsuite.Tagger()
        tagger.open(model_file)
        predictedLabels = tagger.tag(sequenceLabeler.sentToFeatures(taggedToken))
        extractedEntities = sequenceLabeler.extractEntities(
            zip(tokenizedSentence, predictedLabels))
        print("extractedEntities:")
        print(extractedEntities)

    def test_sequenceLabeler_train(self):
        print("test_train_model")
        print("storyName: %s" % storyName)
        global labeledSentences
        global model_file

        trainSentences = []
        for item in labeledSentences:
            trainSentences.append(item["data"])

        features = [sequenceLabeler.sentToFeatures(s) for s in trainSentences]
        labels = [sequenceLabeler.sentToLabels(s) for s in trainSentences]

        trainer = pycrfsuite.Trainer(verbose=False)
        for xseq, yseq in zip(features, labels):
            trainer.append(xseq, yseq)
            print("Trainer \n >> xseq: %s \n >> yseq: %s" % (xseq, yseq))
            print("*" * 20)

        trainer.set_params({
            'c1': 1.0,  # coefficient for L1 penalty
            'c2': 1e-3,  # coefficient for L2 penalty
            'max_iterations': 50,  # stop earlier

            # include transitions that are possible, but not observed
            'feature.possible_transitions': True
        })
        print("model_file: %s" % model_file)
        trainer.train(model_file)
        return True

def test():
    unittest.main()

if __name__ == '__main__':
    test()
