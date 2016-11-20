import json
import re
import operator
import collections
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from nltk.tokenize import RegexpTokenizer

attribute = re.compile("\\((.*)\\)")
class turn:
    def __init__(self, speaker, words):
        self.speaker = speaker
        self.addresse = []
        self.topic = None
        self.words = words
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
        #self.Stopwords = [".","?","\\",";",",","\u2019",")"]
        self.Stopwords = set(stopwords.words('english'))
        self.impactActors = ["Leonard","Sheldon","Penny", "Howard","Raj","Amy","Bernadette"]

    def processText(self, transcript, season, episode):
        """ Map to a logical form """
        scenes = transcript.split("Scene:")
        for s in scenes:
            tt = s.split("\n")
            scene_desc = tt[0].strip()
            sc = Event(scene_desc,episode,season)
            actors = []
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
                    tokenizer = RegexpTokenizer(r'\w+')
                    words = tokenizer.tokenize(dialogue.lower())
                    words, stemmed_words = self.addtoVocab(words)
                    if speaker not in self.impactActors:
                        speaker = "Others"
                    conv = turn(speaker,words)
                    actors.append(speaker)
                    sc.addConversation(conv)
                except ValueError:
                    pass
            actors = set(actors) # get only the unique ones
            sc.addParticipants(actors)
            for c in sc.turn_list:
                # all people in the scene except the speaker are treated recipients
                c.addresse = list(filter(lambda x:  x != c.speaker,actors))
            self.Info.append(sc)

    def addtoVocab(self, words):
        cleanedWords = []
        stemmer = PorterStemmer()
        w_list = self.removeStopWords(words)
        for word in w_list:
            stemmed_word = stemmer.stem(word)
            cleanedWords.append(stemmed_word)
            self.vocabulary[stemmed_word] += 1
        return w_list,cleanedWords

    def removeStopWords(self, words):
        return [word for word in words if word not in self.Stopwords]

    def dumpValues(self):
        """
            Get the content in plain text format. Can deserialize the object to get info
            in JSON format. That's a TODO
        """
        info = {}
        actors = []
        for scene in self.Info:
            key = scene.season+"_"+scene.episode
            sc = {}
            sc["Scene"] = scene.scene_desc
            sc["Partcipiants"] = scene.participants
            sc["Turns"] = []
            for c in scene.turn_list:
                turn = {}
                turn["Speaker"] = c.speaker
                actors.append(c.speaker)
                turn["Words"] = c.words
                turn["Recipients"] = c.addresse
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

    def readTranscripts(self):
        """
            Use the file that has episode and transcript mapping to process
            each scene in the episode and capture all conversations
        """
        with open("corpus.json","r") as fhandle:
            Transcripts = json.load(fhandle)
            fhandle.close()
        for k in Transcripts:
            (episode,season) = k.split("_")
            self.processText(Transcripts[k],season, episode)
        self.dumpValues()

    def getEpisodes(self, season):
        return 
t = getEpisodeTranscripts()
t.readTranscripts()