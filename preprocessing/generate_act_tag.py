import nltk
from collections import defaultdict
"""
 Class generates act_tag based on the existing corpus in nltk
 There are total of 15 act tags which can be assigned to any sentence
"""
class Act_Tag:

	# Initialize the corpus and train the classifier based on this featureset
	def __init__(self):
		self.tagged_data = nltk.corpus.nps_chat.xml_posts()[:10000]
		self.output = []
		self.act_set = [(self.__tokenize_sentence(post.text), post.get('class')) for post in self.tagged_data]
		self.classifier = nltk.NaiveBayesClassifier.train(self.act_set)

	# Method returns the sentence in required format
	def __tokenize_sentence(self, utterance):
		word_act = {}

		for word in nltk.word_tokenize(utterance):
			word_act['contains({})'.format(word.lower())] = True
		return word_act

	# Method classifies the given sentence based on trained classifier set
	def get_act_tag(self, utterance):
		inp_utt = []
		for utt in utterance:
			inp_utt.append(self.__tokenize_sentence(utt))
		
		return self.classifier.classify_many(inp_utt)

# Remove the below comment for example on how to run this class
"""
act = Act_Tag()
inp = ["I am bored","What are your plans for tomorrow?"]
print(act.get_act_tag(inp))
"""
