import scipy.optimize
import numpy as np
from train_svms import ExplainPrediction
from nif_exchange import treats, creator_counts, non_fic_counts
from nif_exchange import CREATOR_FEATURES_PICKLE, TEST_FEATURES_PICKLE, CLASSIFIER_SCORES_PICKLE, \
							 FIDXS_PICKLE, POSSIBILITIES_PICKLE, CLASSIFIERS_PICKLE
import pickle


BIG_NUMBER = 1e9
INCREMENT = 36

# Author counts
author_counts = creator_counts.copy()
for creator in non_fic_counts:
	author_counts[creator] -= non_fic_counts[creator]

classifier_scores = pickle.load(open(CLASSIFIER_SCORES_PICKLE, 'rb'))
kudoer_possibilities = pickle.load(open(POSSIBILITIES_PICKLE, 'rb'))

# Helper functions
def CostDictionary(author_name):
	print author_name

	scores = classifier_scores[author_name].copy()
	impossibilities = [t for t in scores.keys() if not kudoer_possibilities[t][author_name]]

	# Make sure kudoer impossibilities and treat impossibilities sorted last
	for imp in impossibilities:
		scores[imp] = -BIG_NUMBER
	if author_counts[author_name] == 1:
		for treat_title in treats:
			scores[treat_title] = -BIG_NUMBER
	sorted_titles = sorted(scores.keys(), key=lambda x: scores[x], reverse=True)

	creator_costs = dict(zip(sorted_titles, [r for r in range(len(sorted_titles))]))

	for title in scores:
		if scores[title] < 0:
			creator_costs[title] += INCREMENT

	print creator_costs

	# Make impossibilities prohibitive
	for imp in impossibilities:
		creator_costs[imp] = BIG_NUMBER
	if author_counts[author_name] == 1:
		for treat_title in treats:
			creator_costs[treat_title] = BIG_NUMBER
	print creator_costs

	return creator_costs

def StepCostDictionary(author_name):
	print author_name

	scores = classifier_scores[author_name].copy()
	impossibilities = [t for t in scores.keys() if not kudoer_possibilities[t][author_name]]

	# Make sure kudoer impossibilities and treat impossibilities sorted last
	for imp in impossibilities:
		scores[imp] = -BIG_NUMBER
	if author_counts[author_name] == 1:
		for treat_title in treats:
			scores[treat_title] = -BIG_NUMBER
	creator_costs = dict(zip(scores.keys(), [0,] * len(scores)))

	for title in scores:
		if scores[title] < 0:
			creator_costs[title] = 1

	print creator_costs

	# Make impossibilities prohibitive
	for imp in impossibilities:
		creator_costs[imp] = BIG_NUMBER
	if author_counts[author_name] == 1:
		for treat_title in treats:
			creator_costs[treat_title] = BIG_NUMBER
	print creator_costs

	return creator_costs


def Match(classifier_scores, kudoer_possibilities):
	test_titles = classifier_scores['circumference'].keys()

	costs = {}
	for author in author_counts:
		if author_counts[author] <= 0:
			continue
		if author not in classifier_scores:
			costs[author] = dict(zip(test_titles, [len(test_titles),] * len(test_titles)))
			continue

		creator_costs = StepCostDictionary(author)

		for instance in range(1, author_counts[author] + 1):
			instance_name = "%s-%i" % (author, instance)
			costs[instance_name] = creator_costs

	# Get author indices
	author_idxs = dict(zip(costs.keys(), range(len(costs))))
	idx_authors = costs.keys()

	# Get test title indices
	test_title_idxs = dict(zip(test_titles, range(len(test_titles))))
	idx_test_titles = test_titles

	# Put things in array
	cost_matrix = np.zeros([len(costs), len(test_titles)])
	for a, ai in author_idxs.iteritems():
		for t, ti in test_title_idxs.iteritems():
			cost_matrix[ai][ti] = costs[a][t]

	row_ind, col_ind = scipy.optimize.linear_sum_assignment(cost_matrix)
	matches = {}
	for ai, ti in zip(row_ind, col_ind):
		matches[idx_test_titles[ti]] = idx_authors[ai]
	return matches, costs, idx_authors, test_title_idxs


if __name__ == '__main__':
	from nif_exchange import CREATOR_FEATURES_PICKLE, TEST_FEATURES_PICKLE, CLASSIFIER_SCORES_PICKLE, \
							 FIDXS_PICKLE, POSSIBILITIES_PICKLE, CLASSIFIERS_PICKLE
	import pickle

	feature_idxs = pickle.load(open(FIDXS_PICKLE, 'rb'))
	features_bias_idxs = feature_idxs.copy()
	features_bias_idxs['bias'] = len(feature_idxs)

	classifiers = pickle.load(open(CLASSIFIERS_PICKLE, 'rb'))
	test_features = pickle.load(open(TEST_FEATURES_PICKLE, 'rb'))

	matches, costs, _, _ = Match(classifier_scores, kudoer_possibilities)

	for title, author_instance in sorted(matches.iteritems()):
		author = author_instance.split('-')[0]
		print title, ': \t', author, '\t (', costs[author_instance][title], ')'

	# titles_at_large = [
	# 	'(they said eyes are windows) i used them as a mirror',
	# 	'A Mid-Autumn Night\'s Dream',
	# 	'Across Distant Lands',
	# 	'An Unpolished Weapon, a Weapon Newly Formed',
	# 	'Crossing the Rubicon, or How @madaboutmeichangsu (follower count 50k) Finally Snapped',
	# 	'Cursory days',
	# 	'Fire and Ice',
	# 	'For Myself, Alone',
	# 	'Pilgrimage',
	# 	'Ring of Fire',
	# 	'Sisters',
	# 	'Small Bump',
	# 	'Tis the season (so have a fic about seasons!)',
	# 	'Turn the River South',
	# 	'White Peonies',
	# 	'giving up the ghost',
	# 	'pass me the paint and glue (perfect isn\'t easy but it\'s me)',
	# 	'the river runs gentle, pure and deep',		
	# 	'time\'s up, eyes up, wise up',		
	# ]

	# for title in titles_at_large:
	# 	author_costs = dict(zip(costs.keys(), [costs[author][title] for author in costs]))
	# 	sorted_authors = sorted([a for a in author_costs if a[-1] != '2' and a[-1] != '3'], key = lambda a: author_costs[a])
	# 	print '================', title, '================'
	# 	for author in sorted_authors:
	# 		cost = author_costs[author]
	# 		if cost <= 6:
	# 			print author, cost
	# 			ExplainPrediction(classifiers[author.split('-')[0]], test_features[title], feature_idxs)
	# 			print
	# 	print















