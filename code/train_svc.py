# -*- coding: utf-8 -*-

import nif_exchange_2019 as nif_exchange
from nif_exchange_2019 import HTML_DIR, TEST_DIR, creator_counts, non_fic_counts
import os
from collections import defaultdict
import pickle
from text_utils import *
from sklearn import svm
from string import ascii_letters as ASCII_LETTERS
from histogram_utils import HistogramTokensWithFilter, HistogramNgramsWithFilter, DivideHistogram, DotDivide, ConcatenateHistograms, printHist
import numpy as np

# ======================= Some preprocessing ========================= #
ficcer_counts = {}
for creator in creator_counts:
	ct = creator_counts[creator]
	if creator in non_fic_counts:
		ct = creator_counts[creator] - non_fic_counts[creator]
	if ct > 0:
		ficcer_counts[creator] = ct 
creators = ficcer_counts.keys()


# ========================= Big util functions ========================= #
def SpecialTrigramHistogram(tokens):
	hist = HistogramNgramsWithFilter(tokens, n=3, keep=lambda tok: (TokenIsPunctuation(tok) or TokenIsTag(tok)) and not TokenIsBlacklisted(tok))
	return hist


def ProperNameHistogram(tokens):
	hist_all = HistogramNgramsWithFilter(tokens, n=3)
	hist = defaultdict()
	for ngram in hist_all:
		if ngram.lower() != 's huge' and ngram.lower() != 'did i' and IsWhitelistedName(ngram):
			hist['NAME_' + ngram] = hist_all[ngram]
	return hist


def GetFicTense(tokens):
	hist = HistogramNgramsWithFilter(tokens, n=1, keep=lambda x: x == 'says' or x == 'said')
	if hist['says'] > hist['said']:
		return 'PRESENT'
	elif hist['said'] > hist['says']:
		return 'PAST'
	else:
		return 'UNCLEAR'


def TitleFeatures(title):
	features = defaultdict(int)
	utitle = title

	# Is title all lowercase
	if IsLowercase(utitle):
		features['title_lowercase'] = 1

	# Is title capital-first, then lowercase
	is_sentence_case = False
	i = FirstAlphaIndex(utitle)
	if i is not None and utitle[i].isupper() and IsLowercase(utitle[i + 1:]):
		features['title_sentencecase'] = 1

	# Is title properly capitalized	
	if IsTitlecase(utitle):
		features['title_titlecase'] = 1

	# # Does title contain CJK characters
	# if HasUnicode(utitle):
	# 	features['title_unicode'] = 1

	# # Does title contain numbers
	# if HasNumerals(utitle):
	# 	features['title_numerals'] = 1
	
	# Histogram punctuation
	for c in utitle:
		if TokenIsPunctuation(c) and c not in '()\'':
			features['title_other_punct'] += 1
		elif c == '(':
			features['('] += 1
		elif c == ')':
			features[')'] += 1

	return features


def Bag(hist):
	reduced_hist = dict([(k,v) for k,v in hist.items() if v != 0])
	return DotDivide(reduced_hist, reduced_hist)


def ReduceFeatures(train_features, test_feature_set):
	# Zero out features that aren't in the test set
	for featname in train_features:
		if featname not in test_feature_set:
			train_features[featname] = 0.0

	return train_features


def ExtractAllFeatures(directory, title):
	title_feature_bow = Bag(TitleFeatures(title))
	
	f = open(os.path.join(directory, title), 'r')
	raw_contents = f.read()
	f.close()
	tokens = TokenizeHtml(raw_contents)
	special_token_bow = Bag(SpecialTrigramHistogram(tokens))
	proper_name_bow =  Bag(ProperNameHistogram(tokens))
	tense = GetFicTense(tokens)

	features_dict = {}
	features_dict['tense_' + tense] = 1.0
	features_dict = ConcatenateHistograms(features_dict, title_feature_bow)
	features_dict = ConcatenateHistograms(features_dict, special_token_bow)
	features_dict = ConcatenateHistograms(features_dict, proper_name_bow)
	return features_dict


