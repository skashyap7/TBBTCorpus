import corpus_reader 
import json
import itertools

Season_Episode_Mapping = {
    1: 9,
    2: 9,
    3: 9,
    4: 9,
    5: 7,
    6: 9,
    7: 9
}

# Please change with the relative path to corpus (final.json)
#path_to_corpus = "D:/NLP-544/Speaker-Prediction/preprocessing/final.json"
path_to_corpus = "path/to/final.json"
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
        feature.append("bos="+bos)
    
    # a feature for a speaker
    feature.append("speaker="+turn.Speaker)
    # This feature will be redundant as every turn has diff speaker
    #if prev_speaker and prev_speaker != turn.Speaker:
    #    feature.append("speaker_change=True")
    
    # a feature for tokens in dialogue
    for words in turn.Words:
        feature.append("word=TOKEN_"+words[0])
    
    # A feature for pos of word's in dialogues
    for words in turn.Words:
        feature.append("pos=POS_"+words[1])

    # A feature for bigrams of the tokens
    addPairFeature([x[0] for x in turn.Words],feature)
    
    # A feature for recipients of dialogues
    for recipient in turn.Recipients:
        feature.append("pos=REC_"+recipient)
    
    # A feature for act_tag
    feature.append("act_tag="+turn.Act_Tag[0])

    # feature for Topic
    if turn.Topics:
        for topic in turn.Topics:
            feature.append("topic=TOPIC_"+topic)
    
    # Feature for scene
    feature.append("scene=SCENE_"+turn.Scene)
    return feature,turn.Speaker


def episode2feature(season,episode):
    EpisodeFeature = []
    #prev_speaker = None
    bos = True
    eos = False
    for turn in corpus_reader.getNextTurn(season,episode):
        if bos:
            bos = False
        feature, label = turn2feature(turn, bos)
        #print(feature)
        print(label)

def start_program():
    for season in Season_Episode_Mapping:
        for episode in range(1,Season_Episode_Mapping[season]+1):
            episode2feature(season,episode)

start_program()
