import sys
import os
from os import walk
import time

import openpyxl
import xlrd
import csv
from tqdm import *


#This is a python script to preprocess all of the excel spreadsheets and stuff everything into csv files for later use.

#scratch work
'''
	wb = xlrd.open_workbook(DATA_DIR + 'noncampusarrest101112.xls')
	sheet_names = wb.sheet_names()
	xl_sheet = wb.sheet_by_name(sheet_names[0])
	row = xl_sheet.row(0)
	print sheet_names
	print xl_sheet
	print row

TO DO:
	Remove last commas in text file, Use join instead
	Put stats in csv files (total number, headers, etc)

	We should then have all files converted to csv ready to use!
'''


'''CONSTANTS'''
XLS_DIR = '../data/crime-data/xls-files/'
DATA_DIR = '../data/crime-data/'
CSV_DIR = ''
FILES = []
FILE_EXTENSIONS = ['xls', 'xlsx']
'''END CONSTANTS'''

def grabFiles():
	print "Grabbing files from directory %s" %XLS_DIR
	for (dirpath, dirnames, filenames) in walk(XLS_DIR):
		for file in filenames:
			extension = file.split('.')[1]
			if extension == 'xls' or extension == 'xlsx':
				FILES.append(file)
		break
	print "Grabbed %d files" %len(FILES)
	return FILES

def makeDirectory():
	print "Making target directory for csv-files"
	if not os.path.exists(DATA_DIR + 'csv-files'):
		os.makedirs(DATA_DIR + 'csv-files')
		print "Directory made at %s" %(DATA_DIR + 'csv-files')
		return DATA_DIR + 'csv-files'
	else:
		print "Directory already exists at %s!" %(DATA_DIR + 'csv-files')
		return DATA_DIR + 'csv-files'

#Function takes in open-file buffer and list of values to write
def writeLineToFile(fileToWrite, lineToWrite):
	#print "entering WriteLineToFile Func"
	for value in lineToWrite:
		if value != '':
			fileToWrite.write(value + ',')
		elif value == '':
			fileToWrite.write('NULL,')
	# Added the following two lines to remove the comma at the end -DJC
	fileToWrite.seek(-1, os.SEEK_END)
	fileToWrite.truncate()
	fileToWrite.write('\n')

def main():
	START_TIME = time.time()

	#Grabs files in DATA_DIR, makes directory for csv files
	FILES = grabFiles()
	CSV_DIR = makeDirectory()

	for file in FILES:
		extension = file.split('.')[1]
		filename =  file.split('.')[0]

		if extension in FILE_EXTENSIONS:

			print "Writing " + filename + '.' + extension + '...'
			wb = xlrd.open_workbook(XLS_DIR + file)
			sheet = wb.sheet_by_index(0)
			csv_file = open(CSV_DIR + '/' + file.split('.')[0] + '.csv', 'wb')
			wr = csv.writer(csv_file, quoting=csv.QUOTE_ALL)

			csv_file.write(filename + '.csv' + '\n')


			for rownum in trange(sheet.nrows):
				valrow = sheet.row_values(rownum)
				vals = []
				#Load with strings of values
				for val in valrow:
					try:
						vals.append(str(val))
					except:
						vals.append('')
				#If this row was the first it has attributes
				#print vals[0]
				if vals[0] == 'UNITID_P':
						writeLineToFile(csv_file, vals)
				else:
						writeLineToFile(csv_file, vals)


			csv_file.close()

	print "Done writing"
	END_TIME = time.time()

	print str(END_TIME - START_TIME) + "seconds passed"

if __name__ == '__main__':
	main()
