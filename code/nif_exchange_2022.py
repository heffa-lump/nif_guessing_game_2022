# -*- coding: utf-8 -*-

snapshot = './pickles/2022'
POSSIBILITIES_PICKLE = '%s/possibilities.pickle' % snapshot
LMS_PICKLE = '%s/language_models.pickle' % snapshot
TOKENIZED_PICKLE = '%s/tokenized.pickle' % snapshot
HTML_DIR = './training_html/2022'
TEST_DIR = './test_html/2022'

CLASSIFIERS_PICKLE = '%s/classifiers.pickle' % snapshot
MULTI_CLASSIFIER_PICKLE = '%s/multi_classifier.pickle' % snapshot
CREATOR_FEATURES_PICKLE = '%s/creator_features.pickle' % snapshot
TEST_FEATURES_PICKLE = '%s/test_features.pickle' % snapshot
FIDXS_PICKLE = '%s/feature_idxs.pickle' % snapshot
CREATOR_POS_COUNTS_PICKLE = 'creator_pos_counts.pickle'
TEST_POS_COUNTS_PICKLE = 'test_pos_counts.pickle'
CLASSIFIER_SCORES_PICKLE = '%s/classifier_scores.pickle' % snapshot

work_ids = [
	'43152154',    # fourth, second, last
	'43255908',    # All the Distant Stars
	'42662007',    # The Sound of Our Names
	'43244034',    # Spring
	'43275187',    # Aftermath
	'43276863',    # Sploot
	'43264452',    # There is a beast dwelling here
	'43284430',    # turnabout in fire
	'43257780',    # Love me like poison
	'42189246',    # The Transmigrator's Guide to Fix-it Fanfictions
	'42169881',    # Lone Tree Before the Storm
	'43390290',    # borderline
	'43378206',    # Ask a tricky question...
	'43377672',    # To The Victor The Spoils
	'43361166',    # Five times Lin Chen broke into Mei Changsu's apartment (and one he didn't have to)
	'43274044',    # the truth is (stranger than fiction)
	'43345983',    # Scars
	'43345653',    # In veneno veritas
	'43345093',    # Boiling Point
	'42834327',    # Behind the Mask
	'43254471',    # training vipers
	'43365231',    # I was alone, staring over the ledge
	'43142485',    # Fluff
	'42581715',    # It is nothing to die. It is frightful not to live
	'42625641',    # with friends like these
	'42625770',    # Shipping for Fun and Profit
	'42625869',    # Warriors
	'42625932',    # An Overture in E Minor
	'42653040',    # 琴歌
	'42653871',    # the truth will set you free
	'42669087',    # Sacrifice
	'42690228',    # Bound with Victorious Wreaths
	'42742731',    # Chance Encounters
	'42760839',    # Invasion of the Bodysnatchers
	'42816825',    # Blood From a Stone
	'42833343',    # Pity the Child
	'42875841',    # Pilgrimage
	'43008393',    # Superheroes in Fire
	'43009698',    # the voice of parents is the voice of gods
	'43097544',    # ere long see each other again
	'43116042',    # ends, means
	'43131487',    # Interesting Times
	'43165623',    # the map of honour, truth, and loyalty
	'43258503',    # The tragically murdered best friend's guide to changing the plot
	'43258573',    # The Joys of Babysitting
	'43262428',    # ever so many partings welded together
	'43295283',    # and i speak to you like the chorus to the verse
	'43117296',    # half my soul (as the poets say)
	'43298337',    # Hands up! You’re under a-roast
	'43317313',    # when the world has brought you down to your knees
	'43332798',    # with the first link, the chain is forged
	'43366548',    # nor set aught down in malice
	'43377604',    # 生津 | Sheng Jin
	'43381932',    # Langyapedia
	'42453039',    # the young master (doesn't) come down the mountain
	'43389450',    # they warned us, a storm is coming on
	'43259322',    # Eyes Burning Like the Stars
	'43382637',    # stone cold silence
	'43374261',    # 博君一笑 — To Win Your Smile
	'43310311',    # Whiteout
	'43307931',    # Young disciple asks the master
	'43283493',    # Parallel Lines
	'43279525',    # Find Your Way Out
	'43373199',    # Unrecorded but remembered
	'43199536',    # 归邪 | Their Return
	'43242586',    # Breaking the cocoon
]

multimedia_ids = [
	'43283826',    # Hark ! A revenant
	'42964548',    # [Artwork] History is set in stone
	'43235068',    # Natural
	'42919053',    # Art: Escape
	'42869364',    # [PODFIC] Tutors
	'43373209',    # Art: those whispered waves of hope
	'43286050',    # Consort Jing &amp; Young Xiao Jingyan in the palace
	'43202623',    # Butterfly Lovers [Fanart]
	'43284225',    # dance with the devil || nirvana in fire [fanvid]
]

# There are just. A lot this year.
treats = {
}

