from itertools import chain
import nltk
import os, sys, glob, csv
from collections import namedtuple
from collections import defaultdict as ddict
import json


class CondRandField(object):

    

    def crfclassify(self, jsonfile, train, test):
    	words = []
    	POS = []
    	Speaker = []
    	Topic = []
    	with open(jsonfile) as data_file:
    		data = json.load(data_file)

    	if train == True:
    		seasonL = 7
    		EpisodeL = 20
    		s = e = 1
    	else:
    		seasonL = 8
    		EpisodeL = 20
    		s = e = 7

    	while s != seasonL:
    		while e != EpisodeL:
    			key = str(s)+"_"+str(e)
    			if key in data:
	    			for z in range(len(data[key])):
	    				for y in range(len(data[key][z]["Turns"])):
	    					turn = data[key][z]["Turns"][y]["Words"]
	    					for x in range(len(turn)):
	    						words.append(turn[x][0])
	    						POS.append(turn[x][1])
	    						Topic.append(data[key][z]["Turns"][y]["Topics"][0])
	    						sp = data[key][z]["Turns"][y]["Speaker"]
	    						
	    						if ((sp != "Sheldon") and (sp != "Leonard") and (sp != "Howard") and (sp != "Penny")):
	    							sp = "Others"
	    						Speaker.append(sp)
	    		e+=1
    		s+=1
    	i = 0
    	if train ==  True:
    		data_file = "train.data"
    	else:
    		data_file = "test.data"

    	with open(data_file, 'w') as out:
    		while i != len(words):
    			out.write(words[i]+" "+POS[i]+" "+Topic[i]+" "+Speaker[i])
    			out.write("\n")
    			i += 1

CondRandField().crfclassify(sys.argv[1], True, False)
CondRandField().crfclassify(sys.argv[1], False, True)