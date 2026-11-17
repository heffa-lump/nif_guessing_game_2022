# -*- coding: utf-8 -*-

import nif_exchange_2022 as nif_exchange
from nif_exchange_2022 import HTML_DIR, TEST_DIR, creator_counts
import os
from collections import defaultdict
import pickle
from text_utils import *
from sklearn import svm
from string import ascii_letters as ASCII_LETTERS
from histogram_utils import HistogramTokensWithFilter, HistogramNgramsWithFilter, DivideHistogram, DotDivide, ConcatenateHistograms, printHist
import numpy as np

prefixes = sorted(NAME_PREFIXES, key=lambda x: len(x), reverse=True)
prefixes = [p.lower() for p in prefixes]
name_whitelist = sorted(NAME_WHITELIST, key=lambda x: len(x), reverse=True)
name_whitelist = [n.lower() for n in name_whitelist]

# ======================= Small util functions ========================= #
creators = creator_counts.keys()

# ========================= Big util functions ========================= #
def SpecialTrigramHistogram(tokens):
	hist = HistogramNgramsWithFilter(tokens, n=3, keep=lambda tok: (TokenIsPunctuation(tok) or TokenIsTag(tok)) and not TokenIsBlacklisted(tok))

	# tag_higher_gram_blacklist = ['<em>', '</em>', '<b>', '</b>', '<i>', '</i>', u'’', u'“', u'”', u'"', u'\'']
	# for ngram in hist:
	# 	tokens = ngram.split()
		# # Eliminate bi and trigrams with <em> or </em>
		# if len(tokens) > 1 and any(tok in tag_higher_gram_blacklist for tok in tokens):
		# 	hist[ngram] = 0
		# # Eliminate mixed punctuation
		# if len(tokens) > 1 and all(TokenIsPunctuation(tok) for tok in tokens) and any(tok != tokens[0] for tok in tokens):
		# 	hist[ngram] = 0
		# # For some reason punctuation, tag doesn't seem that useful
		# if len(tokens) == 3 and TokenIsPunctuation(tokens[0]) and TokenIsTag(tokens[2]):
		# 	hist[ngram] = 0
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


def ReduceFeaturesAgain(features_by_title):
	if len(features_by_title) < 4:
		return features_by_title

	feature_counts = defaultdict(int)
	for features_dict in features_by_title.values():
		for featname in features_dict:
			if features_dict[featname] != 0:
				feature_counts[featname] += 1

	for title in features_by_title:
		for featname in features_by_title[title]:
			if feature_counts[featname] < 2:
				features_by_title[title][featname] = 0

	return features_by_title


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
	for featdict, i in zip(creator_dict.values(), range(len(creator_dict))):
		for featname, value in featdict.items():
			if featname in feature_idxs:
				j = feature_idxs[featname]
				featvects[i][j] = value
	return featvects


def InvertIndexVector(feature_idxs):
	idx_features = ['',] * len(feature_idxs)
	for f, i in feature_idxs.items():
		idx_features[i] = f
	return idx_features


def CheckForCollisions(creator_matrices):
	collisions = {}
	for creator1, m1 in creator_matrices.items():
		collisions[creator1] = []
		for creator2, m2 in creator_matrices.items():
			if creator1 == creator2:
				continue
			p = m1.dot(m2.transpose())
			s1 = m1.dot(np.ones(m2.transpose().shape))
			s2 = m2.dot(np.ones(m1.transpose().shape))
			s = np.maximum(s1, s2.transpose())
			if len(np.argwhere(p == s)):
				collisions[creator1].append(creator2)
	return collisions


def TrainAll(all_creator_features, feature_idxs):
	classifiers = {}
	# Train classifiers
	for creator in creators:
		print(creator)
		
		if not all_creator_features[creator]:
			print('  No English fics')
			continue

		positives = GetMatrixFromDict(all_creator_features[creator], feature_idxs)
		negatives = np.zeros([0, len(feature_idxs)])
		for ncreator in creators:
			if creator == ncreator:
				continue
			negatives = np.vstack([negatives, GetMatrixFromDict(all_creator_features[ncreator], feature_idxs)])
		X = np.vstack([positives, negatives])
		# Normalize feature vectors (across 2nd dimension)
		feat_norms = np.sqrt(np.sum(X * X, axis=1))
		X = X / feat_norms[:, None]

		labels = np.hstack([np.ones(positives.shape[0]), np.zeros(negatives.shape[0])])

		classifier = svm.LinearSVC(class_weight='balanced')
		classifier.fit(X, labels)
		classifiers[creator] = classifier

		# Sanity check
		all_training_features = {}
		for cf in all_creator_features.values():
			all_training_features = ConcatenateHistograms(all_training_features, cf)
		training_pred = Predict(classifier, all_training_features, feature_idxs)
		print(sum(1 for title in training_pred if training_pred[title] and title in all_creator_features[creator]),) 
		print('/', len(all_creator_features[creator]))
		print(sum(1 for title in training_pred if training_pred[title] and title not in all_creator_features[creator]),)
		print('/', len(training_pred) - len(all_creator_features[creator]))
	return classifiers


def GetClassifierScore(classifier, work_features):
	test_vector = GetMatrixFromDict({'anon' : work_features,}, feature_idxs)[0]
	return classifier.decision_function(test_vector.reshape(1, -1))


