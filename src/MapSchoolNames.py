import os
import sys
import time
from Levenshtein import *

def main():


	schoolSetOne = ['University of Massachusetts at Amherst', 'Georgetown University', 'Georgetown College']

	schoolSetTwo = ['University of Massachusetts - Amherst', 'University of Massachusetts at Lowell', 'Georgetown College']

	for school in schoolSetOne:
		dist = 100
		for item in schoolSetTwo:
			dist = distance(school, item)
			print "LSDist of %s and %s is %s" %(school, item, str(dist)) 

if __name__ == '__main__':
	main()
