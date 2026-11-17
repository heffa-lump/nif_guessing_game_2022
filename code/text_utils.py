# -*- coding: utf-8 -*-

import unicodedata

NAME_PREFIXES = [
'ah',
'xiao',
]

NAME_SUFFIXES = [
'alliance'
'dage',
'daren',
'dashu',
'dianxia',
'didi',
'die',
'fu',
'er',
'ge',
'gege',
'gonggong',
'gongong',
'gongzi',
'jie'
'jiejie',
'jiujiu',
'mama',
'mei',
'meimei',
'nainai',
'qing',
'shu',
'xiansheng',
'xiong',
'yeye',
]

NAME_WHITELIST = [
 'Bitter',
 'bixia',
 'Banruo',
 'Cai',
 'Changsu',
 'Chen',
 'Chilling',
 'Consort',
 'Crown',
 'Dingfeng',
 'Divine',
 'Dong',
 'Emperor',
 'Empress',
 'Fei',
 'Feiliu',
 'Flame',
 'Frostfire',
 'Gang',
 'Gong',
 'Grandprincess',
 'Hanging',
 'Honor',
 'Honour',
 'Highness',
 'Ji',
 'Jiang',
 'Jing',
 'Jinghuan',
 'Jingrui',
 'Jingxuan',
 'Jingyan',
 'Jingyu',
 'Jun',
 'Li',
 'Liang',
 'Lin',
 'Liu',
 'Lu',
 'Marquess',
 'Marquis',
 'Master',
 'Mei',
 'Meng',
 'Mirror',
 'Mu',
 'Niang',
 'Nihuang',
 'Noble',
 'Ping',
 'Prince',
 'Qi',
 'Qilin',
 'Qin',
 'Qing',
 'Quan',
 'Que',
 'Shen',
 'shi',
 'Shisan',
 'Shu',
 'Sir',
 'Su',
 'Tingsheng',
 'Tong',
 'Wei',
 'Xia',
 'Xian',
 'Xiao',
 'Xie',
 'Xuan',
 'Xuanjing',
 'Yan',
 'Yang',
 'Young',
 'Yu',
 'Yue',
 'Yujin',
 'Zhe',
 'Zhen',
 'Zheng',
 'Zhi',
 'Zhui',
 'Zhuo',
 'Zuo',
]

prefixes = sorted(NAME_PREFIXES, key=lambda x: len(x), reverse=True)
prefixes = [p.lower() for p in prefixes]
name_whitelist = sorted(NAME_WHITELIST, key=lambda x: len(x), reverse=True)
name_whitelist = [n.lower() for n in name_whitelist]


def TokenizeHtml(html_string):
    tokens = []
    current_token = ''
    in_tag = False

    for char in html_string: #.decode('utf-8'):
    	if char == '<':
    		if current_token:
    			tokens.append(current_token)
    		current_token = char
    		in_tag = True
    	elif char == '>':
    		current_token += char
    		tokens.append(current_token)
    		current_token = ''
    		in_tag = False
    	elif not in_tag and unicodedata.category(char).startswith('P'):
    		if current_token:
    			tokens.append(current_token)
    		tokens.append(char)
    		current_token = ''
    	elif not in_tag and char.isspace():
    		if current_token:
    			tokens.append(current_token)
    		current_token = ''
    	else:
    		current_token += char
            
    if len(current_token) > 0:
    	tokens.append(current_token)
    return tokens


def TokenIsTag(token):
	return token and token[0] == '<' and token[-1] == '>'

def TokenIsPunctuation(token):
	return len(token) == 1 and unicodedata.category(token).startswith('P')

def MaybeNormalizeTag(token):
	if len(token) >= 7 and token[:7] == '<a href': return 'A:HREF'
	if len(token) >= 3 and token[:3] == '<a ': return 'A:NOHREF'
	if len(token) >= 5 and token[:5] == '<img ': return 'IMG'
	return token

def NormalizeTitle(title):
    """Only care whether it's capitalized, punctuation, or non-ascii"""
    # all-lower, all-upper, first-letter capitalized, punctuation, non-ascii, number
    tokens = TokenizeHtml(title)
    title_tokens = []
    for tok in tokens:
        ntok = '_TITLE_unk'
        if tok.islower():
            ntok = '_TITLE_lower'
        elif IsProper(tok):
            ntok = '_TITLE_proper'
        elif tok.isupper():
            ntok = '_TITLE_upper'
        elif TokenIsPunctuation(tok):
            ntok = '_TITLE_punct'
        elif not tok.isascii():
            ntok = '_TITLE_unicode'
        elif tok.isnumeric():
            ntok = '_TITLE_number'
        title_tokens.append(ntok)

    return title_tokens


def TokenizeWork(title, raw_contents):
    title_tokens = NormalizeTitle(title)
    body_tokens = TokenizeHtml(raw_contents)
    body_tokens = [t for t in body_tokens if len(t) > 0]
    return [title_tokens, body_tokens]


def IsProper(token):
    return token.isalnum() and token[0].isupper() and not token.isupper()

def FirstAlphaIndex(s):
    if all(not c.isalpha() for c in s): 
        return None

    return min(range(len(s)), key = lambda i: s[i].isalpha() * -100)

def IsLowercase(s):
    return all(not c.isalpha() or c.islower() for c in s)

def IsTitlecase(s):
    if s.istitle():
        return True
    tokens = s.split()
    return tokens[0].istitle() and tokens[-1].istitle()

# TODO: test this
def HasUnicode(s):
    return any(not c.isascii for c in s)

# TODO: test this
def HasNumerals(s):
    return any(c.isnumeric for c in s)

def IsWhitelistedName(maybe_name):
    tokens = maybe_name.split()
    if not (tokens[0].isalpha() and tokens[-1].isalpha()):
        return False
    if not (IsProper(tokens[0]) or len(tokens) > 1):
        return False

    normalized = ''.join(maybe_name.split()).lower()
    normalized = ''.join(normalized.split('-'))
    not_consumed = normalized

    # Normalize everything
    for prefix in prefixes:
        if not_consumed.startswith(prefix):
            not_consumed = not_consumed[len(prefix):]

    while not_consumed:
        found_name = False
        for wname in name_whitelist:
            if not_consumed.startswith(wname):
                found_name = True
                not_consumed = not_consumed[len(wname):]
        if not found_name:
            break

    return (not_consumed == '') or (not_consumed in NAME_SUFFIXES)


def TokenIsBlacklisted(tok):
    # ol tags
    return (len(tok) >= 3 and tok[:3] == '<ol') or tok == '</ol>'

