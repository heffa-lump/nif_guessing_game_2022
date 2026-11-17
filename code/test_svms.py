import pickle
from nif_exchange_2022 import CLASSIFIERS_PICKLE, POSSIBILITIES_PICKLE, CLASSIFIER_SCORES_PICKLE, \
POSSIBILITIES_PICKLE, giftees
import numpy as np
from scipy.optimize import linear_sum_assignment

NEGATIVE_INF = float('-inf')
classifier_scores = pickle.load(open(CLASSIFIER_SCORES_PICKLE, 'rb'))
titles = sorted(list(next(iter(classifier_scores.values())).keys()), key=lambda x: x.lower())
creators = sorted(list(classifier_scores.keys()), key=lambda x: x.lower())
kudoer_possibilities = pickle.load(open(POSSIBILITIES_PICKLE, 'rb'))

# print('\t', end='')
# for creator in creators:
# 	print(creator, '\t', end='')
# print()
# for title in titles:
# 	print(title[:-4], '\t', end='')
# 	for creator in creators:
# 		print(classifier_scores[creator][title][0], '\t', end='')
# 	print()

# Create scores matrix, zeroing out kudoers and giftees
scores = np.zeros((len(titles), len(creators)))

for i in range(len(titles)):
	title = titles[i]
	if title[:-4] == 'Natural' or title[:-4] == 'Hark ! A revenant':
		continue
	for j in range(len(creators)):
		creator = creators[j]
		scores[i,j] = classifier_scores[creator][title]
		if not kudoer_possibilities[title[:-4]][creator]:
			scores[i, j] = NEGATIVE_INF
		if giftees[title[:-4]] == creator:
			scores[i, j] = NEGATIVE_INF

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

cost = ColRankCost(scores)

assignments = {}
title_ind, creator_ind = linear_sum_assignment(cost)
for i, j in zip(title_ind, creator_ind):
	title = titles[i]
	creator = creators[j]
	assignments[title] = creator

# for i in range(len(titles)):
# 	title = titles[i]
# 	if i not in title_ind:
# 		jmin = min(range(cost.shape[1]), key = lambda x: cost[i, x])
# 		creator = creators[jmin]
# 		assignments[title] = creator

for title in sorted(assignments.keys(), key = lambda x: x.lower()):
	if not (title[:-4] == 'Natural') and not (title[:-4] == 'Hark ! A revenant'):
		print(assignments[title])

for title in sorted(titles, key=lambda x: x.lower()):
	if not (title[:-4] == 'Natural') and not (title[:-4] == 'Hark ! A revenant'):
		if title in assignments:
			print('TRUE')
		else:
			print()	













