import re
import sys
from markov import Markov

if len(sys.argv) != 2:
	print 'Usage: ' + sys.argv[0] + ' <input file>'
	exit()

textFile = open(sys.argv[1], 'r')
collapseSpaces = re.compile(r'\s+')
content = collapseSpaces.sub(' ', textFile.read())
textFile.close()
content = content.split(' ')

m = Markov(content)

# node definitions
starters = m.getStartingUnits()
followers = set()
for starter in starters:
	print starter, starter
	for follower in m.freqMap[starter]:
		if follower not in starters: # no repeats
			followers.add(follower) # automatically removes dupe followers

for follower in followers:
	print follower, follower

print '#' # separates node definitions and edge definitions

# edge definitions
for starter in starters:
	totalEvents = 0.0
	for follower in m.freqMap[starter]: # count number of words this starter links to
		totalEvents += m.freqMap[starter][follower]

	for follower in m.freqMap[starter]:
		print starter, follower, str(round(m.freqMap[starter][follower] / totalEvents, 3)*100) + '%'
