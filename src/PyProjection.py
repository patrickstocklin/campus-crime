import os
import sys
import argparse

'''
This python module performs a column-projection on a csv file, allowing
users to slice their csv files by index

TODO:
	Handle Exceptions like OutOfScope or FileDoesNotExist
'''

'''CONSTANTS'''
DATA_DIR = '../data/'
CSV_DIR = '../data/csv-files/'
FILENAME = ''

NEW_LINE_BREAK = "\n"*1
LINE_PARTITION = "="*80
'''END CONSTANTS'''

'''
Grabs Indices as raw input, returns as a list of integers
e.g. '0,3-5,7,8,9-12' -> raw_input
'''
def grabIndices():
	indices = []
	userInput = raw_input().split(',')
	for item in userInput:
		if '-' not in item:
			indices.append(int(item))
		elif '-' in item:
			'''return list of range from lower->upper'''
			rangeWindow = grabIndicesGivenRange(item)
			for index in rangeWindow:
				indices.append(index)
	return indices

'''
Given a range 'LB-UP', returns all integers in between as a list
'''
def grabIndicesGivenRange(indexRange):
	indices = []
	lowerLimit, upperLimit = int(indexRange.split('-')[0]), int(indexRange.split('-')[1])
	for indexNumber in range(lowerLimit,upperLimit+1):
		indices.append(indexNumber)
	return indices

'''
Given a file, returns a list of attributes denoted by column-index
'''
def grabFileHeader(filename):
	with open(CSV_DIR + filename, 'rw') as f:
		f.readline()
		header = f.readline()
		f.close()
	headers = header.split(',')
	for index in range(0,len(headers)):
		headers[index] = headers[index] + ' (' + str(index) + ')'
	return headers

'''
given a fileName, directory to store, and set of indices, returns the sliced file
'''
def sliceFile(filename, fileDirectory, indices):
	indicesSplit = "[" + ",".join(str(index) for index in indices) + "]"
	targetFile = fileDirectory + filename.split('.')[0] + indicesSplit + ".csv"
	with open(CSV_DIR + filename, 'rw') as f:
		with open(targetFile, 'wr+') as w:
			w.write(filename.split('.')[0] + indicesSplit + ".csv" + '\n')
			for line in f:
				if line == filename + '\n':
					pass
				else:
					sliceAndWriteLineToFile(line, w, indices)
			w.close()
		f.close()
	return targetFile

'''
Given a line, fileBuffer, and set of indices to keep, writes to the file
'''
def sliceAndWriteLineToFile(lineToSlice, fileToWrite, indices):
	lineValues = lineToSlice.split(',')
	for x in range(0, len(lineValues)):
		if x in indices:
			fileToWrite.write(lineValues[x].strip() + ',')
	fileToWrite.seek(-1, os.SEEK_END)
	fileToWrite.truncate()
	fileToWrite.write('\n')

'''
Makes Directory /Dataset/sliced-csvs/ if non-existent
'''
def makeDirectory():
	if not os.path.exists(DATA_DIR + 'sliced-csvs'):
		os.makedirs(DATA_DIR + 'sliced-csvs')
	return DATA_DIR + 'sliced-csvs/'

'''
Prints Instructions, Takes in File Headers with Indices
'''
def displayInstructions(fileHeader):
	print LINE_PARTITION
	print "PyProjection.py"
	print LINE_PARTITION
	print "Please enter the indices of the columns you wish to grab"
	print NEW_LINE_BREAK
	print "You can select multiple columns by adding a dash between indices"
	print NEW_LINE_BREAK
	print "e.g. '0-2,4,6-8' will grab the first 3 columns, 5th, and 7th-9th"
	print NEW_LINE_BREAK
	print "Enter values as a sequence separated by commas"
	print LINE_PARTITION
	print "The attributes of the file %s are as follows:" %(FILENAME)
	print NEW_LINE_BREAK
	print fileHeader
	print LINE_PARTITION
	print NEW_LINE_BREAK

'''
MAIN
'''
def main():
	parser = argparse.ArgumentParser(description="A python script to slice CSVs by column-index")
	parser.add_argument('-f', nargs=1, 
		help='filename of csv to slice')
	args = parser.parse_args()
	
	FILENAME = str(args.f[0])

	headers = grabFileHeader(FILENAME)
	displayInstructions(headers)
	indices = grabIndices()
	targetDirectory = makeDirectory()
	slicedFile = sliceFile(FILENAME, targetDirectory, indices)

	print "Sliced File stored in " + slicedFile

if __name__ == '__main__':
	main()