def FeatureIndices(creator_dicts, test_dict):
	all_feature_names = set()
	for creator_dict in creator_dicts.values():
		for work_dict in creator_dict.values():
			for featname in work_dict.keys():
				all_feature_names.add(featname)
	for work_dict in test_dict.values():
		for featname in work_dict:
			all_feature_names.add(featname)
	return dict(zip(list(all_feature_names), range(len(all_feature_names))))


def GetMatrixFromDict(creator_dict, feature_idxs):
	"""Rows are works, columns are features"""
	featvects = np.zeros([len(creator_dict), len(feature_idxs)])
	titles = []
	for title, i in zip(creator_dict.keys(), range(len(creator_dict))):
		featdict = creator_dict[title]
		titles.append(title)
		for featname, value in featdict.items():
			if featname in feature_idxs:
				j = feature_idxs[featname]
				featvects[i][j] = value
	return featvects, titles


def GetAllCreatorFeatures(test_feature_set):
	all_creator_features = {}
	for creator in creators:
		all_creator_features[creator] = {}
		creator_dir = os.path.join(HTML_DIR, creator)
		for title in os.listdir(creator_dir):
			print(title)
			if (title.startswith('.')):
				continue
			features_dict = ExtractAllFeatures(creator_dir, title)
			features_dict = ReduceFeatures(features_dict, test_feature_set)
			all_creator_features[creator][title] = features_dict
	return all_creator_features

def TrainMulticlass(all_creator_features, feature_idxs):
	X_list = []
	Y_list = []
	title_order = []
	for creator in all_creator_features:		
		if not all_creator_features[creator]:
			print('No English fics')
			continue

		positives, titles = GetMatrixFromDict(all_creator_features[creator], feature_idxs)
		title_order = title_order + titles
		X_list.append(positives)
		Y_list.append(np.array(positives.shape[0] * [creator,]))

	X = np.vstack(X_list)
	# Normalize feature vectors (across 2nd dimension)
	feat_norms = np.sqrt(np.sum(X * X, axis=1))
	X = X / feat_norms[:, None]

	Y = np.hstack(Y_list)

	classifier = svm.SVC(kernel='rbf', class_weight='balanced')
	classifier = classifier.fit(X, Y)

	# Test on training set
	Z = classifier.predict(X)
	print(sum(Y == Z), '/', len(Y))

	return classifier
		


if __name__ == '__main__':
	from nif_exchange_2019 import CREATOR_FEATURES_PICKLE, TEST_FEATURES_PICKLE, FIDXS_PICKLE, MULTI_CLASSIFIER_PICKLE

	# test_features = {}
	# for title in os.listdir(TEST_DIR):
	# 	print(title)
	# 	if (title.startswith('.')):
	# 		continue
	# 	features_dict = ExtractAllFeatures(TEST_DIR, title)
	# 	test_features[title] = features_dict
	# pickle.dump(test_features, open(TEST_FEATURES_PICKLE, 'wb'))
	test_features = pickle.load(open(TEST_FEATURES_PICKLE, 'rb'))
	test_feature_set = set()
	for work_hist in test_features.values():
		test_feature_set = test_feature_set.union(work_hist.keys())

	# feature_idxs = FeatureIndices({}, test_features)
	# pickle.dump(feature_idxs, open(FIDXS_PICKLE, 'wb'))
	feature_idxs = pickle.load(open(FIDXS_PICKLE, 'rb'))

	print(len(feature_idxs), 'features')
	# all_creator_features = GetAllCreatorFeatures(test_feature_set)
	# pickle.dump(all_creator_features, open(CREATOR_FEATURES_PICKLE, 'wb'))
	all_creator_features = pickle.load(open(CREATOR_FEATURES_PICKLE, 'rb'))

	classifier = TrainMulticlass(all_creator_features, feature_idxs)	
	pickle.dump(classifier, open(MULTI_CLASSIFIER_PICKLE, 'wb'))
	classifier = pickle.load(open(MULTI_CLASSIFIER_PICKLE, 'rb'))

	# Get predictions
	X, titles = GetMatrixFromDict(test_features, feature_idxs)
	feat_norms = np.sqrt(np.sum(X * X, axis=1))
	X = X / feat_norms[:, None]

	y = classifier.predict(X)
	for t, l in zip(titles, y):
		print(t, ':', l)













