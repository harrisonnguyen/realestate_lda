import csv
import random
corpus = []
with open('realestate_data_coord.csv','r') as csv_file:
	reader = csv.DictReader(csv_file)
	for row in reader:
		if random.random()>0.995:
			description = row['descript']
			corpus.append(description)

#perform the tfidf
from sklearn.feature_extraction.text import TfidfVectorizer
tf = TfidfVectorizer(analyzer='word', min_df = 0, stop_words = 'english',encoding = 'latin-1')

tfidf_matrix = tf.fit_transform(corpus)
feature_names = tf.get_feature_names()

#write results to file
with open('realestate_tfidf.csv','wb') as csvfile:
	fieldnames = ['id','phrase','score']
	writer = csv.DictWriter(csvfile, fieldnames = fieldnames)
	writer.writeheader()
	doc_id = 0
	for doc in tfidf_matrix.todense():
		print "Document %d" %doc_id
		word_id = 0
		for score in doc.tolist()[0]:
			if score > 0:
				word = feature_names[word_id]
				writer.writerow({'id': doc_id, 'phrase': word.encode("utf-8"), 'score': score})
			word_id +=1
		doc_id +=1

