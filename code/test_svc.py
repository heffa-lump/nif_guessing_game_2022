import pickle
from nif_exchange_2019 import MULTI_CLASSIFIER_PICKLE, TEST_FEATURES_PICKLE, FIDXS_PICKLE, \
POSSIBILITIES_PICKLE, giftees
from train_svc import GetMatrixFromDict
import numpy as np
from scipy.optimize import linear_sum_assignment

NEGATIVE_INF = float('-inf')

def ScoreCost(scores):
	# Find max score
	max_score = NEGATIVE_INF
	for s in scores.ravel():
		if s > max_score:
			max_score = s
	# Cost matrix (lower is better) from scores (higher is better)
	cost = np.zeros(scores.shape)
	for i in range(scores.shape[0]):
		for j in range(scores.shape[1]):
			cost[i,j] = max_score - scores[i,j] + 1
	return cost

def RowRankCost(scores):
	cost = np.zeros(scores.shape)
	for i in range(scores.shape[0]):
		sorted_j = sorted(range(len(scores[i,:])), key=lambda x: scores[i,x], reverse=True)
		c = 0
		for j in sorted_j:
			c = c + 1
			cost[i,j] = c
	return cost

def ColRankCost(scores):
	cost = np.zeros(scores.shape)
	for j in range(scores.shape[1]):
		sorted_i = sorted(range(len(scores[:,j])), key=lambda x: scores[x,j], reverse=True)
		c = 0
		for i in sorted_i:
			c = c + 1
			cost[i,j] = c
	return cost


test_features = pickle.load(open(TEST_FEATURES_PICKLE, 'rb'))
feature_idxs = pickle.load(open(FIDXS_PICKLE, 'rb'))
classifier = pickle.load(open(MULTI_CLASSIFIER_PICKLE, 'rb'))
kudoer_possibilities = pickle.load(open(POSSIBILITIES_PICKLE, 'rb'))

# Print scores and predictions
X, title_dict = GetMatrixFromDict(test_features, feature_idxs)
feat_norms = np.sqrt(np.sum(X * X, axis=1))
X = X / feat_norms[:, None]
scores = classifier.decision_function(X)

# Straighten out title orders
s_idx = sorted(range(len(title_dict)), key = lambda x: title_dict[x].lower())

# Zero out kudoers and giftees
for i in range(len(title_dict)):
	title = title_dict[i]
	for j in range(len(classifier.classes_)):
		creator = classifier.classes_[j]
		if title in kudoer_possibilities and creator in kudoer_possibilities[title] \
			and not kudoer_possibilities[title][creator]:
			scores[i, j] = NEGATIVE_INF
		if title in giftees and giftees[title] == creator:
			scores[i, j] = NEGATIVE_INF

# Print table
print('\t', end='')
for creator in classifier.classes_:
	print(creator, '\t', end='')
print()
for i in range(len(s_idx)):
	print(title_dict[s_idx[i]], '\t', end='')
	for j in range(len(classifier.classes_)):
		print(scores[s_idx[i],j], '\t', end='')
	print()
for i in s_idx:
	jmax = max(range(len(scores[i,:])), key = lambda x: scores[i, x])
	print(classifier.classes_[jmax])
print()

cost = ScoreCost(scores)
assignments = {}
title_ind, creator_ind = linear_sum_assignment(cost)
for i, j in zip(title_ind, creator_ind):
	title = title_dict[i]
	creator = classifier.classes_[j]
	assignments[title] = creator

for i in range(len(title_dict)):
	title = title_dict[i]
	if i not in title_ind:
		jmin = min(range(cost.shape[1]), key = lambda x: cost[i, x])
		creator = classifier.classes_[jmin]
		assignments[title] = creator

for title in sorted(assignments.keys(), key = lambda x: x.lower()):
	if not (title[:-4] == 'Natural') and not (title[:-4] == 'Hark ! A revenant'):
		print(assignments[title])

























