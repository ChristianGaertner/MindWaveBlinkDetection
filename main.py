'''

Analyse raw mindwave curves.

Takes about 7ms per datapoint, or about 0.14s for a dataset of 20 000 datapoints

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

from functools import reduce
import sys

from numpy import array
from scipy import signal


def read(file):
    """reads the data file into a list and converts them to integers
    'file' path to a text file

    Returns list of integers
    """
    with open(file) as f:
        # read all data into a list
        strings = f.readlines()
        # remove title from list
        del strings[0]

        # convert x.000 to just x
        strings = [s.split('.')[0] for s in strings]

        # convert to integers, but remove empty strings first
        '''
        TODO: see if the filter is really needed, since there should
        be no empty data strings
        With a dataset of 20 000 lines the filter method takes appr. 0.002 seconds
        longer...
        '''
        return map(int, filter(None, strings))


def peakdet(data, threshold, mindist=30):
    """A very simple peak detection,
    it just returns the indices at which the values are above the threshold.

    Returns list of indices
    """

    m_threshold = threshold
    l_threshold = 0.7 * threshold

    indices = []
    tmp_det = []

    # phase of peak detection
    # Valid phases are:
    # 0: idle
    # 1: first peak detected
    # 2: first peak detected, waiting for second peak
    # 3: seconds peak detected
    peak_det = 0

    # counts how long we've been waiting for the next maxima/minima
    in_peak = 0

    # Stores the sign of the first peak
    positive_start = True

    # Cycle through all the data,
    # i is the index, and x the value
    for i, x in enumerate(data):

        # This is the peak detection, if the value is greater
        # than the threshold we register a peak (for now)
        if abs(x) > threshold and peak_det is not -1:
            if peak_det == 0:
                # we found a new peak
                peak_det = 1

                # store for later, if we started with a positive or negative peak
                positive_start = x > 0

            # this means after the zero crossing we found the next connected peak
            elif peak_det != 1:
                # but if the sign of the peak is still the same, means that we had
                # not crossed the 0, thus not a peak we were after.
                if (x > 0 and positive_start) or (x < 0 and not positive_start):
                    print("lost(" + repr(peak_det) + "):")
                    print("\t" + repr(tmp_det))
                    print("\ti=" + repr(i) + ",x=" + repr(x) + ",p_s=" + repr(positive_start))
                    peak_det = -1
                else:
                    peak_det = 3

            tmp_det.append(i)
        elif peak_det == 1:
            # We just leaved the peak zone, switch to waiting
            peak_det = 2
        elif peak_det == 2:
            # We lower the threshold here, since we are expecting a peak, but only
            # if the sign of the value has changed
            if (x < 0 and positive_start) or (x > 0 and not positive_start):
                threshold = l_threshold

            # Waiting for the next peak, count upwards
            in_peak += 1
            if in_peak > mindist:
                # Max wait time for next peak exceeded. Reset
                peak_det = -1
                tmp_det = []
        elif peak_det == 3:
            # We just left the seconds peak zone. A complete peak has been detected.
            # Append the indicies to the main list and reset
            peak_det = -1
            indices.extend(tmp_det)
        else:
            # reset everything
            in_peak = 0
            peak_det = 0
            threshold = m_threshold
            positive_start = True
            tmp_det = []

    return indices


def lowPassFilter(data):
    cutoff = 2.4
    fs = 100
    order = 6

    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = signal.butter(order, normal_cutoff, btype='low', analog=False)
    return signal.lfilter(b, a, data)


def cluster(data, threshold):
    """A simple numbering clustering algorithm.
    'data' should be a list of numbers, which should get clustered.
    The 'threshold' is the biggest gap which can exist between elements
    before they will be seperated into two clusters.

    Returns a list of lists with the original numbers, clustered.
    """
    # data.sort()
    groups = [[data[0]]]

    for x in data[1:]:
        if abs(x - groups[-1][-1]) <= threshold:
            groups[-1].append(x)
        else:
            groups.append([x])

    return groups


def guishow(data, maxtab, altplot=None):
    """Plots the data and maxtab with matplotlib
    'data' will be drawn as graph
    'maxtab' will be scattered with red dots on the 'data' graph

    Returns None
    """
    from matplotlib.pyplot import plot, scatter, show, vlines

    plot(data)

    if altplot is not None:
        plot(altplot)

    scatter(array(maxtab), [0] * len(maxtab), color='red', s=50, zorder=3)
    vlines(array(maxtab), -1000, 1000, color='red', zorder=3)

    show()


def main():
    path = 'data/data0.txt'

    if len(sys.argv) > 1:
        if sys.argv[1] == "--help":
            print("main.py [path]|--help (gui)")
            return

        path = sys.argv[1]

    ddf = list(read(path))

    print('Analyzing ' + repr(len(ddf)) + ' elements')

    ddfC = lowPassFilter(ddf)

    maxtab = peakdet(ddfC, 250)

    maxtab = cluster(maxtab, 100)

    peaks = []

    for g in maxtab:
        peaks.append(reduce(lambda x, y: x + y, g) / len(g))


    # peaks = [p - 30 for p in peaks]

    print('Found ' + repr(len(peaks)) + ' peaks')
    print(peaks)

    if len(sys.argv) > 2 and sys.argv[2].strip() == 'gui':
        guishow(ddf, peaks, ddfC)


if __name__ == "__main__":
    main()