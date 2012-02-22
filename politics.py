import reddit
from redditHelpers import sanitize, markovComments, getCommentsText

r = reddit.Reddit(user_agent='reader')
r.login('stupiddumb', 'pizzabox')

topSubmissions = r.get_subreddit('politics').get_hot(limit=10)

print 'Aggregating from...'

aggregateCommentsText = ''
for submission in topSubmissions:
	print submission.title.encode('ascii', 'ignore')

	comments = submission.comments_flat
	aggregateCommentsText += getCommentsText(comments)

print

while True:
	print markovComments(aggregateCommentsText)
	raw_input('')
