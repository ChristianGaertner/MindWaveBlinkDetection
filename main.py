'''

Analyse raw mindwave curves.

MIT License
===========

Copyright (c) 2015 Christian Gaertner <chrisdagardner@gmail.com>

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.

'''

from numpy import array
import sys

def read(file):
	'''reads the data file into a list and converts them to integers
	'file' path to a text file

	Returns list of integers
	'''
	with open(file) as f:
		# read all data into a list
		strings = f.readlines()
		# remove title from list
		del strings[0]
		# convert to integers, but remove empty strings first
		'''
		TODO: see if the filter is really needed, since there should
		be no empty data strings
		With a dataset of 20 000 lines the filter method takes appr. 0.002 seconds
		longer...
		'''
		return map(int, filter(None, strings))

def peakdet(data, threshold):
	'''A very simple peak detection,
	it just returns the indices at which the values are above the threshold.

	Returns list of indices
	'''
	indices = []
	for i, x in enumerate(data):
		if x > threshold:
			indices.append(i)

	return indices


def cluster(data, threshold):
	'''A simple numbering clustering algorithm.
	'data' should be a list of numbers, which should get clustered.
	The 'threshold' is the biggest gap which can exist between elements
	before they will be seperated into two clusters.
	
	Returns a list of lists with the original numbers, clustered.
	'''
	#data.sort()
	groups = [[data[0]]]

	for x in data[1:]:
		if abs(x - groups[-1][-1]) <= threshold:
			groups[-1].append(x)
		else:
			groups.append([x])

	return groups


def guishow(data, maxtab):
	'''Plots the data and maxtab with matplotlib
	'data' will be drawn as graph
	'maxtab' will be scattered with red dots on the 'data' graph

	Returns None
	'''
	from matplotlib.pyplot import plot, scatter, show
	plot(data)
	scatter(array(maxtab), [0] * len(maxtab), color='red')
	show()

def main():
	ddf = read('data/data0.txt')
	# backticks are for string + int concatenation
	print 'Analyzing ' + `len(ddf)` + ' elements'

	maxtab = peakdet(ddf, 500)

	maxtab = cluster(maxtab, 100)

	peaks = []

	for g in maxtab:
		peaks.append(reduce(lambda x, y: x + y, g) / len(g))


	print 'Found ' + `len(peaks)` + ' peaks'
	print peaks

	if len(sys.argv) > 1 and sys.argv[1].strip() == 'gui':
		guishow(ddf, peaks)
	





if __name__ == "__main__":
    main()