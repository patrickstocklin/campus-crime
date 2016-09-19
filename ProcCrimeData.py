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
# the function writes the content of each file as a multidimensional
# array of strings
def grabData(includeHateCrimeData):
	FILES = []
	print "Grabbing files from directory %s" %DATA_DIR
	for (dirpath, dirnames, filenames) in walk(DATA_DIR):
		for filename in filenames:
			name = filename.split('.')[0]
			extension = filename.split('.')[1]
			if extension == 'csv' and True if includeHateCrimeData else 'hate' not in name:
				with open(DATA_DIR + filename, 'r') as csvfile:
					print 'Grabbing data from '+ filename
					file_reader = csv.reader(csvfile, delimiter=',', quotechar='|')
					file_str = ''
					file_lines = []
					for row in file_reader:
						file_lines.append(row)
					FILES.append(file_lines)

	print "Grabbed %d files" %len(FILES) +"\n"
	return FILES

# Get data from line element, handles NULL case
def getData(element):
	return 0. if element == 'NULL' else float(element)


'''
 This function checks for information in the crime stored
 in numerical values
 
 @param type:      Which type of data we are looking at (Arrests, Crime, Discipline, Hate)
 @param line:      Array of terms in the line (stored as strings)
 @param output:    the output data in writeToDict()
 @param univ_name: the name of the university the data is about
 @param total:     the section where the total number of crimes is tracked
 @param sections:  An array of strings that indicate which
                   sections of the data to update. Traversed
                   in parallel with indicies
 @param years:     Years we are examining
'''
def writeLineToData(type, line, output, univ_name, total, sections, years):
	if output[univ_name]['City'] == None:
		output[univ_name]['City'] = line[ len(line) - 3 - (len(sections) * len(years)) - 9 ]
	if output[univ_name]['State'] == None:
		output[univ_name]['State'] = line[ len(line) - 3 - (len(sections) * len(years)) - 8 ]

	indices = [ i+len(line)-(3+len(years)*len(sections)) for i in range(len(years)*len(sections)) ]
	for i in range(len(indices)):
		if sections[i/len(years)]+' '+years[i/len(sections)] not in output[univ_name]:
			output[univ_name][sections[i/len(years)]+' '+years[i/len(sections)]] = getData( line[indices[i]] )
		else:
			output[univ_name][sections[i/len(years)]+' '+years[i/len(sections)]] += getData( line[indices[i]] )


	# Adding the info to the output dictionary
	# sections += sections + sections
	# for i in range(len(indices)):
	# 	if line[indices[i]] == 'NULL':
	# 		output[univ_name][sections[i]] += 0.
	# 	else:
	# 		output[univ_name][sections[i]] += float(line[indices[i]])
	# 		output[univ_name][total] += float(line[indices[i]])


# Process the data into a dictionary organized by University
def writeToDict(data):
	output = {}
	for file in data:
		filename = ''
		years = []
		for line in file:
			if len(line) == 1 or line[0] == "UNITID_P":
				if len(line) == 1: filename = line[0]
				print 'Parsing '+ filename
				# Keep track of the years this data covers
				years = filename.split('.')[0]
				years = [years[i] for i in range(len(years)-6, len(years))]
				years = [years[0]+years[1], years[2]+years[3], years[4]+years[5]]
				continue
			# Creating dictionary key with the university name
			univ_name = line[1]
			if univ_name not in output:
				output[univ_name] = { 'City':              None,
				                      'State':             None,
				                      'Pub or Priv':       line[ len(line)-17 ] }
				                      # 'Men':                getData( line[ len(line)-15 ] ),
				                      # 'Women':              getData( line[ len(line)-14 ] ),
				                      # 'Total Students':     getData( line[ len(line)-13 ] ),
				             		  # 'Total Arrests':      0. }
				             		  # 'Total Crimes':       0.,
				             		  # 'Murders':            0.,
				             		  # 'Negligible Mans.':   0.,
				             		  # 'Forced Entries':     0.,
				             		  # 'Nonforced Entries':  0.,  
				             		  # 'Robberies':          0.,
				             		  # 'Aggr. Assaults':     0.,
				             		  # 'Burglaries':         0.,
				             		  # 'Vehicular Mans.':    0., 
				             		  # 'Arsons':             0.  }
			if 'arrest' in filename:
				sections = ['Arrests w Weapon', 'Arrests w Drugs', 'Arrest w Liquor']
				writeLineToData('Arrests', line, output, univ_name, 'Total Arrests', sections, years)
			if 'crime' in filename:
				pass
			if 'discipline' in filename:
				pass
			if 'hate' in filename:
				pass
	print "Finished parsing files.\n"
	return output



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

		data = grabData(options['includeHateCrimeData'])
		data = writeToDict(data)
		print data['Delaware State University']


		END_TIME = time.time()
		print "Crime data collected in "+ str(round(END_TIME - START_TIME, 2)) +" seconds."

c = CrimeData({'includeHateCrimeData': False})
