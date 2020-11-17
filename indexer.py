import pandas as pd
import numpy as np
import os
import pickle
from collections import defaultdict
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from collections import Counter
from math import log

en_stop = set(stopwords.words('english'))

def getDefDict():
	return defaultdict(int)

class Index:
	def __init__(self):
		self.lemmatizer = WordNetLemmatizer()
		self.docs = {}
		self.vocabulary = {}
		self.doc_rep = defaultdict(getDefDict)
		self.postings = defaultdict(getDefDict)


	def get_corpus_size(self):
		return len(self.docs)

	def get_vocab_size(self):
		return len(self.vocabulary)

	def pre_process_doc(self, doc):
		tokens = word_tokenize(doc)
		cleaned_tokens = [w.lower() for w in tokens if w.lower() not in en_stop]
		lem_tokens = [self.lemmatizer.lemmatize(token) for token in cleaned_tokens]
		return lem_tokens

	def update_index(self, tokens, doc):
		#Add token to the vocabulary and set dimension number
		for token in tokens:
			if token not in self.vocabulary:
				self.vocabulary[token] = self.get_vocab_size() + 1
		
		#Add doc to the corpus and give dimension to doc
		if doc not in self.docs:
			self.docs[doc] = self.get_corpus_size() + 1
		
		#Update posting list
		token_set = set(tokens)
		for token in token_set:
			self.postings[token][doc] += 1

		#Update doc representation
		term_freq = dict(Counter(tokens))
		for uq_token in term_freq:
			self.doc_rep[doc][uq_token] += term_freq[uq_token]

	def create_index(self):
		location = '/home/mukund/Documents/College/Sem-IX/IR/Films'
		movie_data = pd.read_csv(location+'/movies.csv', header=0)
		iteration = 0
		for index, row in movie_data.iterrows():
			iteration += 1

			# #Smaller set
			# if(iteration > 10):
			# 	break

			lines = []
			with open(row['location'], 'r') as f:
				lines = f.readlines()

			if not len(lines):
				return

			init_doc = ' '.join(lines)
			filtered_tokens = self.pre_process_doc(init_doc)
			self.update_index(filtered_tokens, row['url'])
		return

	def get_tf(self, term, doc):
		freq = self.doc_rep[doc][term]
		doc_dict = self.doc_rep[doc]
		max_freq = max(list(doc_dict.values()))
		if not freq:
			return 0
		return freq/max_freq

	def get_midf(self, term):
		dfr = len(self.postings[term])
		ctf = sum(list(self.postings[term].values()))
		return dfr/ctf

	def get_idf(self, term):
		return log(len(self.docs)/len(self.postings[term]))

	def get_tfidf(self, term, doc):
		tf = self.get_tf(term, doc)
		idf = self.get_idf(term)
		return tf*idf

	def print(self):
		print(self.get_corpus_size())
		print(self.get_vocab_size())
		print(dict(self.postings))
		print(dict(self.doc_rep))

def dump_index(collection):
	with open('index.pickle', 'wb') as f:
		pickle.dump(collection, f)

if __name__ == '__main__':
	movie_index = Index()
	movie_index.create_index()
	movie_index.print()
	dump_index(movie_index)