creator_urls = {
	'aninfiniteweirdo' :      'https://archiveofourown.org/users/aninfiniteweirdo/works',
	'bromeliaddreams':      'https://archiveofourown.org/users/bromeliaddreams/works',
	'caulkhead':            'https://archiveofourown.org/users/caulkhead/works',
	'DC_Derringer':         'https://archiveofourown.org/users/DC_Derringer/works',
	'intyalote':            'https://archiveofourown.org/users/intyalote/works',
	'Kasasagi':             'https://archiveofourown.org/users/Kasasagi/works',
	'kimboo_york':          'https://archiveofourown.org/users/kimboo_york/works',
	'LadyMerlin':           'https://archiveofourown.org/users/LadyMerlin/works',
	'liuet':                        'https://archiveofourown.org/users/liuet/works',
	'Merelhyn' :              'https://archiveofourown.org/users/Merelhyn/works',
	'Nemainofthewater' :      'https://archiveofourown.org/users/Nemainofthewater/works',
	'RuanChunXian': 'https://archiveofourown.org/users/RuanChunXian/works',
	'RubberLotus':          'https://archiveofourown.org/users/RubberLotus/works',
	'Rusoe':                        'https://archiveofourown.org/users/Rusoe/works',
	'Shadaras':             'https://archiveofourown.org/users/Shadaras/works',
	'tciddaemina':          'https://archiveofourown.org/users/tciddaemina/works',
	'ThebanSacredBand':     'https://archiveofourown.org/users/ThebanSacredBand/works',
	'ThunderstormsandMemories' : 'https://archiveofourown.org/users/ThunderstormsandMemories/works',
	'Triss_Hawkeye':        'https://archiveofourown.org/users/Triss_Hawkeye/works',
	'Umi':                  'https://archiveofourown.org/users/umichii/pseuds/Umi/works',
	'whYJayteesee':  'https://archiveofourown.org/users/whYJayteesee/works',
	'xpityx' :                        'https://archiveofourown.org/users/xpityx/works',
	'zandalorian':          'https://archiveofourown.org/users/zandalorian/works',
}

# This year, we aren't given the number of works each creator made.
creator_counts = dict(zip(creator_urls.keys(), [2,] * len(creator_urls)))

# These are separated out this year
non_fic_counts = {}

# Useless if you have creator_urls
pseuds = {}

giftees = {
        'Aftermath' : 'Merelhyn',
        'All the Distant Stars' : 'liuet',
        'An Overture in E Minor' : 'bromeliaddreams',
        'Ask a tricky question...' : 'Thimblerig',
        'Behind the Mask' : 'Shadaras',
        'Blood From a Stone' : 'mekare',
        'Boiling Point' : 'Nemainofthewater',
        'Bound with Victorious Wreaths' : 'Kasasagi',
        'Breaking the cocoon' : 'RubberLotus',
        'Chance Encounters' : 'kimboo_york',
        'Eyes Burning Like the Stars' : 'ThunderstormsandMemories',
        'Find Your Way Out' : 'tupperwaregoods',
        'Five times Lin Chen broke into Mei Changsu\'s apartment (and one he didn\'t have to)' : 'Nemainofthewater',
        'Fluff' : 'whYJayteesee',
        'Hands up! You’re under a-roast' : 'liuet',
        'I was alone, staring over the ledge' : 'intyalote',
        'In veneno veritas' : 'DC_Derringer',
        'Interesting Times' : 'Triss_Hawkeye',
        'Invasion of the Bodysnatchers' : 'Rusoe',
        'It is nothing to die. It is frightful not to live' : 'ThebanSacredBand',
        'Langyapedia' : 'caulkhead',
        'Lone Tree Before the Storm' : 'Shadaras',
        'Love me like poison' : 'xpityx',
        'Parallel Lines' : 'Machidieles',
        'Pilgrimage' : 'Shadaras',
        'Pity the Child' : 'intyalote',
        'Sacrifice' : 'Machidieles',
        'Scars' : 'ThebanSacredBand',
        'Shipping for Fun and Profit' : 'tupperwaregoods',
        'Sploot' : 'em_94',
        'Spring' : 'LadyMerlin',
        'Superheroes in Fire' : 'RubberLotus',
        'The Joys of Babysitting' : 'em_94',
        'The Sound of Our Names' : 'aninfiniteweirdo',
        'The Transmigrator\'s Guide to Fix-it Fanfictions' : 'zandalorian',
        'The tragically murdered best friend\'s guide to changing the plot' : 'zandalorian',
        'There is a beast dwelling here' : 'tciddaemina',
        'To The Victor The Spoils' : 'Triss_Hawkeye',
        'Unrecorded but remembered' : 'Triss_Hawkeye',
        'Warriors' : 'RuanChunXian',
        'Whiteout' : 'BromeliadDreams',
        'Young disciple asks the master' : 'Nemainofthewater',
        'and i speak to you like the chorus to the verse' : 'ThunderstormsandMemories',
        'borderline' : 'Lake_Badger',
        'ends, means' : 'Merelhyn',
        'ere long see each other again' : 'xpityx',
        'ever so many partings welded together' : 'Lake_Badger',
        'fourth, second, last' : 'Kasasagi',
        'half my soul (as the poets say)' : 'Rusoe',
        'nor set aught down in malice' : 'aninfiniteweirdo',
        'stone cold silence' : 'Merelhyn',
        'the map of honour, truth, and loyalty' : 'Umi',
        'the truth is (stranger than fiction)' : 'DC_Derringer',
        'the truth will set you free' : 'DC_Derringer',
        'the voice of parents is the voice of gods' : 'tciddaemina',
        'the young master (doesn\'t) come down the mountain' : 'Thimblerig',
        'they warned us, a storm is coming on' : 'RubberLotus',
        'training vipers' : 'intyalote',
        'turnabout in fire' : 'troubleinmind',
        'when the world has brought you down to your knees' : 'troubleinmind',
        'with friends like these' : 'LadyMerlin',
        'with the first link, the chain is forged' : 'aninfiniteweirdo',
        '生津 | Sheng Jin' : 'RuanChunXian',
        '归邪 | Their Return' : 'Merelhyn',
        '琴歌' : 'Thimblerig',
        '博君一笑 — To Win Your Smile' : 'Triss_Hawkeye',
}
