from sklearn.feature_extraction.text import CountVectorizer
import csv
import nltk
from num2words import num2words
import re


def check_tuples(tokens,tagged_words):
	new_list = []
	i = 0
	while i <  len(tagged_words)-1:
		current_tuple = tagged_words[i]
		next_tuple = tagged_words[i+1]
		#print current_tuple, next_tuple
		next_word = next_tuple[0]
		if next_word in common_words:
			current_tag = current_tuple[1]
			if current_tag == 'JJ' or current_tag == 'VBG' or current_tag == 'VBD' or current_tag == 'NN':
				new_list.append(current_tuple[0] + "_" + next_word)
				i += 2
			elif current_tag == 'CD':
				word = convert_num(current_tuple[0])
				if word is None:
					new_list.append(current_tuple[0] + "_" + next_word)
				else:
					new_list.append(word + '_' + next_word)
				i+=2
			else:
				new_list.append(current_tuple[0])
				i+=1
		elif 'condition' in next_word and current_tuple[0] == 'air':
			new_list.append(current_tuple[0] + '_' + next_word)
			i+=2
		else: 
			new_list.append(current_tuple[0])
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

#import the common nouns from file
common_words_file = open('common_nouns.txt','r')
common_words = []
for line in common_words_file:
	common_words.append(line.strip("\n"))


#create the tokeniser
vectorizer = CountVectorizer(min_df=1, encoding = 'latin-1',decode_error = 'ignore',stop_words = stop_words,token_pattern='[A-Za-z]{2,}|[0-9]{1,}')
analyze = vectorizer.build_analyzer()
with open('tokenised_descript.csv','wb') as csvwrite:
	fieldnames = ['house_id','description']
	writer = csv.DictWriter(csvwrite,fieldnames = fieldnames)
	writer.writeheader()

	x = 0
	with open('realestate_data_coord.csv','r') as csvfile:
		reader = csv.DictReader(csvfile)
		for i in range(0,1):
			row = reader.next()
			description = row['descript']
			#tokens = nltk.word_tokenize(description)
			tokens = analyze(description)
			#text = word_tokenize(description)
			tagged_words = nltk.pos_tag(tokens)
			list = check_tuples(tokens,tagged_words)
			#write to file
			writer = open(str(x)+'.txt','w')
			for words in list:
				if (not bool(re.search(r'\d',words))) and (len(words) > 2):
					writer.write(words.encode("utf-8") + " ")
			writer.close()
			x +=1

			#paragraph = []
			#for words in tokens:
			#	encoded_word = words.encode("utf-8")
			#	paragraph.append(encoded_word)
			#writer.writerow({'house_id': x, 'description': paragraph})
			#x+=1
csvwrite.close()