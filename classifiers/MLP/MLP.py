import numpy 
import json
import pycrfsuite
from sklearn import preprocessing
from sklearn.neural_network import MLPClassifier as P
training_topicList=[]
training_recipientsList=[]
training_speakerList=[]

testing_topicList=[]
testing_recipientsList=[]
testing_speakerList=[]

trainingData=dict()
testingData=dict()

topic_encoder= preprocessing.LabelEncoder()#for feature
speaker_encoder=preprocessing.LabelEncoder()#for speaker


def loadJSONFile(path):
	"""
	load json file and dump it as a dict obj, and return it.
	"""
	with open(path, encoding="latin1") as f:
		content=f.read()
		transcriptDict=json.loads(content)
	return transcriptDict

transcript=loadJSONFile("final.json")

def splitData(dictionary, trainingData,testingData):
	"""
	split data into 80% training and 20% testing
	"""
	length=len(dictionary)
	trainingLength=int(length*4/5)
	count=0
	for key in dictionary:
		if count<trainingLength:
			trainingData[key]=dictionary[key]
		else:
			testingData[key]=dictionary[key]
		count=count+1

splitData(transcript, trainingData, testingData)



def extractFeatures(dictionary, topicList, recipientsList, speakerList):
	"""
	extract feature vectors and speaker lables for training data
	"""
	for key in dictionary:
		sceneList=dictionary[key]
		for i in range(len(sceneList)):
			sceneDict=sceneList[i]
			if "Turns" in sceneDict:
				turnList=sceneDict["Turns"]
				if len(turnList)>0:
					for turnIndex in range(len(turnList)):
						turnDict=turnList[turnIndex]
						#extract bag of words with POS
						topics=turnDict["Topics"]
						topicList.append(topics)
						#extract speaker
						speakerList.append(turnDict["Speaker"])
						#extract recipients
						recipients=turnDict["Recipients"]
						recipientsList.append(recipients)

	

extractFeatures(trainingData, training_topicList, training_recipientsList, training_speakerList)
extractFeatures(testingData, testing_topicList, testing_recipientsList, testing_speakerList)

def allRecipents(recipientsList):
	recipients=[]
	recipients.extend(recipientsList)
	return recipients

allCharacters=allRecipents(training_speakerList)
speaker_encoder.fit(allCharacters)
#print(speaker_encoder.classes_)
def allTopics(training_topicList, testing_topicList):
	topics=[]
	for i in range(len(training_topicList)):
		if training_topicList[i] is not None:
			topics.extend(training_topicList[i])
	for i in range(len(testing_topicList)):
		if testing_topicList[i] is not None:
			topics.extend(testing_topicList[i])	
	return topics
allTopics=allTopics(training_topicList, testing_topicList)
allTopics=[item.strip() for item in allTopics]
#print(allTopics)
topic_encoder.fit(allTopics)
feature_vector_length=len(topic_encoder.classes_)

#create input feature vector, lenght = feature_vector_lenght

def inputFeatureMat(topicList, topic_encoder, feature_vector_length):
	result=[]
	
	for i in range(len(topicList)):
		unencode_vector=topicList[i]
		feature_vector=[0]*feature_vector_length
		if unencode_vector is not None:
			unencode_vector=[item.strip() for item in unencode_vector]
			encode_vector=topic_encoder.transform(unencode_vector)
			if i==1:
				print("Before applied label_encoder on input feature: "+str(unencode_vector))
				print("After applied label_encoder on input feature: "+str(encode_vector))
			for j in range(len(encode_vector)):
				feature_vector[encode_vector[j]]=1
			result.append(feature_vector)
		else:
			result.append(feature_vector)
	return result


trainingMat=inputFeatureMat(training_topicList, topic_encoder, feature_vector_length)
testingMat=inputFeatureMat(testing_topicList, topic_encoder, feature_vector_length)

training_y=speaker_encoder.transform(training_speakerList)
testing_y=speaker_encoder.transform(testing_speakerList)


