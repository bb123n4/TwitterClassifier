# Name: Jinbo HE
# CS5100 project 3 question 1
####################################
# funtion implementation
import csv
import re
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
                handle = element[0]
                text = element[1]
		# 1st field: allocate a value to corresponding person
		
		if (handle == "HillaryClinton"):
			handle = 0
		elif (handle == "realDonaldTrump"):
			handle = 1
		
		# 2nd field: cleanup the words
                text = re.sub('https://[^ ]+',' ',text)
                text = re.sub('(#|@)[^ ]*',' ',text)   
                text = re.sub('[^a-zA-Z0-9_\']', ' ', text)
                text = re.sub('(\s|^)\'', ' ', text)
                text = re.sub('\'\s', ' ', text)
                text = re.sub('\s\s+', ' ', text)
                text = text.lower()
                
                element[0] = handle
                element[1] = text
                return element
        
	map (cleanupHelper, data)
	print data[-1]
	stop_words = ['a','0']
	# just use the frist 5000 twitters as trainning set
	dictionary = (''.join([x[1] for x in data[:4999]])).split()
	dictionary.sort()
	# filtering data if it is in the stop_words list
	dictionary = filter(lambda x: x not in stop_words, dictionary)
	
	print dictionary[0:2000]
	
	


	return data

def train():
	return 0


def evaluation():
	return 0

def predict():
	return 0

#####################################
# run this file 
result = cleanup(read_data("tweets.csv"))

