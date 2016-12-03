import json
import sys
import sklearn
from sklearn import svm
from sklearn.svm import SVC
from sklearn.feature_extraction.text import TfidfVectorizer

path_to_corpus = "..\\..\\preprocessing\\final.json"

class svmClassifier:
    def __init__(self, path):
        self.train_data  = []
        self.test_data   = []
        self.train_labels = []
        self.test_labels = []
        self.classification = []
        self.svm_classifier = svm.SVC(gamma=0.001, C=50,decision_function_shape='ovr',kernel='rbf')
        self.corpus_path = path
        self.corpus = {}
        self.vocab = []

    """ This function reads the corpus file into a dict"""
    def readCorpus(self):
        with open(self.corpus_path,"r") as fh:
            self.corpus = json.load(fh)

    """ This function generates a list of words for a dialogue"""
    def bagofWords(self, turn):
        label = turn.Speaker
        feature = [x[0].strip() for x in turn.Words]
        return feature,label

    def train(self):
        for season_episode in self.corpus:
            season,episode = [int(x) for x in season_episode.split("_")]
            if season < 8:
                episode = self.corpus[season_episode]
                for scene in episode:
                    for turn in scene["Turns"]:
                        self.train_data.append(" ".join([x[0] for x in turn["Words"]]))
                        self.vocab.extend([x[0].strip() for x in turn["Words"]])
                        self.train_labels.append(turn["Speaker"])
            else:
                episode = self.corpus[season_episode]
                for scene in episode:
                    for turn in scene["Turns"]:
                        self.test_data.append(" ".join([x[0] for x in turn["Words"]]))
                        self.vocab.extend([x[0].strip() for x in turn["Words"]])
                        self.test_labels.append(turn["Speaker"])

    def predict(self):
        vec = TfidfVectorizer(min_df=3,lowercase=True, sublinear_tf=True, use_idf=True,vocabulary=list(set(self.vocab)))
        train_vector = vec.fit_transform(self.train_data)
        print("Generating model")
        self.svm_classifier.fit(train_vector,self.train_labels)
        test_vector = vec.transform(self.test_data)
        print("Classifying Data")
        self.classification = self.svm_classifier.predict(test_vector)

    def get_stats(self, filename):
        counter = {"Sheldon":{"correct": 0, "acutal": 0, "predicted": 0}, "Howard": {"correct": 0, "acutal": 0, "predicted": 0}, "Penny": {"correct": 0, "acutal": 0, "predicted": 0},\
         "Leonard":{"correct": 0, "acutal": 0, "predicted": 0},\
         "Raj":{"correct": 0, "acutal": 0, "predicted": 0},"Others":{"correct": 0, "acutal": 0, "predicted": 0}} 
        txt = "\n Speaker\tPrecision\tRecall\t\tF1\n"
        try:
            for act, pre in zip(self.test_labels, self.classification):
                if act == pre:
                    counter[pre]["correct"] += 1
                counter[act]["acutal"] += 1
                counter[pre]["predicted"] += 1

            for speaker in counter:
                if counter[speaker]["predicted"]:
                    precision = counter[speaker]["correct"] / counter[speaker]["predicted"]
                else:
                    precision = 0
                if counter[speaker]["acutal"]:
                    recall = counter[speaker]["correct"] / counter[speaker]["acutal"]
                else:
                    recall = 0
                if precision+recall != 0:
                    f1 = (2 * precision * recall) / (precision + recall)
                else:
                    f1 = 0
                print(speaker, precision, recall, f1)
                txt += speaker+"\t\t"+ str(format(precision*100,'.2f'))+"\t\t"+str(format(recall*100,'.2f'))+"\t\t"+str(format(f1*100,'.2f'))+"\n"
        except KeyError:
            pass
        with open("bow_ovr.txt","w") as fh:
            json.dump(counter,fh)
        with open("results\\"+filename,"w") as fh:
            fh.write(txt)

if sys.argv[1]:
    output_filename = sys.argv[1]
else:
    output_filename ="result.txt"
svm = svmClassifier(path_to_corpus)
svm.readCorpus()
svm.train()
svm.predict()
svm.get_stats(output_filename)