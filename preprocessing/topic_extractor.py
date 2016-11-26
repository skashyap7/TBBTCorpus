from nltk.tokenize          import RegexpTokenizer
from stop_words             import get_stop_words
from nltk.stem.porter       import PorterStemmer
from gensim.models.ldamodel import LdaModel
from gensim                 import corpora, models

class LDA:
	def __init__(self):
		print("Initializing topic extractor")
		self.topics = []
	"""
	This method takes list of documents in string format and returns a list of tokens
	"""
	def __tokenize(self, docs):
		output = []
		for doc in docs:
			tokenizer = RegexpTokenizer(r'\w\w\w\w\w+')
			output.append(tokenizer.tokenize(doc.lower()))
		return output


	"""
	This method takes list of words and identifies stop words and removes them from the list
	"""
	def __remove_stop_words(self, docs):
		output = []
		for doc in docs:
			en_stop = get_stop_words('en')
			stopped_tokens = [i for i in doc if not i in en_stop]
			output.append(stopped_tokens)
		return output


	"""
	This method takes words in each document and returns its corresponding base word
	"""
	def __lemmatizer(self, docs):
		output = []
		for doc in docs:
			stemmer = PorterStemmer()
			texts = [stemmer.stem(i) for i in doc]
			output.append(texts)
		return output


	"""
	This method takes each lemmatized text and generates a document-term matrix
	"""
	def __dt_matrix(self, terms):
		gen_dict = corpora.Dictionary(terms)
		corpus = [gen_dict.doc2bow(term) for term in terms]
		return [corpus, gen_dict]


	def get_topic(self, doc_set):
		# compile sample documents into a list
		o1 = self.__tokenize(doc_set)
		o2 = self.__remove_stop_words(o1)
		#o3 = self.__lemmatizer(o2)
		o4 = self.__dt_matrix(o2)
		
		self.topics = LdaModel(o4[0], num_topics=1, id2word=o4[1], passes=50)
		output = self.topics.show_topics(num_topics=1, num_words=3, log=False, formatted=True)
		return [x.split("*")[1].replace('"', '') for x in output[0][1].split("+")]

