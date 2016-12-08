# Name: Jinbo HE
# CS5100 project 3 question 1
####################################
# funtion implementation
import csv
def read_data(file):
	reader = csv.reader(open(file), delimiter=',')
	output = list()
	included_cols = [1,2]
	for row in reader:
		content = list(row[i] for i in included_cols)
		output.append(content)

	output = output[1:] # delete the first item as it is not a data item
 	return output
	

def cleanup(data):
	# let 0 represent Clinton
	# let 1 represent Trump
	def cleanupHelper(element):
		# 1st field: allocate a value to corresponding person
		if (element[0] == "HillaryClinton"):
			element[0] = 0
		elif (element[0] == "realDonaldTrump"):
			element[0] = 1
		return element
		# 2nd field: cleanup the words
		

	map (cleanupHelper, data)
	print data[0],data[-1]
	


	return 0

def train():
	return 0


def evaluation():
	return 0

def predict():
	return 0

#####################################
# run this file 
cleanup(read_data("tweets.csv"))

