import corpus_reader 
import json
import itertools

import scipy
import sklearn
from sklearn import svm
from sklearn.svm import SVC

Season_Episode_Mapping = {
    1: 17,
    2: 7,
    3: 23,
    4: 23,
    5: 23,
    6: 22,
    7: 24,
    8: 24,
    9: 24
}

speaker_enum = {
    "Leonard": 1,
    "Sheldon": 2,
    "Penny" : 3,
    "Howard": 4,
    "Raj" : 5,
    "Others": 6,
}

speaker_rev_enum = {
    1: "Leonard",
    2: "Sheldon",
    3: "Penny",
    4: "Howard",
    5: "Raj",
    6: "Others",
    7: "Amy",
    8: "Bernadette"
}

act_tag_enum = {
    "whQuestion" : 1,
    "Continuer" : 2,
    "Other" : 3,
    "nAnswer" : 4,
    "Statement" : 5,
    "Clarify" : 6,
    "Reject" : 7,
    "System" : 8,
    "Emphasis" : 9,
    "yAnswer" : 10,
    "ynQuestion" : 11,
    "Greet" : 12,
    "Accept" : 13,
    "Emotion" : 14,
    "Bye": 15
}

with open("topics.json","r") as th:
    topic_list = json.load(th)
sorted(topic_list)
topic_enum = {}
for idx,topic in enumerate(topic_list):
    topic_enum[topic] = idx


# Please change with the relative path to corpus (final.json)
#path_to_corpus = "D:\\NLP-544\\Speaker-Prediction\\preprocessing\\final.json"
path_to_corpus = "..\\..\\preprocessing\\final.json"
corpus_reader.loadCorpus(path_to_corpus)

def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = itertools.tee(iterable)
    next(b, None)
    return zip(a, b)

def getpairwise(iterable):
    p = pairwise(iterable)
    return [ x+","+y for x,y in p]    

def addPairFeature(token_list,feature):
    idx1 = 0
    idx2 = 1
    for f_add in getpairwise(token_list):
        ft_tag = "token["+str(idx1)+":"+str(idx2)+"]="
        feature.append(ft_tag+f_add)

def turn2feature(turn, bos):
    feature = []
    
    # a feature for speaker
    if bos:
        feature.append(1)
    else:
        feature.append(0)
    
    # a feature for a speaker
    feature.append(speaker_enum[turn.Speaker])
    # This feature will be redundant as every turn has diff speaker
    #if prev_speaker and prev_speaker != turn.Speaker:
    #    feature.append("speaker_change=True")
    
    # a feature for tokens in dialogue
    #for words in turn.Words:
    #    feature.append("word=TOKEN_"+words[0])
    
    # A feature for pos of word's in dialogues
    #for words in turn.Words:
    #    feature.append("pos=POS_"+words[1])

    # A feature for bigrams of the tokens
    #addPairFeature([x[0] for x in turn.Words],feature)
    
    # A feature for recipients of dialogues
    #for recipient in turn.Recipients:
    #    feature.append("pos=REC_"+recipient)
    
    # A feature for act_tag
    feature.append(act_tag_enum[turn.Act_Tag[0]])

    # feature for Topic
    if turn.Topics:
        # some utterances have only 2 topics
        # we may have to add a special tag to say 
        # it does not have enough topics
        cnt  = 0
        for topic in turn.Topics:
            try:
                feature.append(topic_enum[topic])
            except KeyError:
                feature.append(topic_enum["Unknown"])
            cnt += 1
        while(cnt < 3):
            feature.append(topic_enum["Insufficient_Topics"])
            cnt += 1
    # Feature for scene
    #feature.append("scene=SCENE_"+turn.Scene)
    #print(feature)
    return feature,speaker_enum[turn.Speaker]


def episode2feature(season,episode):
    EpisodeFeature = []
    Label = []
    #prev_speaker = None
    bos = True
    eos = False
    for turn in corpus_reader.getNextTurn(season,episode):
        if bos:
            bos = False
        feature, label = turn2feature(turn, bos)
        if len(feature) != 6:
            continue
        EpisodeFeature.append(feature)
        Label.append(label)
    return EpisodeFeature,Label

def get_stats(result,train_labels,class_num):
    total_classified = 0
    correct_classified = 0
    wrong_classified = 0
    total_labels = 0
    for i in range(len(result)):
        if result[i] == class_num:
            if train_labels[i] == result[i]:
                correct_classified += 1
            else:
                wrong_classified += 1
    for i in range(len(train_labels)):
        if train_labels[i] == class_num:
            total_labels += 1

    total_classified = correct_classified + wrong_classified
    precision = (correct_classified/total_classified)
    recall = (correct_classified/total_labels)
    if (precision + recall) == 0:
        f1_score = 0
    else:
        f1_score = (2*precision*recall)/(precision+recall)
    return precision*100 ,recall*100, f1_score*100

def start_program():
    clf = svm.SVC(gamma=0.001, C=100.)
    all_features = []
    all_labels = []
    train_features = []
    train_labels = []
    for season in range(1,5):
        for episode in range(1,Season_Episode_Mapping[season]-4):
            features, labels = episode2feature(season,episode)
            all_features.extend(features)
            all_labels.extend(labels)
    #print(all_features)
    for season in range(5,8):
        for episode in range(Season_Episode_Mapping[season]-4,Season_Episode_Mapping[season]+1):
            features, labels = episode2feature(season,episode)
            train_features.extend(features)
            train_labels.extend(labels)

    clf.fit(all_features,all_labels)
    result = clf.predict(train_features)
    txt = "\n Speaker\tPrecision\tRecall\t\tF1\n"
    for i in range(1,7):
        precision, recall,f1_score = get_stats(result, train_labels,i)
        txt += speaker_rev_enum[i]+"\t\t"+ str(format(precision,'.2f'))+"\t\t"+str(format(recall,'.2f'))+"\t\t"+str(format(f1_score,'.2f'))+"\n"
    with open("output.txt","w") as fh:
        fh.write(txt)


start_program()
