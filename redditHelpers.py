import re
import random
from markov import Markov

def sanitize(content):
	# TODO: Horrible:
	convertEntities = re.compile(r'(&lt;|&gt;)')
	content = convertEntities.sub('', content)

	collapseSpaces = re.compile(r'\s+')
	content = collapseSpaces.sub(' ', content)

	return content

def markovComments(comments):
	words = comments.split(' ');
	startWord = random.choice(words)
	while not startWord[0].isupper():
		startWord = random.choice(words)

	m = Markov(words)
	chain = m.getNextSentence(startWord, 20)
	sentence = startWord
	for word in chain:
		sentence += ' ' + word
	
	return sentence

def getCommentsText(comments):
	allcomments = ''
	for comment in comments:
		try:
			allcomments += comment.body.encode('ascii', 'ignore')
		except Exception: # some comments are really "MoreComments" with no body. This takes care of it.
			continue

	return sanitize(allcomments)

