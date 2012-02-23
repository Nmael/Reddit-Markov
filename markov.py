import random
import string

class Markov:
	ENDING_PUNCT = ['.', '!', '?']
	units = []
	freqMap = dict()

	def __init__(self, units):
		self.units = units
		self.generateFreqMap(units)
	
	def generateFreqMap(self, units):
		"""Generates the Markov Chain as a dictionary: {unit: {followingUnit1: Probability, followingUnit2: Probability}}
		units is an array. It should contain the "things" that the Chain will try to string together (e.g., words, letters)."""

		for i in range(0, len(units)-1):
			thisWord = units[i]
			nextWord = units[i+1]

			if thisWord == '' or nextWord == '': continue # don't bother with empty units

			if thisWord in self.freqMap:
				if nextWord in self.freqMap[thisWord]:
					self.freqMap[thisWord][nextWord] += 1
				else:
					self.freqMap[thisWord][nextWord] = 1
			else:
				self.freqMap[thisWord] = dict()
				self.freqMap[thisWord][nextWord] = 1

		if units[-2] != '':
			self.freqMap[units[-2]] = dict() # we have no predictions for the final word.
																			 # note: we use units[-2] because split always makes units[-1] the empty string.
	
	def getStartingUnits(self, threshold=None):
		"""Returns potential "starting" units (defined as a unit that follows one
		of the ENDING_PUNCT punctuation marks and starts with an uppercase letter).
		If threshold is specified, will only returns units with >= threshold number
		of possible following units.  If no such unit exists, returns None."""

		starters = []
		if len(self.units) > 0: # add first unit
			if threshold == None or threshold <= len(self.units[0]): # reject if under threshold
				starters.append(self.units[0])

		for thisUnit in self.freqMap:
			for punct in self.ENDING_PUNCT:
				if thisUnit[-1] == punct: # this unit ends a sentence; try to add all its followers
					for followingUnit in self.freqMap[thisUnit]:
						if threshold == None or threshold <= len(self.freqMap[followingUnit]): # reject if under threshold
							if followingUnit[0] in string.uppercase and followingUnit not in starters: # must start with uppercase
								starters.append(followingUnit)

					break

		if len(starters) == 0: return None
		return starters

	def getRandomStartingUnit(self, threshold=None):
		"""Wrapper around getStartingUnit; returns a random starting word."""

		return random.choice(getStartingUnits(self, threshold))

	def getNextWord(self, seed):
		if seed:
			seedMap = self.freqMap[seed]

		if not seedMap: # never seen seed word; find a random seed
			return random.choice(list(self.freqMap.keys()))

		totalWeight = 0
		for weight in seedMap.values():
			totalWeight += weight

		rnd = random.randint(0, totalWeight-1)
		for successor in seedMap.keys():
			if rnd < seedMap[successor]:
				return successor
			else:
				rnd -= seedMap[successor]
	
	def getNNextWords(self, seed, n):
		lastWord = seed
		for i in range(0, n):
			newWord = self.getNextWord(lastWord)
			yield newWord
			lastWord = newWord
	
	def getNextSentence(self, seed, limit):
		if not seed: # find a random seed
			seed = random.choice(list(self.freqMap.keys()))

		lastWord = seed
		lastChar = lastWord[len(lastWord)-1]
		i = 0
		while lastChar != '.' and lastChar != '!' and lastChar != '?' and i < limit:
			newWord = self.getNextWord(lastWord)
			yield newWord
			lastWord = newWord
			lastChar = lastWord[len(lastWord)-1]
			i += 1
