# -*- coding: utf-8 -*-

import nif_exchange_2022 as nif_exchange
from nif_exchange_2022 import HTML_DIR, TEST_DIR, creator_counts
import os
from collections import defaultdict
import pickle
from text_utils import *
from string import ascii_letters as ASCII_LETTERS
from histogram_utils import HistogramTokensWithFilter, HistogramNgramsWithFilter, DivideHistogram, DotDivide, ConcatenateHistograms, printHist
import numpy as np
import nltk
from nltk.lm.preprocessing import padded_everygram_pipeline


if __name__ == '__main__':
	from nif_exchange_2022 import LMS_PICKLE, POSSIBILITIES_PICKLE, TOKENIZED_PICKLE
	import pickle

	NGRAM_LEVEL = 3
	creators = creator_counts.keys()


	# Tokenize each work
	all_tokenized = {}
	for creator in creators:
		all_tokenized[creator] = {}
		lm = nltk.lm.MLE(NGRAM_LEVEL)
		creator_dir = os.path.join(HTML_DIR, creator)

		# Create tokenized training data
		for title in os.listdir(creator_dir):
			if (title.startswith('.')):
				continue
			print('Tokenizing', title)

			fname = title
			raw_contents = open(os.path.join(creator_dir, fname), 'r').read()
			all_tokenized[creator][title] = TokenizeWork(title, raw_contents)

	pickle.dump(all_tokenized, open(TOKENIZED_PICKLE, 'wb'))
	all_tokenized = pickle.load(open(TOKENIZED_PICKLE, 'rb'))

	# Train language models
	all_creator_models = {}
	for creator in creators:
		print('Fitting', creator)
		
		# Create tokenized training data
		tokenized_works = []
		for title, body in all_tokenized[creator].values():
			tokenized_works.append(title)
			tokenized_works.append(body)
		train, vocab = padded_everygram_pipeline(NGRAM_LEVEL, tokenized_works)
		
		lm = nltk.lm.StupidBackoff(order = NGRAM_LEVEL)
		lm.vocab = nltk.lm.Vocabulary(unk_cutoff = 2)
		lm.fit(train, vocab)
		all_creator_models[creator] = lm
	pickle.dump(all_creator_models, open(LMS_PICKLE, 'wb'))
	all_creator_models = pickle.load(open(LMS_PICKLE, 'rb'))


	creator = 'zandalorian'
	print('Testing', creator)
	creator_lm = all_creator_models[creator]
	for title in all_tokenized[creator].keys():
		work = all_tokenized[creator][title]
		test, vocab = padded_everygram_pipeline(NGRAM_LEVEL, work)
		test_ngrams = [[tt for tt in t] for t in test]
		test_ngrams = test_ngrams[0] + test_ngrams[1]
		entropy = creator_lm.entropy(test_ngrams)
		print(title, ':', entropy)
	print('Others')
	for cc in creators:
		if cc == creator:
			continue
		for title in all_tokenized[cc]:
			work = all_tokenized[cc][title]
			test, vocab = padded_everygram_pipeline(NGRAM_LEVEL, work)
			test_ngrams = [[tt for tt in t] for t in test]
			test_ngrams = test_ngrams[0] + test_ngrams[1]
			entropy = creator_lm.entropy(test_ngrams)
			print(title, ':', entropy)


		