def Predict(classifier, test_features, feature_idxs):
	predictions = {}
	for title in test_features:		
		predictions[title] = GetClassifierScore(classifier, test_features[title])
	return predictions


def VectorHistogram(vector, feature_idxs):
	idx_features = InvertIndexVector(feature_idxs)
	hist = {}
	for i in range(len(vector)):
		if abs(vector[i]) > 1e-6:
			hist[idx_features[i]] = vector[i]
	return hist


def ExplainPrediction(classifier, work_features, feature_idxs):
	w = classifier.coef_[0]
	work_vector = GetMatrixFromDict({'test' : work_features,}, feature_idxs)[0]
	x = work_vector
	features_bias_idxs = feature_idxs.copy()
	features_bias_idxs['bias'] = len(feature_idxs)
	printHist(VectorHistogram(w * x, features_bias_idxs), lead=20, bottom=True)


if __name__ == '__main__':
	from nif_exchange_2022 import CREATOR_FEATURES_PICKLE, TEST_FEATURES_PICKLE, CLASSIFIERS_PICKLE, FIDXS_PICKLE, \
							 POSSIBILITIES_PICKLE, CLASSIFIER_SCORES_PICKLE

	# test_features = {}
	# for title in os.listdir(TEST_DIR):
	# 	print(title)
	# 	if (title.startswith('.')):
	# 		continue
	# 	features_dict = ExtractAllFeatures(TEST_DIR, title)
	# 	test_features[title] = features_dict
	# pickle.dump(test_features, open(TEST_FEATURES_PICKLE, 'wb'))
	test_features = pickle.load(open(TEST_FEATURES_PICKLE, 'rb'))

	# test_feature_set = set()
	# for work_hist in test_features.values():
	# 	test_feature_set = test_feature_set.union(work_hist.keys())
	# feature_idxs = FeatureIndices({}, test_features)
	# pickle.dump(feature_idxs, open(FIDXS_PICKLE, 'wb'))
	feature_idxs = pickle.load(open(FIDXS_PICKLE, 'rb'))

	# print(len(feature_idxs), 'features')

	# all_creator_features = {}
	# for creator in creators:
	# 	all_creator_features[creator] = {}
	# 	creator_dir = os.path.join(HTML_DIR, creator)
	# 	for title in os.listdir(creator_dir):
	# 		print(title)
	# 		if (title.startswith('.')):
	# 			continue
	# 		features_dict = ExtractAllFeatures(creator_dir, title)
	# 		features_dict = ReduceFeatures(features_dict, test_feature_set)
	# 		all_creator_features[creator][title] = features_dict
	# 		print(int(sum(features_dict.values())))
	# 	all_creator_features[creator] = ReduceFeaturesAgain(all_creator_features[creator])
	# pickle.dump(all_creator_features, open(CREATOR_FEATURES_PICKLE, 'wb'))

	all_creator_features = pickle.load(open(CREATOR_FEATURES_PICKLE, 'rb'))

	# classifiers = TrainAll(all_creator_features, feature_idxs)	
	# pickle.dump(classifiers, open(CLASSIFIERS_PICKLE, 'wb'))
	# classifiers = pickle.load(open(CLASSIFIERS_PICKLE, 'rb'))

	# features_bias_idxs = feature_idxs.copy()
	# features_bias_idxs['bias'] = len(feature_idxs)

	# # Get predictions
	# classifier_scores = {}
	# for creator in sorted(creators):
	# 	if creator not in classifiers:
	# 		continue
	# 	pred = Predict(classifiers[creator], test_features, feature_idxs)
	# 	classifier_scores[creator] = pred
	# print()
	# pickle.dump(classifier_scores, open(CLASSIFIER_SCORES_PICKLE, 'wb'))
	classifier_scores = pickle.load(open(CLASSIFIER_SCORES_PICKLE, 'rb'))

	for creator in classifier_scores:
		for title in classifier_scores:
			print(creator, title, classifier_scores[creator][title])
						
	# kudoer_possibilities = pickle.load(open(POSSIBILITIES_PICKLE, 'rb'))
	# classifier_possibilities = {}
	# for creator in sorted(creators):
	# 	if creator not in classifiers:
	# 		continue
	# 	pred = classifier_scores[creator]
	# 	sorted_titles = sorted(pred.keys(), key = lambda x: pred[x], reverse=True)
	# 	sfiltered_titles = [t for t in sorted_titles if t[:-4] in kudoer_possibilities and kudoer_possibilities[t[:-4]][creator]]
	# 	num_works = creator_counts[creator]
	# 	classifier_possibilities[creator] = sfiltered_titles[:num_works]
	# 	print(creator, ':', classifier_possibilities[creator])

	# print('-----------')
	# for title in sorted(test_features.keys()):
	# 	print(title, ':\t',)
	# 	for creator in creators:
	# 		if creator not in classifiers:
	# 			continue
	# 		if title not in classifier_possibilities[creator]:
	# 			continue
	# 		if GetClassifierScore(classifiers[creator], test_features[title]) > 0:
	# 			print(creator,)
	# 		else:
	# 			print('[%s]' % creator,)
	# 	print()














