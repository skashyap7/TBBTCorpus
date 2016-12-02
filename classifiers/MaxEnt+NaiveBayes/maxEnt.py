from json import loads
from sklearn import linear_model
from sklearn.feature_extraction.text import TfidfVectorizer


"""
	Maximum entroy trainer : Uses scikit learn Logistic Regression module
"""
class MaxEnt:

	# Constructor
	def __init__(self):
		self.train_data   = []
		self.train_label  = []
		self.test_data    = []
		self.test_label   = []
		self.logistic     = linear_model.LogisticRegression()
		self.train_vector = None
		self.test_vector  = None
		self.vec          = None
		self.maxEnt       = None
		self.prediction   = None

	# file_name: should be of type JSON 
	def _parserTrain(self, file_name):
		content = None
		with open(file_name, "r") as reader:
			try:
				content = loads(reader.read())
			except:
				print("JSON file is not parsable")
				return
		if not content:
			print("No data found")
			return


		season_list = []		
		for seasons in content:
			season_num = int(seasons.split("_")[1])
			season_list.append(season_num)

			turns = content[seasons][1]["Turns"]
			for turn in turns:
				sentence = ""
				for word in turn["Words"]:
					sentence += word[0] + " "
				sentence = sentence.strip()
				label  = turn["Speaker"]
				if len(sentence) == 0:
					continue
				if season_num <= 8:
					self.train_data.append(sentence)
					self.train_label.append(self._convertSpeaker(label))
				else:
					self.test_data.append(sentence)
					self.test_label.append(self._convertSpeaker(label))

	
		season_list.sort()	


	def _trainModel(self):
		self.vec = TfidfVectorizer(min_df=3,lowercase=True, sublinear_tf=True, use_idf=True)
		self.train_vector = self.vec.fit_transform(self.train_data)
		
		self.maxEnt = linear_model.LogisticRegression()
		self.maxEnt.fit(self.train_vector, self.train_label)

	def _classifyData(self):
		self.test_vector = self.vec.transform(self.test_data)
		self.prediction  = self.maxEnt.predict(self.test_vector)

	def _calAccuracy(self):
		print(len(self.test_label), len(self.prediction))
		correct = 0
		actual  = len(self.test_label)
		for act, pred in zip(self.test_label, self.prediction):
			print(act, pred)
			if act == pred:
				correct += 1
		print(correct/actual)

	def _convertSpeaker(self, speaker_name):
		
		if speaker_name != "Leonard" and speaker_name != "Sheldon" and speaker_name != "Penny" and speaker_name != "Howard":
			return "Others"
		return speaker_name

	def _calculatePRF(self):
		counter = {"Sheldon":{"correct": 0, "acutal": 0, "predicted": 0}, "Howard": {"correct": 0, "acutal": 0, "predicted": 0}, "Penny": {"correct": 0, "acutal": 0, "predicted": 0}, "Leonard":{"correct": 0, "acutal": 0, "predicted": 0}, "Others":{"correct": 0, "acutal": 0, "predicted": 0}}	
		
		for act, pre in zip(self.test_label, self.prediction):
			if act == pre:
				counter[pre]["correct"] += 1
			counter[act]["acutal"] += 1
			counter[pre]["predicted"] += 1

		for speaker in counter:
			precision = counter[speaker]["correct"] / counter[speaker]["predicted"]
			recall = counter[speaker]["correct"] / counter[speaker]["acutal"]

			f1 = (2 * precision * recall) / (precision + recall)

			print(speaker, precision, recall, f1)

trainer = MaxEnt()
trainer._parserTrain("/Users/rakshithr/Desktop/MaxEnt/MaxEnt/final.json")
trainer._trainModel()
trainer._classifyData()
trainer._calAccuracy()
trainer._calculatePRF()
