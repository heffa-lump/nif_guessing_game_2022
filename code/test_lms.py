from nif_exchange_2022 import POSSIBILITIES_PICKLE, TEST_DIR
from text_utils import TokenizeWork
from nltk.lm.preprocessing import padded_everygram_pipeline
import pickle
import os

models_pickle = './pickles/2022/language_models/backoff_gram3.pickle'
scores_pickle = './pickles/2022/scores_gram3.pickle'

all_creator_models = pickle.load(open(models_pickle, 'rb'))
ngram_level = next(iter(all_creator_models.values())).order

all_scores = {}
print('\t', end='')
for creator in all_creator_models:
	print('%s\t' % (creator,), end='')
print()

fnames = os.listdir(TEST_DIR)
fnames.sort(key = lambda x: x.lower())
for fname in fnames:
	if (fname.startswith('.')):
		continue
	title = fname[:-4]
	print('%s\t' % (title,), end='')
	all_scores[title] = {}

	raw_contents = open(os.path.join(TEST_DIR, fname), 'r').read()
	work = TokenizeWork(title, raw_contents)
	test, vocab = padded_everygram_pipeline(ngram_level, work)
	test_ngrams = [[tt for tt in t] for t in test]
	test_ngrams = test_ngrams[0] + test_ngrams[1]

	for creator in all_creator_models:
		score = all_creator_models[creator].perplexity(test_ngrams)
		all_scores[title][creator] = score
		print('%f\t' % (score,), end='')
	print()
pickle.dump(all_scores, open(scores_pickle, 'wb'))