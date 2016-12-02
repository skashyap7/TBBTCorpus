from json import loads

"""
	Maximum entroy trainer : Uses scikit learn Logistic Regression module
"""
class MaxEnt:

	# Constructor
	def __init__(self):
		self.train_data = []
		self.train_label= []
		self.test_data  = []
		self.test_label = []

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


		print(content["1_1"])
		for seasons in content:
			season_num = int(seasons[:-2])
			print(seasons)

			turns = content[seasons][1]["Turns"]
			for turn in turns:
				tokens = [word[0] for word in turn["Words"]]
				label  = turn["Speaker"]
				if season_num <= 8:
					self.train_data.append(tokens)
					self.train_label.append(label)
				else:
					self.test_data.append(tokens)
					self.test_label.append(label)
			return



		

trainer = MaxEnt()
trainer._parserTrain("/Users/rakshithr/Desktop/MaxEnt/MaxEnt/final.json")
