from getBagOfWords import BagOfWords
import nltk

train_set = []
test_set = []
test_label = []
bw = BagOfWords()
predict = []

def baseline_classification():
	bw._parserTrain("/Users/rakshithr/Desktop/MaxEnt/MaxEnt/final.json")
	train_set = []
	for x,y in zip(bw.train_data, bw.train_label):
		train_set.append(({"token": x},convertSpeaker(y)))

	test_set = []
	for x,y in zip(bw.test_data, bw.test_label):
		lab = convertSpeaker(y)
		test_set.append(({"token": x}, lab))
		test_label.append(lab)

	classifier = nltk.NaiveBayesClassifier.train(train_set)

	print(nltk.classify.accuracy(classifier, test_set))
	#predict = nltk.classify.predict(classifier, test_set)

def convertSpeaker(speaker_name):

	if speaker_name != "Leonard" and speaker_name != "Sheldon" and speaker_name != "Penny" and speaker_name != "Howard":
		return "Others"
	return speaker_name

def calculatePRF():
	counter = {"Sheldon":{"correct": 0, "acutal": 0, "predicted": 0}, "Howard": {"correct": 0, "acutal": 0, "predicted": 0}, "Penny": {"correct": 0, "acutal": 0, "predicted": 0}, "Leonard":{"correct": 0, "acutal": 0, "predicted": 0}, "Others":{"correct": 0, "acutal": 0, "predicted": 0}}

	for act, pre in zip(test_label, predict):
		if act == pre:
			counter[pre]["correct"] += 1
		counter[act]["acutal"] += 1
		counter[pre]["predicted"] += 1

	for speaker in counter:
		precision = counter[speaker]["correct"] / counter[speaker]["predicted"]
		recall = counter[speaker]["correct"] / counter[speaker]["acutal"]

		f1 = (2 * precision * recall) / (precision + recall)

		print(speaker, precision, recall, f1)
baseline_classification()
#calculatePRF()
