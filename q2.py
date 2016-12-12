
from q1 import cleanup
from q1 import read_data
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report
def run():
	nb = MultinomialNB()
	# make use of the cleanup and read_data from q1
	trainning,tests,dictionaries = cleanup(read_data("tweets.csv"))
	# Use data to fit the model
	nb.fit(trainning['features'], trainning['classes'])
	print "------predicting------"
	y_pred = nb.predict(tests['features'])
	y_true = tests['classes']
	target_names = ['Clinton','Trump']
	print(classification_report(y_true, y_pred, target_names=target_names))