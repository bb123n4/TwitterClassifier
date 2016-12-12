# Name: Jinbo HE
# CS5100 project 3 question 1
####################################
# funtion implementation
from __future__ import division
import csv # package for dealing with csv file
import re  # package for regex
import numpy # package for numpy
from collections import OrderedDict # package for ordered dictionary
from collections import Counter # package for counter object
from sklearn.metrics import classification_report # package for showing evaluation report

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
	def cleanupHelper(element):
		handle = element[0]
		text = element[1]
		# 1st field: allocate a value to corresponding person
		# let 0 represent Clinton
		# let 1 represent Trump
		
		if (handle == "HillaryClinton"):
			handle = 0
		elif (handle == "realDonaldTrump"):
			handle = 1
		
		# 2nd field: cleanup the words using regex
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
	# map the cleanhelper to each data item
	map (cleanupHelper, data)
	
	# reference from http://www.lextek.com/manuals/onix/stopwords1.html
	stop_words = ['a','about','above','across','after','again','against','all','almost','alone','along','already',
				 'also','although','always','among','an','and','another','any','anybody','anyone','anything','anywhere','are','area',
				 'areas','around','as','ask','asked','asking','asks','at','away','b','back','backed','backing','backs','be','became','because',
				 'become','becomes','been','before','began','behind','being','beings','best','better','between','big','both','but','by','c','came','can',
				 'cannot','case','cases','certain','certainly','clear','clearly','come','could','d','did','differ','different','differently','do','does','done',
				 'down','down','downed','downing','downs','during','e','each','early','either','end','ended','ending','ends','enough','even','evenly',
				 'ever','every','everybody','everyone','everything','everywhere','f','face','faces','fact','facts','far','felt','few','find','finds','first',
				 'for','four','from','full','fully','further','furthered','furthering','furthers','g','gave','general','generally','get','gets','give','given',
				 'gives','go','going','good','goods','got','great','greater','greatest','group','grouped','grouping','groups','h','had','has','have','having','he',
				 'her','here','herself','high','high','high','higher','highest','him','himself','his','how','however','i','if','important','in','interest','interested',
				 'interesting','interests','into','is','it','its','itself','j','just','k','keep','keeps','kind','knew','know','known','knows','l','large','largely','last',
				 'later','latest','least','less','let','lets','like','likely','long','longer','longest','m','made','make','making','man','many','may','me','member','members',
				 'men','might','more','most','mostly','mr','mrs','much','must','my','myself','n','necessary','need','needed','needing','needs','never','new','new','newer',
				 'newest','next','no','nobody','non','noone','not','nothing','now','nowhere','number','numbers','o','of','off','often','old','older','oldest','on','once',
				 'one','only','open','opened','opening','opens','or','order','ordered','ordering','orders','other','others','our','out','over','p','part','parted','parting',
				 'parts','per','perhaps','place','places','point','pointed','pointing','points','possible','present','presented','presenting','presents','problem','problems',
				 'put','puts','q','quite','r','rather','really','right','right','room','rooms','s','said','same','saw','say','says','second','seconds','see','seem','seemed',
				 'seeming','seems','sees','several','shall','she','should','show','showed','showing','shows','side','sides','since','small','smaller','smallest','so','some',
				 'somebody','someone','something','somewhere','state','states','still','still','such','sure','t','take','taken','than','that','the','their','them','then',
				 'there','therefore','these','they','thing','things','think','thinks','this','those','though','thought','thoughts','three','through','thus','to','today',
				 'together','too','took','toward','turn','turned','turning','turns','two','u','under','until','up','upon','us','use','used','uses','v','very','w','want',
				 'wanted','wanting','wants','was','way','ways','we','well','wells','went','were','what','when','where','whether','which','while','who','whole','whose','why',
				 'will','with','within','without','work','worked','working','works','would','x','y','year','years','yet','you','young','younger','youngest','your','yours','z']
	# use a threshold to divide trainning set and tests set
	threshold = 3999
	trainning_data = data[0:threshold]
	print "------Constructing Dictionary------"
	# constructing dictionaries for overall,trump and clinton
	trump_dict = ''
	clinton_dict = ''
	dictionary = (' '.join([x[1] for x in trainning_data])).split()
	for x in trainning_data:
		if (x[0] == 1):
			trump_dict = trump_dict + ' ' + x[1]
		else:
			clinton_dict = clinton_dict + ' ' + x [1]
	trump_dict = trump_dict.split()
	clinton_dict = clinton_dict.split()
	dictionary.sort()

	# filtering data if it is in the stop_words list
	dictionary = filter(lambda x: x not in stop_words, dictionary)
	trump_dict = filter(lambda x: x not in stop_words, trump_dict)
	clinton_dict = filter(lambda x: x not in stop_words, clinton_dict)

	dict_counts = OrderedDict()
	trump_counts = OrderedDict()
	clinton_counts = OrderedDict()

	for words in dictionary:
		dict_counts[words] = dict_counts.get(words,0) + 1
		trump_counts[words] = trump_counts.get(words,0)
		clinton_counts[words] = clinton_counts.get(words,0)
	for words in trump_dict:
		trump_counts[words] = trump_counts.get(words,0) + 1
	for words in clinton_dict:
		clinton_counts[words] = clinton_counts.get(words,0) + 1

	keys = dict_counts.keys()
	values = dict_counts.values()
	print "Construction Complete!"

     
	def normalize(element):
		# normalize the data to features, i.e. times the word(included in the overall dictionray) 
		# appear in the input text
		text = element[1]
		norm = [0] * len(keys)
		for word in (text.split()):
			if word in keys:
				norm[keys.index(word)] += 1
		element[1] = norm
	print '------Normalizing data------'
	
	map (normalize, data)

	print 'Normalizing Complete!'
	
	# convert different data sets to numpy for further calculations
	trainning_data = data[0:threshold]
	trainning_classes = list()
	trainning_features = list()
	for i in trainning_data:
		trainning_classes.append(i[0])
		trainning_features.append(i[1])

	trainning_classes = numpy.asarray(trainning_classes)	
	trainning_features = numpy.asarray(trainning_features)


	test_data = data[(threshold+1):]
	tests_features = list()
	tests_classes = list()
	for x in test_data:
		tests_features.append(x[1])
		tests_classes.append(x[0])
	tests_classes = numpy.asarray(tests_classes)	
	tests_features = numpy.asarray(tests_features)

	# pack values for output
	trainning = {'classes':trainning_classes,'features':trainning_features}
	tests = {'classes':tests_classes,'features':tests_features}
	dictionaries = {'overall':dict_counts,'trump':trump_counts,'clinton':clinton_counts}

	return trainning,tests,dictionaries

