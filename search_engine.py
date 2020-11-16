import pandas as pd
import numpy as np
from indexer import Index, getDefDict
from collections import Counter, defaultdict
from math import sqrt
import pickle
import os

class Engine:
	def __init__(self, collection):
		self.index = collection
		self.terms = []
		self.max_results = 5
		self.set_dims(collection)

	def set_dims(self, collection):
		for term in self.index.vocabulary:
			self.terms.append(term)

	def cosine_sim(self, doc1, doc2):
		key_set1 = set(doc1.keys())
		key_set2 = set(doc2.keys())
		key_set = key_set1.union(key_set2)

		dot_prod = 0
		for key in key_set:
			dot_prod += (doc1[key]*doc2[key])
		mag1 = 0
		for key in key_set1:
			mag1 += doc1[key]**2
		mag1 = sqrt(mag1)
		mag2 = 0
		for key in key_set2:
			mag2 += doc2[key]**2
		mag2 = sqrt(mag2)

		sim = dot_prod/(mag1*mag2)
		return sim

	def vectorize_doc(self, doc_dict):
		doc_vec = defaultdict(int)
		max_freq = max(list(doc_dict.values()))
		for term in doc_dict:
			term_freq = doc_dict[term]/max_freq
			idf = self.index.get_idf(term)
			doc_vec[term] = term_freq*idf
		return doc_vec

	def format_query(self, query_tokens):
		q_freq = dict(Counter(query_tokens))
		max_freq = max(list(q_freq.values()))
		q_vec = defaultdict(int)
		for term in q_freq:
			term_freq = q_freq[term]/max_freq
			idf = self.index.get_idf(term)
			q_vec[term] = term_freq*idf
		return q_vec

	def search(self, query_doc):
		filtered_query = self.index.pre_process_doc(query_doc)
		formatted_query = self.format_query(filtered_query)
		query_res = []
		for doc_name in self.index.doc_rep:
			doc = self.index.doc_rep[doc_name]
			doc_vec = self.vectorize_doc(doc)
			sim = self.cosine_sim(doc_vec, formatted_query)
			query_res.append((sim, doc_name))

		query_res.sort()

		# return last 'max_results' results
		return query_res[-self.max_results:]

def load_collection(file='index.pickle'):
	if os.path.isfile(file):
		f = open(file, 'rb')
		collection = pickle.load(f)
		f.close()
		return collection
	else:
		print('No index found. Create index by running indexer.py file.')


if __name__ == '__main__':
	collection = load_collection()
	search_engine = Engine(collection)

	query = input('Search Engine\nQuery: ')
	while query != 'exit':
		result = search_engine.search(query)
		for res in result:
			print(res[1])
		query = input('Query: ')