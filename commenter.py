import reddit
import urllib2 # for exceptions
import time
import pickle
from redditHelpers import sanitize, markovComments, getCommentsText

REDDIT_USERNAME = ''
REDDIT_PASSWORD = ''
DEBUG = False
REMEMBER_HIT = True
TARGET_REDDIT = ''
NEW_SUBMISSIONS_REDDIT = ''
SUBMISSIONS_TO_MONITOR = 5
MONITOR_INTERVAL = 30 # seconds
NEW_SUBMISSION_INTERVAL = 3600 # seconds
COMMENT_THRESHOLD = 25
PICKLE_FILE_SUBMISSIONS = 'hitSubmissions.pkl'
PICKLE_FILE_COMMENTS = 'hitComments.pkl'

try:
	from settings import *
except ImportError:
	pass

r = reddit.Reddit(user_agent='reader')
r.login(REDDIT_USERNAME, REDDIT_PASSWORD)

# get already-hit submissions and comments
hitSubmissions = []
hitComments = []
if REMEMBER_HIT:
	try:
		pklSubmissions = open(PICKLE_FILE_SUBMISSIONS, 'rb')
		pklComments = open(PICKLE_FILE_COMMENTS, 'rb')
		hitSubmissions = pickle.load(pklSubmissions)
		hitComments = pickle.load(pklComments)
		pklSubmissions.close()
		pklComments.close()
	except IOError:
		pass # move on with empty arrays

ticksSinceSubmission = 0 # MONITOR_INTERVAL intervals
while True:
	topSubmissions = r.get_subreddit(TARGET_REDDIT).get_hot(limit=SUBMISSIONS_TO_MONITOR)
	oldNumHitSubmissions = len(hitSubmissions)
	oldNumHitComments = len(hitComments)
	mostPopularComment = None
	aggregateCommentsText = ''

	try:
		for submission in topSubmissions:
			if DEBUG: print 'Checking ' + submission.title + '...'
			if submission.id not in hitSubmissions:
				if not DEBUG: submission.upvote()
				comments = submission.comments_flat
				for comment in comments:
					try:
						if mostPopularComment == None or comment.ups > mostPopularComment.ups:
							mostPopularComment = comment
					except Exception: # "MoreComments" again
						continue

				commentsText = getCommentsText(comments)
				aggregateCommentsText += commentsText
				if len(commentsText) > COMMENT_THRESHOLD: # TODO
					newPostString = markovComments(commentsText)
					if not DEBUG: submission.add_comment(newPostString)
					hitSubmissions.append(submission.id)

					print 'NEW POST!'
					print '"' + newPostString + '"'
					print submission.permalink.encode('ascii', 'ignore')
					if DEBUG: print '(DEBUG MODE: No post submitted)'
					print

		if mostPopularComment and mostPopularComment.id not in hitComments:
			if DEBUG:
				print 'Most popular comment:'
				print str(mostPopularComment)
				print mostPopularComment.permalink

			newReplyString = markovComments(aggregateCommentsText)
			if not DEBUG: mostPopularComment.reply(newReplyString)
			hitComments.append(mostPopularComment.id)

			print 'NEW REPLY!'
			print '" ' + newReplyString + '"'
			print mostPopularComment.permalink.encode('ascii', 'ignore')
			if DEBUG: print '(DEBUG MODE: No reply submitted)'
			print


		if REMEMBER_HIT:
			if len(hitSubmissions) != oldNumHitSubmissions: # we added submissions, repickle
				pklFile = open(PICKLE_FILE_SUBMISSIONS, 'wb')
				pickle.dump(hitSubmissions, pklFile)
				pklFile.close()

			if len(hitComments) != oldNumHitComments:
				pklFile = open(PICKLE_FILE_COMMENTS, 'wb')
				pickle.dump(hitComments, pklFile)
				pklFile.close()

		if ticksSinceSubmission * MONITOR_INTERVAL >= NEW_SUBMISSION_INTERVAL:
			ticksSinceSubmission = 0
		"""	print 'NEW SUBMISSION!'
			topSourceSubmissions = r.get_subreddit(NEW_SUBMISSIONS_REDDIT).get_hot(limit=10)
			aggregateCommentsText = ''
			for submission in topSourceSubmissions:
				if DEBUG: print 'Aggregating ' + submission.title.encode('ascii', 'ignore')
				aggregateCommentsText += getCommentsText(submission.comments_flat)

			newSubmissionTitle = markovComments(aggregateCommentsText).upper()
			if not DEBUG: r.submit(TARGET_REDDIT, newSubmissionTitle, text=markovComments(aggregateCommentsText.upper()))
			print '"' + newSubmissionTitle + '"'
			if DEBUG: print '(DEBUG MODE: No submission made)'
			print"""

		print 'Tick... ' + str(NEW_SUBMISSION_INTERVAL - (ticksSinceSubmission * MONITOR_INTERVAL)) + ' seconds until new submission...'
		ticksSinceSubmission += 1
		time.sleep(MONITOR_INTERVAL)
	except urllib2.HTTPError: # ignore urllib2 errors
		pass
	except urllib2.URLError: # ignore urllib2 errors
		pass
