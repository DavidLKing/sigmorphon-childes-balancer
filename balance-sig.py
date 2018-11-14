#!/usr/bin/env python3

import sys
import operator
import nltk
import argparse
import pdb

# nltk.data.path.append("/scratch2/king/nltk_data")



class Freq:
    def __init__(self):
        pass

    def loadfiles(self, childesFile):
        print("Loading CHILDES data")
        childesLines = open(childesFile, 'r').readlines()
        freqs = self.getFreqs(childesLines)
        return freqs

    def getFreqs(self, lines):
        print("Counting the frequencies in CHILDES")
        freqs = {}
        for l in lines:
            if l[0] not in ['@']:
                if not l.startswith('*CHI'):
                    l = l.split('\t')
                    for word in nltk.word_tokenize(l[1].strip()):
                        if word not in freqs:
                            freqs[word] = 0
                        freqs[word] += 1
        return freqs

class Balance:
    def __init__(self):
        pass

    def catInput(self, dataDict, _file):
        print("Indexing dict with target form")
        array = open(_file, 'r').readlines()
        for line in array:
            line = line.strip()
            try:
                key = line.split('\t')[2]
            except:
                pdb.set_trace()
            if key not in dataDict:
                dataDict[key] = []
            dataDict[key].append(line)
        return dataDict

    # needed for sigmorphon
    # def loadfiles(self, corpus):
    def loadfiles(self, corpus):
        print("Loading morph data")
        # edit, make this a dict
        data = {}
        data = self.catInput({}, corpus)
        # data = self.catInput({}, train)
        # data = self.catInput(data, dev)
        # data = self.catInput(data, test)
        # data = [x.strip() for x in data]
        return data

    def balance(self, cdi, data):
        print("Balancing data")
        cdiTotal = len(cdi)
        sortedOutput = []
        sortedCdi = sorted(cdi.items(), key=operator.itemgetter(1))
        sortedCdi.reverse()
        for sc in sortedCdi:
            if sc[0] in data:
                for line in data[sc[0]]:
                    sortedOutput.append(line)
        devtest = []
        for word in data:
            if word not in sortedCdi:
                for line in data[word]:
                    devtest.append(line)
        print(len(sortedOutput), "found in Childes")
        print(len(devtest), "left for dev and test")
        print("Childes coverage:", len(sortedOutput) / cdiTotal)
        return sortedOutput, devtest

    def writeout(self, found, devtest):
        outfile = open('german-task1-train.balanced', 'w')
        outfile_dev_test = open('german-task1-dev-test.balanced', 'w')
        for line in found:
            line += '\n'
            outfile.write(line)
        for line in devtest:
            line += '\n'
            outfile_dev_test.write(line)
        outfile.flush()
        outfile_dev_test.flush()
        outfile.close()
        outfile_dev_test.close()

if __name__ == '__main__':
    # define options
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--childes', help="CHILES data, concatted into 1 text file", required=True)
    parser.add_argument('-u', '--unimorph', help="corpus", required = True)
    args = parser.parse_args()

    f = Freq()
    b = Balance()
    # child directed input
    cdi = f.loadfiles(args.childes)
    data = b.loadfiles(args.unimorph)
    found, devtest = b.balance(cdi, data)
    b.writeout(found, devtest)
