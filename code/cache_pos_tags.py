# -*- coding: utf-8 -*-

import nif_exchange
from nif_exchange import HTML_DIR, TEST_DIR, creator_counts
from text_utils import TokenizeHtml, TokenIsTag
import os
from nltk.tag.stanford import StanfordTagger
from histogram_utils import HistogramNgramsWithFilter, printHist
import pickle

creators = creator_counts.keys()

class MyTagger(StanfordTagger):
    _SEPARATOR = '_'
    _JAR = 'stanford-postagger.jar'

    def __init__(self, *args, **kwargs):
        super(MyTagger, self).__init__(*args, **kwargs)

    @property
    def _cmd(self):
        return [
            'edu.stanford.nlp.tagger.maxent.MaxentTagger',
            '-model',
            self._stanford_model,
            '-textFile',
            self._input_file_path,
            '-tokenize',
            'true',
        ]

tagger = MyTagger('english-bidirectional-distsim.tagger', path_to_jar='/path/to/workspace/stanford-postagger-2018-10-16/stanford-postagger.jar')

def TagPos(directory, title):
	f = open(os.path.join(directory, title), 'r')
	raw_contents = f.read()
	f.close()
	tokens = [t for t in TokenizeHtml(raw_contents) if not TokenIsTag(t)]
	tagged = tagger.tag_sents([tokens,])
	return tagged


if __name__ == '__main__':
	from nif_exchange import CREATOR_POS_COUNTS_PICKLE, TEST_POS_COUNTS_PICKLE

	test_pos_counts = {}
	for title in os.listdir(TEST_DIR):
		print title
		test_pos_counts[title] = TagPos(TEST_DIR, title)
	pickle.dump(test_pos_counts, open('creator_pos_counts/unrevealed.pickle', 'wb'))

	for creator in creators:
		creator_pos_counts = {}
		creator_dir = os.path.join(HTML_DIR, creator)
		for title in os.listdir(creator_dir):
			print title
			creator_pos_counts[title] = TagPos(creator_dir, title)
		pickle.dump(creator_pos_counts, open('creator_pos_counts/%s.pickle' % creator, 'wb'))