trainer = P(hidden_layer_sizes=(75,6), activation='logistic', solver='adam', alpha=0.00001, batch_size='auto', learning_rate='constant', learning_rate_init=0.001, power_t=0.5, max_iter=200, shuffle=True, random_state=None, tol=0.0001, verbose=True, warm_start=False, momentum=0.9, nesterovs_momentum=True, early_stopping=False, validation_fraction=0.1, beta_1=0.9, beta_2=0.999, epsilon=1e-08)
trainer = trainer.fit(trainingMat, training_y)
predict_y=trainer.predict(testingMat)
#print(training_feature_mat)
#print(training_speakerList)
pred=speaker_encoder.inverse_transform(predict_y)
#print(pred)
def evaluate(predication, true):
	correct=0
	for i in range(len(true)):
		if predication[i] == true[i]:
			correct=correct+1
	ac=correct/len(true)
	print("Accuracy is: "+str(ac))

evaluate(pred, testing_speakerList)

def performance(predication, true):
	pre_correct_sheldon=0
	pre_correct_leonard=0
	pre_correct_penny=0
	pre_correct_howard=0
	pre_correct_others=0
	true_sheldon=0
	true_leonard=0
	true_penny=0
	true_howard=0
	true_others=0
	pre_sheldon=0
	pre_leonard=0
	pre_penny=0
	pre_howard=0
	pre_others=0

	#count pre_*
	for i in range(len(predication)):
		if "Sheldon" == predication[i]:
			pre_sheldon=pre_sheldon+1
		elif "Leonard" == predication[i]:
			pre_leonard=pre_leonard+1
		elif "Penny" == predication[i]:
			pre_penny=pre_penny+1
		elif "Howard" == predication[i]:
			pre_howard=pre_howard+1
		else:
			pre_others=pre_others+1
	#count true_*
	for i in range(len(true)):
		if "Sheldon" == true[i]:
			true_sheldon=true_sheldon+1
		elif "Leonard" == true[i]:
			true_leonard=true_leonard+1
		elif "Penny" == true[i]:
			true_penny=true_penny+1
		elif "Howard" == true[i]:
			true_howard=true_howard+1
		else:
			true_others=true_others+1
	#count pre_correct_*
	for i in range(len(true)):
		if "Sheldon" == true[i] and predication[i]==true[i]:
			pre_correct_sheldon=pre_correct_sheldon+1
		elif "Leonard" == true[i] and predication[i]==true[i]:
			pre_correct_leonard=pre_correct_leonard+1
		elif "Penny" == true[i] and predication[i]==true[i]:
			pre_correct_penny=pre_correct_penny+1
		elif "Howard" == true[i] and predication[i]==true[i]:
			pre_correct_howard=pre_correct_howard+1
		elif "Others" == true[i] and predication[i]==true[i] or "Raj" == true[i] and predication[i]==true[i]:
			pre_correct_others=pre_correct_others+1

	precision_sheldon=pre_correct_sheldon/pre_sheldon
	recall_sheldon=pre_correct_sheldon/true_sheldon
	f1_sheldon=2*(precision_sheldon*recall_sheldon)/(precision_sheldon+recall_sheldon)
	print("Presision for sheldon: "+str(precision_sheldon))
	print("Recall for sheldon: "+str(recall_sheldon))
	print("F1 for sheldon: "+str(f1_sheldon))

	precision_leonard=pre_correct_leonard/pre_leonard
	recall_leonard=pre_correct_leonard/true_leonard
	f1_leonard=2*(precision_leonard*recall_leonard)/(precision_leonard+recall_leonard)
	print("Presision for leonard: "+str(precision_leonard))
	print("Recall for leonard: "+str(recall_leonard))
	print("F1 for leonard: "+str(f1_leonard))

	precision_penny=pre_correct_penny/pre_penny
	recall_penny=pre_correct_penny/true_penny
	f1_penny=2*(precision_penny*recall_penny)/(precision_penny+recall_penny)
	print("Presision for penny: "+str(precision_penny))
	print("Recall for penny: "+str(recall_penny))
	print("F1 for penny: "+str(f1_penny))

	precision_howard=pre_correct_howard/pre_howard
	recall_howard=pre_correct_howard/true_howard
	f1_howard=2*(precision_howard*recall_howard)/(precision_howard+recall_howard)
	print("Presision for howard: "+str(precision_howard))
	print("Recall for howard: "+str(recall_howard))
	print("F1 for howard: "+str(f1_howard))

	precision_others=pre_correct_others/pre_others
	recall_others=pre_correct_others/true_others
	f1_others=2*(precision_others*recall_others)/(precision_others+recall_others)
	print("Presision for others: "+str(precision_others))
	print("Recall for others: "+str(recall_others))
	print("F1 for others: "+str(f1_others))

performance(pred, testing_speakerList)