import reddit
from markovGrapher import MarkovGrapher
from redditHelpers import *

REDDIT_USERNAME = ''
REDDIT_PASSWORD = ''

try:
	from settings import *
except ImportError:
	pass

r = reddit.Reddit(user_agent='reader')
r.login(REDDIT_USERNAME, REDDIT_PASSWORD)

text = ''
submissions = r.get_subreddit('all').get_top(limit=10)
for submission in submissions:
	text += getCommentsText(submission.comments) + ' '

print text
#m = Markov(text.split(' '))
#mg = MarkovGrapher(m)
#mg.graph()
