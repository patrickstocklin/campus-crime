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

 @param line:      array of terms in the line (stored as strings)
 @param output:    the output data in writeToDict()
 @param univ_name: the name of the university the data is about
 @param total:     the section where the total number of crimes is tracked
 @param sections:  an array of strings that indicate which
                   sections of the data to update. Traversed
                   in parallel with indicies
 @param years:     years we are examining
'''
def writeLineToData(line, output, univ_name, total, sections, years):
	if output[univ_name]['City'] == None:
		output[univ_name]['City'] = line[ len(line) - 3 - (len(sections) * len(years)) - 9 ]
	if output[univ_name]['State'] == None:
		output[univ_name]['State'] = line[ len(line) - 3 - (len(sections) * len(years)) - 8 ]
	if output[univ_name]['Pub or Priv'] == None:
		output[univ_name]['Pub or Priv'] = line[ len(line) - 3 - (len(sections) * len(years)) - 5 ]

	indices = [ i+len(line)-(3+len(years)*len(sections)) for i in range(len(years)*len(sections)) ]
	if total not in output[univ_name]:
		output[univ_name][total] = 0.
	for i in range(len(indices)):  # This is a mess lol
		if sections[i/len(years)]+years[i/len(sections)] not in output[univ_name]:
			output[univ_name][sections[i/len(years)]+years[i/len(sections)]] = getData( line[indices[i]] )
			output[univ_name][total+years[i/len(sections)]] = getData( line[indices[i]] )
			output[univ_name][total] += getData( line[indices[i]] )
		else:
			output[univ_name][sections[i/len(years)]+years[i/len(sections)]] += getData( line[indices[i]] )
			output[univ_name][total+years[i/len(sections)]] += getData( line[indices[i]] )
			output[univ_name][total] += getData( line[indices[i]] )


# Process the data into a dictionary organized by University
def writeToDict(data):
	output = {}
	for file in data:
		filename = ''
		years = []
		for line in file:
			if len(line) == 1 or line[0] == "UNITID_P":
				if len(line) == 1:
					filename = line[0]
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
				                      'Pub or Priv':       None  }
			if 'arrest' in filename:
				sections = ['Arrests w Weapon ', 'Arrests w Drugs ', 'Arrests w Liquor ']
				writeLineToData(line, output, univ_name, 'Total Arrests', sections, years)
			elif 'crime' in filename:
				sections = ['Murders ', 'Negligible Mans. ', 'Forcible Entries ', 'Nonforcible entries ']
				sections += ['Robberies', 'Aggr. Assaults ', 'Burglaries ', 'Vehicular Mans. ', 'Arsons ']
				writeLineToData(line, output, univ_name, 'Total Crimes', sections, years)
			elif 'discipline' in filename:
				sections = ['Displ. Actions w Weapon ', 'Displ. Actions w Drugs ', 'Displ. Actions w Liquor ']
				writeLineToData(line, output, univ_name, 'Total Displ. Actions', sections, years)
			elif 'hate' in filename:
				sections = ['HC Murders ', 'HC Negligible Mans. ', 'HC Forcible Entries ']
				sections += ['HC Nonforcible Entries ', 'HC Robberies ', 'HC Aggr. Assault ']
				sections += ['HC Burglaries ', 'HC Vehicular Mans. ', 'HC Arsons ', 'HC Body Injuries ']
				writeLineToData(line, output, univ_name, 'Total Hate Crimes', sections, years)
	print "Finished parsing files.\n"
	badKeys = []
	for key in output:
		if output[key]['State'] != None and len(output[key]['State']) != 2:
			badKeys.append(key)
	for key in badKeys:
		del output[key]
	return output


# Write data to a pandas DataFrame
def writeToDataFrame(data):
	# List of all universities
	universities = []
	for key in data:
		if key not in universities:
			universities.append(key)
	universities.sort()

	# Columns of the table
	columns = ['City', 'State', 'Pub or Priv']
	years = ['05', '06', '07', '08', '09', '10', '11', '12', '13']

	arrSections = ['Arrests w Weapon ', 'Arrests w Drugs ', 'Arrests w Liquor ']
	for section in arrSections:
		for year in years:
			columns += [section+year]
	columns.append('Total Arrests')

	crimeSections = ['Murders ', 'Negligible Mans. ', 'Forcible Entries ', 'Nonforcible Entries ']
	crimeSections += ['Robberies ', 'Aggr. Assaults ', 'Burglaries ', 'Vehicular Mans. ', 'Arsons ']
	for section in crimeSections:
		for year in years:
			columns += [section+year]
	columns.append('Total Crimes')

	dispSections = ['Displ. Actions w Weapon ', 'Displ. Actions w Drugs ', 'Displ. Actions w Liquor ']
	for section in dispSections:
		for year in years:
			columns += [section+year]
	columns.append('Total Displ. Actions')

	hateSections = ['HC Murders', 'HC Negligible Mans. ', 'HC Forcible Entries ']
	hateSections += ['HC Nonforcible Entries ', 'HC Robbieries ', 'HC Aggr. Assaults ']
	hateSections += ['HC Burglaries ', 'HC Vehicular Mans. ', 'HC Arsons ', 'HC Body Injuries ']
	for section in hateSections:
		for year in years:
			columns += [section+year]
	columns.append('Total Hate Crimes')

	dataArray = []
	for univ in universities:
		univData = [data[univ]['City'], data[univ]['State'], data[univ]['Pub or Priv']]

		for secion in arrSections:
			for year in years:
				if (section+year) in data[univ]:
					univData.append(data[univ][section+year])
				else:
					univData.append('NULL')
		else: pass
		if 'Total Arrests' in data[univ]:
			univData.append(data[univ]['Total Arrests'])
		else:
			univData.append('NULL')

		for secion in crimeSections:
			for year in years:
				if (section+year) in data[univ]:
					univData.append(data[univ][section+year])
				else:
					univData.append('NULL')
		else: pass
		if 'Total Crimes' in data[univ]:
			univData.append(data[univ]['Total Crimes'])
		else:
			univData.append('NULL')

		for secion in dispSections:
			for year in years:
				if (section+year) in data[univ]:
					univData.append(data[univ][section+year])
				else:
					univData.append('NULL')
		else: pass
		if 'Total Displ. Actions' in data[univ]:
			univData.append(data[univ]['Total Displ. Actions'])
		else:
			univData.append('NULL')

		for section in hateSections:
			for year in years:
				if (section+year) in data[univ]:
					univData.append(data[univ][section+year])
				else:
					univData.append('NULL')
		if 'Total Hate Crimes' in data[univ]:
			univData.append(data[univ]['Total Hate Crimes'])
		else:
			univData.append('NULL')

		dataArray.append(univData)

	output = pd.DataFrame(np.array(dataArray), index=universities, columns=columns)
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
		print 'Collecting crime data into a DataFrame:\n'
		START_TIME = time.time()

		data = grabData(options['includeHateCrimeData'])

		data = writeToDict(data)
		self.dictionary = data

		data = writeToDataFrame(data)
		self.dataFrame = data

		END_TIME = time.time()
		print "Crime data collected in "+ str(round(END_TIME - START_TIME, 2)) +" seconds."

'''

To implement: Instantiate CrimeData class, which will have public values
              dictionary which is a Python dictionary which contains all
              of the information. 

'''
