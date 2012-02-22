import re
import sys
from markov import Markov

class MarkovGrapher:
	def __init__(self, markov):
		self.markov = markov

	def graph(self):
		# node definitions
		nodes = set()
		starters = self.markov.getStartingUnits()
		for starter in starters:
			nodes = nodes.union(self.traverseChain(starter))

		# edge definitions
		edges = set()
		for node in nodes:
			totalEvents = 0.0
			for follower in self.markov.freqMap[node]: # count number of words this starter links to
				totalEvents += self.markov.freqMap[node][follower]

			for follower in self.markov.freqMap[node]:
				edges.add((node, follower, str(round(self.markov.freqMap[node][follower] / totalEvents, 3)*100) + '%'))

		self.printTGF(nodes, edges)

	def traverseChain(self, starter):
		"""Returns a set of every unit referencd by starter."""

		return self.traverseChainHelper(starter, set([starter]))

	def traverseChainHelper(self, starter, referenced):
		"""Recursive component of traverseChain. referenced is a set of all words
		referenced up to this point."""

		for follower in self.markov.freqMap[starter]:
			if follower not in referenced:
				referenced = self.traverseChainHelper(follower, referenced)
				referenced.add(follower)

		return referenced

	def printTGF(self, nodes, edges):
		"""Outputs the given nodes and edges in Trivial Graph Format.
		nodes is a set of strings.
		edges is a set of three-tuples: (node1, node2, optional edge text)"""

		for node in nodes:
			print node, node

		print '#' # separates node definitions and edge definitions

		for edge in edges:
			text = edge[2] if len(edge) > 2 else ''
			print edge[0], edge[1], text

if __name__ == '__main__':
	if len(sys.argv) != 2:
		print 'Usage: ' + sys.argv[0] + ' <input file>'
		exit()

	textFile = open(sys.argv[1], 'r')
	collapseSpaces = re.compile(r'\s+')
	content = collapseSpaces.sub(' ', textFile.read())
	textFile.close()
	content = content.split(' ')

	mg = MarkovGrapher(Markov(content))
	mg.graph()
