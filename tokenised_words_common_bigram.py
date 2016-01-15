from sklearn.feature_extraction.text import CountVectorizer
import csv
import nltk
from num2words import num2words
import re


def check_tuples(tagged_words):
	new_list = []
	i = 0
	if len(tagged_words) < 3:
		for words in tagged_words:
			new_list.append(words)
		return new_list
	while i <  len(tagged_words):
		if i == 0:
			current_word = tagged_words[i]
			next_word = tagged_words[i+1]
			next_next_word = tagged_words[i+2]
			if current_word in common_adjectives:
				bigram = current_word + '_' + next_word
				#trigram = bigram + '_' + next_next_word
				new_list.append(bigram)
				#new_list.append(trigram)
				i+=2
			elif current_word in common_nouns:
				bigram = current_word + '_' + next_word
				new_list.append(bigram)
				i+=2
			else:
				new_list.append(current_word)
				i+=1
		elif i == len(tagged_words)-2:	
			previous_word = tagged_words[i-1]
			current_word = tagged_words[i]
			next_word = tagged_words[i+1]
			if current_word in common_adjectives:
				bigram = current_word + '_' + next_word
				new_list.append(bigram)
				i+=2
			elif current_word in common_nouns:
				bigram = current_word + '_' + next_word
				#trigram = previous_word + '_' + bigram
				new_list.append(bigram)
				bigram = previous_word + '_' + current_word
				new_list.append(bigram)
				#new_list.append(trigram)
				i+=2
			else:
				new_list.append(current_word)
				i+=1
		elif i == len(tagged_words)-1:
			current_word = tagged_words[i]
			new_list.append(current_word)
			i+=1
		else:
			previous_word = tagged_words[i-1]
			current_word = tagged_words[i]
			next_word = tagged_words[i+1]
			#next_next_word = tagged_words[i+2]			
			if current_word in common_adjectives:
				bigram = current_word + '_' + next_word
				#trigram = bigram + '_' + next_next_word
				new_list.append(bigram)
				#new_list.append(trigram)
				i+=2
			elif current_word in common_nouns:
				bigram = current_word + '_' + next_word
				#trigram = previous_word + "_" + bigram
				new_list.append(bigram)
				#new_list.append(trigram)
				bigram = previous_word + '_' + current_word
				new_list.append(bigram)
				i+=2
			else:
				new_list.append(current_word)
				i+=1
	return new_list
	
	
def convert_num(number):
	word = ''
	try:
		#convert the number to an integer
		number = int(number)
		word = num2words(number)
	except ValueError:
		word = None
	return word
			
	

#import the stopword list
from sklearn.feature_extraction import text
removed = set(['one','two','three','four','five','six','seven','eight','nine','ten', 'eleven', 'twelve','fifteen','twenty','fifty','hundred'])
stop_words = text.ENGLISH_STOP_WORDS.difference(removed)
added = set(['approx','sqm'])
stop_words = stop_words.union(added)

#import the common nouns from file
common_nouns_file = open('common_nouns.txt','r')
common_nouns = []
for line in common_nouns_file:
	common_nouns.append(line.strip("\n").strip(" "))

common_adjectives_file = open('common_adjectives.txt','r')
common_adjectives = []
for line in common_adjectives_file:
	common_adjectives.append(line.strip("\n").strip(" "))


#create the tokeniser
vectorizer = CountVectorizer(min_df=1, encoding = 'latin-1',decode_error = 'ignore',stop_words = stop_words,token_pattern='[A-Za-z]{1,}')
analyze = vectorizer.build_analyzer()
with open('realestate_data_coord.csv','r') as csvfile:
	reader = csv.DictReader(csvfile)
	x = 0
	for i in range(0,1):
	#for row in reader:
		#if x < 5889:
		#	x +=1
		#	continue
		#else:
		if x %1000 == 0:
			print x
		row = reader.next()
		description = row['descript']
		#tokens = nltk.word_tokenize(description)
		tokens = analyze(description)
		#text = word_tokenize(description)
		list = check_tuples(tokens)
		#write to file
		writer = open('text_common_trigrams2/' + str(x)+'.txt','w')
		for words in list:
			writer.write(words.encode("utf-8") + " ")
		writer.close()
		x +=1
csvfile.close()
