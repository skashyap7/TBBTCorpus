import json
import re
import operator
import collections
import nltk
import os
from generate_act_tag import Act_Tag
from os import path
from stop_words import get_stop_words
from nltk.stem.porter import PorterStemmer
from nltk.tokenize import RegexpTokenizer
from topic_extractor import LDA



attribute = re.compile("\\((.*)\\)")
class turn:
    def __init__(self, speaker, words, scene, act_tag):
        self.speaker = speaker
        self.addresse = []
        self.topic = []
        self.words = []
        self.scene = scene
        self.act_tag = act_tag
        for token,pos  in nltk.pos_tag(words):
            self.words.append((token,pos))
        self.speaker_attribute = None

    def addAddresse(self, p_list):
        self.addresse = p_list


class Event:
    def __init__(self, scene_desc, episode, season):
        self.episode = episode
        self.season = season
        self.scene_desc = scene_desc
        self.turn_list = []
        self.cntr = -1
        self.participants = []

    def addConversation(self, conv):
        self.turn_list.append(conv)

    def addParticipants(self, actors):
        self.participants = list(actors)

class getEpisodeTranscripts:
    def __init__(self):
        self.episodeInfo = {}
        self.Info = []
        self.allTranscripts = {}
        self.vocabulary = collections.defaultdict(int)
        self.Stopwords = get_stop_words('en')
        self.impactActors = ["Leonard","Sheldon","Penny", "Howard","Raj","Amy","Bernadette"]

    def processText(self, transcript, season, episode):
        """ Map to a logical form """
        scenes = transcript.split("Scene:")
        for s in scenes:
            tt = s.split("\n")
            scene_desc = tt[0].strip()
            sc = Event(scene_desc,episode,season)
            actors = []
            doc_set = []
            for t in tt[1:]:
                try:
                    (speaker, dialogue) =  t.split(":")
                    # check if the speaker has associated attributes with it
                    speaker = speaker.strip()
                    #print(speaker)
                    m = attribute.search(speaker)
                    if m:
                        attr = m.group(1)
                        # Remove extra information from speaker info
                        # eg : Sheldon (Laughing) : should give only sheldon
                        # as the speaker
                        speaker = speaker.split("(")[0].strip()
                    doc_set.append(dialogue) 
                    tokenizer = RegexpTokenizer(r'\w+')
                    words = tokenizer.tokenize(dialogue.lower())
                    act_tag = Act.get_act_tag([dialogue]) 
                    words = self.addtoVocab(words)
                    if speaker not in self.impactActors:
                        speaker = "Others"
                    conv = turn(speaker,words, scene_desc, act_tag)
                    actors.append(speaker)
                    sc.addConversation(conv)
                except ValueError:
                    pass
            actors = set(actors) # get only the unique ones
            if doc_set:
                try:
                    topic = lda.get_topic(doc_set)
                except ValueError:
                    topic = None
            else:
                topic = None
            sc.addParticipants(actors)
            for c in sc.turn_list:
                # all people in the scene except the speaker are treated recipients
                c.addresse = list(filter(lambda x:  x != c.speaker,actors))
                c.topic = topic
            self.Info.append(sc)

    def addtoVocab(self, words):
        #stemmer = PorterStemmer()
        w_list = self.removeStopWords(words)
        for word in w_list:
            self.vocabulary[word] += 1
        return w_list

    def removeStopWords(self, words):
        return [word for word in words if word not in self.Stopwords]

    def dumpValues(self):
        """
            Get the content in plain text format. Can deserialize the object to get info
            in JSON format. That's a TODO
        """
        info = {}
        actors = []
        dialogue_list = []
        for scene in self.Info:
            key = scene.season+"_"+scene.episode
            sc = {}
            sc["Scene"] = scene.scene_desc
            sc["Partcipiants"] = scene.participants
            sc["Turns"] = []
            dialogue_list.append(scene.scene_desc)
            for c in scene.turn_list:
                turn = {}
                turn["Speaker"] = c.speaker
                turn["Scene"] = c.scene
                actors.append(c.speaker)
                turn["Words"] = c.words
                turn["Topics"] = c.topic
                turn["Act_Tag"] = c.act_tag
                turn["Recipients"] = c.addresse
                dlg = c.speaker+" : "+" ".join(x[0] for x in c.words)
                dialogue_list.append(dlg)
                sc["Turns"].append(turn)
            if key not in info:
                info[key] = []
            info[key].append(sc)
        with open("final.json","w") as fh:
            json.dump(info,fh,indent=4)
            fh.close()
        # Dump Vocabulary
        with open("vocabulary.json","w") as fh:
            json.dump(self.vocabulary,fh,indent=4)
            fh.close()
        with open("dialogues.json","w") as fh:
            json.dump(dialogue_list,fh)
            fh.close()

    def readTranscripts(self):
        """
            Use the file that has episode and transcript mapping to process
            each scene in the episode and capture all conversations
        """
        #corpus_path = "D:\\NLP-544\\Speaker-Prediction\\preprocessing\\corpus.json"
        corpus_path = "corpus.json"
        with open(corpus_path,"r") as fhandle:
            Transcripts = json.load(fhandle)
            fhandle.close()
        for k in Transcripts:
            (episode,season) = k.split("_")
            self.processText(Transcripts[k],season, episode)
        self.dumpValues()

    def getEpisodes(self, season):
        return 

lda = LDA()
Act = Act_Tag()
t = getEpisodeTranscripts()
t.readTranscripts()
