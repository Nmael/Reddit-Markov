import re
import sys
from markov import Markov

class MarkovGrapher:
	def __init__(self, markov):
		self.markov = markov

	def graph(self):
		# node definitions
		nodes = self.traverseChain(self.markov)

		# edge definitions
		edges = set()
		for node in nodes:
			totalEvents = 0.0
			if node not in self.markov.freqMap.keys(): # end nodes have no edges
				break

			for follower in self.markov.freqMap[node]: # count number of words this starter links to
				totalEvents += self.markov.freqMap[node][follower]

			for follower in self.markov.freqMap[node]:
				edges.add((node, follower, str(round(self.markov.freqMap[node][follower] / totalEvents, 3)*100) + '%'))

		self.printTGF(nodes, edges)

	def traverseChain(self, chain):
		"""Returns a set containing every unit in the markov chain."""

		found = set()
		unitsRemaining = set()

		# load first level of keys
		for key in self.markov.freqMap.keys():
			for futureUnit in self.markov.freqMap[key]:
				found.add(key)
				unitsRemaining.add(key)

		# load all referenced keys, quote-unquote recursively
		while len(unitsRemaining) > 0:
			thisUnit = unitsRemaining.pop()
			if thisUnit not in self.markov.freqMap.keys(): # ending unit
				break

			for nextUnit in self.markov.freqMap[thisUnit]:
				if nextUnit not in found:
					found.add(nextUnit)

				if nextUnit not in self.markov.freqMap.keys():
					break

				for futureUnit in self.markov.freqMap[nextUnit]:
						unitsRemaining.add(futureUnit)

		return found

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
