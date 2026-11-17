# -*- coding: utf-8 -*-

import nif_exchange_2019 as nif_exchange
from nif_exchange_2019 import HTML_DIR, TEST_DIR
import os
import unicodedata
from collections import defaultdict
import pickle
from text_utils import MaybeNormalizeTag

def HistogramTokens(tokens):
	HistogramTokensWithFilter(tokens)

def HistogramTokensWithFilter(tokens, keep=lambda x: True):
	hist = defaultdict(int)
	for token in tokens:
		if keep(token):
			ntoken = MaybeNormalizeTag(token)
			hist[ntoken] += 1
	return hist


def HistogramNgramsWithFilter(tokens, n=1, max_ngrams_only=False, keep=lambda x: True):
	hist = defaultdict(int)
	
	# Start at nth token
	for i in range(len(tokens)):
		for m in range(n-1, 0, -1):
			# n = 1 -> m = 0 -> m+1 = 1 -> j = 0; n = 4 -> m = 3 -> m+1 = 4 -> j = 0...3
			if all(keep(tokens[i - j]) for j in range(min(i, m + 1))):
				ngram_name = ' '.join([MaybeNormalizeTag(tokens[i - j]) for j in range(m, -1, -1)])
				hist[ngram_name] += 1
				if max_ngrams_only:
					break

	return hist


def AddHistograms(hist1, hist2):
	sums = hist1
	for key in hist2:
		sums[key] += hist2[key]
	return sums

def DivideHistogram(hist, denom):
	result = hist
	for key in hist:
		result[key] = float(hist[key])/denom
	return result

def DotDivide(numers, denoms):
	result = numers
	for key in numers:
		result[key] = float(numers[key]/denoms[key])
	return result

def DotMultiply(hist1, hist2):
	result = defaultdict(int)
	for tok in hist1:
		if tok in hist2:
			result[tok] = hist1[tok] * hist2[tok]
	return result

def DotProduct(hist1, hist2):
	return sum(hist1[tok] * hist2[tok] for tok in hist1)

def ConcatenateHistograms(hist1, hist2):
	hist3 = hist1
	hist3.update(hist2)
	return hist3

def printHist(hist, lead=50, bottom=False):
	skeys = sorted(hist.keys(), key=lambda x:hist[x], reverse=True)
	for key in skeys[:lead]:
#		print(key.encode('utf-8'), ':\t', hist[key])
		print(key, ':\t', hist[key])
	if not bottom:
		print(len(hist))
		return

	for _ in range(3):
		print('.')
	for key in skeys[0-lead:]:
#		print(key.encode('utf-8'), '\t\t', hist[key])
		print(key, '\t\t', hist[key])
	print(len(hist))


if __name__ == '__main__':
	creators = nif_exchange.creator_counts.keys()
	
	# Collect master token counts
	#master_counts = MasterCounts(creators)
	#printHist(master_counts)
	#pickle.dump(master_counts, open('master_counts.pickle', 'wb'))

	# Collect unigram freqs for each creator
	#creator_hists = CreatorHists(creators)
	#pickle.dump(creator_hists, open('unigram_freqs_by_creator.pickle', 'wb'))

	# creator_hists = pickle.load(open('unigram_freqs_by_creator.pickle', 'rb'))

	# Sum average document frequencies, where document = creator
	doc_freqs = defaultdict(int)
	for _, creator_hist in creator_hists.iteritems():
		for tok in creator_hist:
			doc_freqs[tok] += creator_hist[tok]
	stokens = sorted(doc_freqs.keys(), key = lambda x: doc_freqs[x], reverse=True)
	stopwords = stokens[:50]

	# Get punctuation and tag bags of words
	special_test_bows = special_test_hists
	for title in special_test_hists:
		for token in special_test_hists[title]:
			if special_test_hists[title][token] > 0:
				special_test_bows[title][token] = 1
	creator_bows = creator_hists
	for creator in creator_hists:
		for token in creator_hists[creator]:
			if creator_hists[creator][token] > 0:
				creator_bows[creator][token] = 1

	# Zero out stopwords
	for title in test_hists:
		for stopword in stopwords:
			test_hists[title][stopword] = 0

	# Dot product everything
	scores = dict(zip(test_hists.keys(), {}))
	for title, test_hist in test_hists.iteritems():
		dot_products = dict(zip(creator_hists.keys(), [0.0,]*len(creator_hists)))
		for creator, creator_hist in creator_hists.iteritems():
			prod = analyze_fics.DotProduct(test_hist, creator_hist)
			dot_products[creator] = prod
		scores[title] = dot_products
	pickle.dump(scores, open('pair_scores.pickle', 'wb'))
















