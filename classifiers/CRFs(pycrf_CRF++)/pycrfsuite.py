from itertools import chain
import nltk
import pycrfsuite as crf
import os, sys, glob, csv
from collections import namedtuple
import hw3_corpus_tool as tool
import numpy as np
from collections import defaultdict as ddict


#Class to perform conditional random field classification
class CondRandField(object):

    #Initializing the number of iterations to 50.
    #The L1 penalty value is assigned to 1.0
    #The L2 penalty value is assigned to 1e-3
    #The possible transitions is set to True
    def __init__(self, enumerations=100, L1Penalty=1.0, L2Penalty=1e-3):
        self.crf_feature_train = crf.Trainer(verbose=False)
        self.crf_feature_train.set_params({
            'c1': L1Penalty,
            'c2': L2Penalty,
            'max_iterations': enumerations,
            'feature.possible_transitions': True
        })
    
    #Method to append more features to the trainer
    #More features include TOKEN and its respective POS
    #It also includes the act tag of the sentence
    def MoreFeatures(self, features, sentence, conv, index):
        if sentence.pos is not None:
            for x, partofspeech in enumerate(sentence.pos):
                features.append("TOKEN_%s" % (partofspeech.token))
                features.append("POS[%d]=%s" % (x+1, partofspeech.pos))
        else: 
            words = sentence.text.replace('>', '').replace('<', '').replace('.', '').split()
            for x, word in enumerate(words):
                features.append("ACT_TAG[%d]=%s" % (x+1, word))
        return features

    #Method to append basic features to the trainer
    #More features include beginning of the sentence
    #It also includes feature to indicate change of speaker for a given utterance
    def AppendFeatures(self, conv, index):
        features = []
        if index == 0:
            features.append("BOS")
        else:
            if conv[index].speaker != conv[index-1].speaker:
                features.append('SpeakerChange')
        sentence = conv[index]
        crf_features = self.MoreFeatures( features, sentence, conv, index)
        return crf_features
    
    #Method to build the x and y values for the crf model
    #The value_x indicates the list of features for a given sentence
    #The value_y indicates the list of act tags for all the sentences in the dialog
    def buildmodel(self, conv):
        value_x, value_y = [], []
        for index, sentence in enumerate(conv):
            value_x.append(self.AppendFeatures(conv, index))
            value_y.append(sentence.act_tag)
        return value_x, value_y

    def crftrainer(self, directry, data_model):
        conversations = tool.get_data(directry)
        for f_name, conv in conversations:
            value_x, value_y = self.buildmodel(conv)
            self.crf_feature_train.append(value_x, value_y)
        
        self.crf_feature_train.train(data_model)
    
    #Method to write the output to a file in the following format
    #Filename=xyz.csv
    #LABEL1
    #LABEL2
    #...
    def writetofile(self, conversations, output):
        with open(output, 'w') as out:
            for f_name, conv in conversations:
                out.write('Filename="%s"\n' % f_name.split("/")[-1])
                value_x, value_y = self.buildmodel(conv)
                prediction_value_y = self.crf_tag.tag(value_x)
                assert len(prediction_value_y) == len(value_x)
                out.write("\n".join(prediction_value_y))
                out.write("\n\n")        
   
    def crfpred(self, datafolder, output):
        conversations = tool.get_data(datafolder)
        self.writetofile(conversations, output)      

    def base_Crf(self, directry, datafolder, output, crfmodel):
        self.crftrainer(directry, crfmodel)
        self.crf_tag = crf.Tagger()
        self.crf_tag.open(crfmodel)
        self.crfpred(datafolder, output)

    def crfclassify(self, directry, datafolder, output, crfmodel="crf_model.data"):
        self.base_Crf(directry, datafolder, output, crfmodel)

class ExtendedCRF(CondRandField):
    

    def ExtraAdvancedFeatures(self, conv, index, sentence, adv_features):
        if sentence.pos is not None:
            for m in range(len(sentence.pos)):
                adv_features.append("TOKEN[%d]=%s" % (m, sentence.pos[m].token))
                adv_features.append("POS[%d]=%s" % (m, sentence.pos[m].pos))

            for y in range(len(sentence.pos) - 1):
                adv_features.append("TOKEN_%s|TOKEN_%s" % (sentence.pos[y].token, sentence.pos[y+1].token))
                adv_features.append("POS_%s|POS_%s" % (sentence.pos[y].pos, sentence.pos[y+1].pos))
        
        return adv_features



    def AppendFeatures(self, conv, index):
        adv_features = super(ExtendedCRF, self).AppendFeatures(conv, index)
        if index == len(conv) - 1:
            adv_features.append("EOS")
            pass
        if index == len(conv) - 2:
            adv_features.append("EOS[-1]")
            pass

        sentence = conv[index]
        advanced_features = self.ExtraAdvancedFeatures(conv, index, sentence, adv_features)
        
        return advanced_features
ExtendedCRF(enumerations=100).crfclassify(sys.argv[1], sys.argv[2], sys.argv[3])