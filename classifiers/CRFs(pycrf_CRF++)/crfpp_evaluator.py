from itertools import chain
import nltk
import os, sys, glob, csv
from collections import namedtuple
from collections import defaultdict as ddict
import json


class CondRandField(object):

    

    def crfclassify(self, result):
        with open(result,"r", encoding="latin1") as _fhandle:
            content = _fhandle.read()
            _fhandle.close()
        tokens = content.split()
        t = 3
        correct = 0
        pred_shel = 0
        total = len(tokens)  / 5
        print (tokens)
        while t < total:
            if tokens[t] == tokens[t+1] and tokens[t] == "Others":
                print(tokens[t-3],tokens[t], tokens[t+1])
                correct += 1
            if tokens[t] == "Others":
                pred_shel += 1
            t += 5
        precision = correct / pred_shel
        
        print ( precision )


    	


CondRandField().crfclassify(sys.argv[1])