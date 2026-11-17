# -*- coding: utf-8 -*-

from ao3 import AO3
from nif_exchange_2022 import * 
import pickle

creators = creator_counts.keys()

possibilities = {}
archive = AO3()
for wid in work_ids:
	work = archive.work(id=wid)

	possibilities[work.title] = dict(zip(creators, [True,]*len(creators)))
	for commenter in work.kudos_left_by:
		if commenter in creators:
			possibilities[work.title][commenter] = False
	print(work.title)


# # Special exceptions for my fic and the one I betaed.
# for creator in creators:
# 	if creator != 'circumference':
# 		possibilities['Days in the Sun'][creator] == False
# 	if creator != 'kimboo_york':
# 		possibilities['The Bodhisattva of Jinling'][creator] = False
# for title in possibilities:
# 	if title != 'Days in the Sun':
# 		possibilities[title]['circumference'] = False
pickle.dump(possibilities, open(POSSIBILITIES_PICKLE, 'wb'))

possibilities = pickle.load(open(POSSIBILITIES_PICKLE, 'rb'))
for title in possibilities:
	print(title, ':', end='')
	for candidate in possibilities[title]:
		if possibilities[title][candidate]:
			print(candidate, end='')
	num_candidates = sum(1 for c, v in possibilities[title].items() if v)
	print('(', num_candidates, ')')
	print()



















