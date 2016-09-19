'''
This program processes the 2013 crime data in the CSV
files and writes the data to pandas DataFrame objects
'''

from os import walk
import pandas as pd
import numpy as np
import csv
import time


'''CONSTANTS'''
DATA_DIR = "./Dataset/csv-files/"
'''END CONSTANTS'''


# Grabbing files from data directory
# the function writes the content of each file to a multidimensional array
def grabData(includeHateCrimeData):
	FILES = []
	print "Grabbing files from directory %s" %DATA_DIR
	for (dirpath, dirnames, filenames) in walk(DATA_DIR):
		for filename in filenames:
			name = filename.split('.')[0]
			extension = filename.split('.')[1]
			if extension == 'csv' and True if includeHateCrimeData else 'hate' not in name:
				with open(DATA_DIR + filename, 'rb') as csvfile:
					print 'Grabbing data from '+ filename
					file_reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
					file_str = ''
					file_lines = []
					for row in file_reader:
						file_lines.append(''.join(row).split(','))
					FILES.append({'name': filename, 'content': file_lines})
		break

	print "Grabbed %d files" %len(FILES)
	return FILES

'''
TODO: Organzie data into pandas DataFrames
Need to specify how we want to organize data
'''

'''
Use tis class in other programs,
its constructor processes the CSV files
'''
class CrimeData:
	'''
	@param options (not required): Dictionary can contain
		- 'includeHateCrime': boolean which determines if we want to load hate crimes
		   hate crime files seem to be much larger so when we test we want this to be
		   false
	'''
	def __init__(self, options={'includeHateCrimeData': True}):
		START_TIME = time.time()

		files = grabData(options['includeHateCrimeData'])

		END_TIME = time.time()
		print "Crime data collected in "+ str(round(END_TIME - START_TIME, 2)) +" seconds."

c = CrimeData({'includeHateCrimeData': False})
