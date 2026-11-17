# -*- coding: utf-8 -*-

snapshot = './pickles/2019'
POSSIBILITIES_PICKLE = '%s/possibilities.pickle' % snapshot
CREATOR_FEATURES_PICKLE = '%s/creator_features.pickle' % snapshot
TEST_FEATURES_PICKLE = '%s/test_features.pickle' % snapshot
CLASSIFIERS_PICKLE = '%s/classifiers.pickle' % snapshot
FIDXS_PICKLE = '%s/feature_idxs.pickle' % snapshot
CREATOR_POS_COUNTS_PICKLE = 'creator_pos_counts.pickle'
TEST_POS_COUNTS_PICKLE = 'test_pos_counts.pickle'
CLASSIFIER_SCORES_PICKLE = '%s/classifier_scores.pickle' % snapshot
HTML_DIR = './training_html/2019'
TEST_DIR = './test_html/2019'
MULTI_CLASSIFIER_PICKLE = '%s/multi_classifier.pickle' % snapshot

work_ids = [
	'21340036',  # The One I Love Has a Mole On His Neck
	'21460609',  # A Gold Dragon
	'21514882',  # Sisters
	'21549388',  # Pilgrimage
	'21570544',  # A Mid-Autumn Night's Dream
	'21580225',  # Come back to Haunt Me
	'21591010',  # White Peonies
	'21604906',  # The Bodhisattva of Jinling
	'21605236',  # the river runs gentle, pure and deep
	'21659368',  # Days in the Sun
	'21666307',  # with every year that passes (we don't forget)
	'21716167',  # letters borne on wild goose wings
	'21680746',  # (they said eyes are windows) I used them as a mirror
	'21711379',  # The Origin of Pearls
	'21709666',  # Fun Time
	'21679474',  # Giving up the ghost
	'21684658',  # Four seasons of promises
	'21685291',  # Disaster lesbian
	'21702277',  # The choice of an end
	'21686110',  # Turn the River South
	'21510385',  # Cursory days
	'21689740',  # Tis the season (so have a fic about seasons!)
	'21705685',  # Crossing the Rubicon, or How @madaboutmeichangsu (follower count 50k) Finally Snapped
	'21689896',  # For Myself, Alone
	'21691291',  # Fire and Ice
	'21693415',  # TREAT The Evidence of Your Survival
	'21729496',  # Across Distant Lands
	'21732943',  # Xiao Jingyan and he Cursed Cousin
	'21754528',  # Parachute
	'21754546',  # Four Conversations About Stealing A Prince (and One After The Fact)
	'21754792',  # TREAT. An Unpolished Weapon, a Weapon Newly Formed
	'21756148',  # Perseverance
	'21765853',  # Like waves on the shore
	'21766735',  # Hair ties the tongue numb
	'21780118',  # Ring of Fire
	'21786463',  # Princess Consort Mei
	'21786529',  # Treasured
	'21789262',  # Keeping Company
	'21797395',  # As You Command
	'21806902',  # TREAT pass me the paint and glue (perfect isn't easy but it's me)
	'21807520',  # Small Bump
	'21807688',  # TREAT time's up, eyes up, wise up
	'21814450',  # The Bull-Headed Lion
]

treats = {
	'The Evidence of Your Survival', 
	'An Unpolished Weapon, a Weapon Newly Formed', 
	'pass me the paint and glue (perfect isn\'t easy but it\'s me)', 
	'time\'s up, eyes up, wise up',
}

creator_counts = {
	'qwertyuiop678' : 1,
	'Katharos' : 1,
	'ihamtmus' : 1,
	'nanasheeeh' : 1,
	'mysticaltorque' : 3,
	'gixi_ninja' : 1,
	'ZairaA' : 2,
	'intyalote' : 1,
	'Lanerose' : 1,
	'troubleinmind' : 3,
	'mekare' : 1,
	'spaceAltie' : 1,
	'InfinityIllusion' : 1,
	'LadyMerlin' : 2,
	'tciddaemina' : 1,
	'circumference' : 1,
	'RuanChunXian' : 1,
	'kimboo_york' : 2,
	'mabyn' : 1,
	'Ione' : 2,
	'BlackRook' : 1,
	'theravenconspiracy' : 1,
	'ConvenientAlias' : 3,
	'tornasoleando' : 1,
	'lunatique' : 2,
	'speos' : 1,
	'romantic_drift' : 1,
	'forbiddenstars' : 1,
	'zorana' : 1,
	'umichii' : 1,
	'orangememory' : 1,
	'hongliu' : 1,
}

# troubleinmind is the vidder
non_fic_counts = {'ihamtmus' : 1, 'mekare' : 1, 'spaceAltie' : 1, 'theravenconspiracy' : 1, 'lunatique' : 2, 'troubleinmind' : 1}

pseuds = {
	'RuanChunXian' : 'huanzhuyulu',
	'umichii' : 'Umi',
}

giftees = {}