def train(trainning,dictionaries):
	# this function is resiponsible for calculating
	#  P(Trump) P(Clinton) P(features) P(features|Trump) P(features|Clinton)
	#  while P(features) P(features|Trump) P(features|Clinton) are lists
	#  keep every corresponding feature probability
	dict_keys = dictionaries['overall'].keys()
	dict_values = dictionaries['overall'].values()
	trump_values = dictionaries['trump'].values()
	clinton_values = dictionaries['clinton'].values()

	classes = trainning['classes']
	classes_counter = Counter(classes)

	p_clinton = classes_counter[0] / len (classes)	# P(Clinton)
	p_trump = classes_counter[1] / len (classes)   # P(Clinton)
	
	p_features_clinton = list() # P(features|Clinton)
	p_features_trump = list() # P(features|Trump)
		
	sum_of_dict = sum(dict_values)
	sum_of_trump_dict = sum(trump_values)
	sum_of_clinton_dict = sum(clinton_values)
	p_features = [x / sum_of_dict for x in dict_values] #P(features)
	p_features_trump = [x/sum_of_trump_dict for x in trump_values] # P(features|Trump)
	p_features_clinton = [x/sum_of_clinton_dict for x in clinton_values] # P(features|Clinton)
	
	p_features = numpy.asarray(p_features)
	p_features_clinton = numpy.asarray(p_features_clinton)
	p_features_trump = numpy.asarray(p_features_trump)
	
	# pack those value for output
	model = {'p_features':p_features,'p_clinton':p_clinton,
			'p_trump':p_trump,'p_features_clinton':p_features_clinton,
			'p_features_trump':p_features_trump}

	return model


def evaluation(fact,result):
	print "The report of self-implemented NB:"
	print "**************************************************"
	print "Training Set: 4000 Items, Tests Set: 2444 Items"
	print "**************************************************"
	y_pred = result
	y_true = fact
	target_names = ['Clinton','Trump']
	print(classification_report(y_true, y_pred, target_names=target_names))
	return 0

def predict(data,model):
	print "------Predicting------"
	p_features = model['p_features']
	p_clinton = model['p_clinton']
	p_trump = model['p_trump']
	p_features_clinton = model['p_features_clinton']
	p_features_trump = model['p_features_trump']
	
	# calculate the probabilty for each classes:
	# Note: In this implementation, duplicate input words would be calculated multiple times
	#       For example: "pen pineapple apple pen", the corresponding feature pen would be calculated twice
	#                     the equation would be: P(c1 | pen,pen,pineapple,apple) 
	#                          				     = P(pen|c1) * P(pen|c1) * P(apple|c1) * P(pineapple|c1) * p(c1)/
	#                                              P(pen) * P(pen) * P(apple) * P (Pineapple)
	clinton_rate = (numpy.product(p_features_clinton ** data,axis = 1) * p_clinton) / (numpy.product (p_features ** data, axis=1))
	trump_rate = (numpy.product(p_features_trump ** data,axis = 1) * p_trump) / (numpy.product (p_features ** data,axis = 1))
	# choose the greater probability
	result = numpy.greater(trump_rate,clinton_rate)
	# Convert boolean to int representation
	result = result.astype(int) 

	return result

def run():
	trainning,tests,dictionaries = cleanup(read_data("tweets.csv"))
	model = train(trainning,dictionaries)
	evaluation(tests['classes'],predict(tests['features'],model))


	


