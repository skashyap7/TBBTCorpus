from json import loads


"""
	This class divides the data into bag of words
	Season 1-8 are in train, rest in test
"""
class BagOfWords:

	# Constructor
	def __init__(self):
		self.train_data   = []
		self.train_label  = []
		self.test_data    = []
		self.test_label   = []

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
				label  = turn["Speaker"]
				if len(sentence) == 0:
					continue
				if season_num <= 8:
					self.train_data.append(sentence)
					self.train_label.append(label)
				else:
					self.test_data.append(sentence)
					self.test_label.append(label)

	


