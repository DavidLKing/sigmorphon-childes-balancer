#!/usr/bin/env python3

import sys
import operator
import nltk
import argparse
import string
import pdb
from math import *

def loadingBar(i, N, size):
    percent = float(i) / float(N)
    sys.stdout.write("\r"
                     + str(int(i)).rjust(3, '0')
                     +"/"
                     +str(int(N)).rjust(3, '0')
                     + ' ['
                     + '='*ceil(percent*size)
                     + ' '*floor((1-percent)*size)
                     + ']')

def clean_str(string):
    # List of one off edits
    replace_these = {
        'ß' : 'ss'
    }

    for item in replace_these:
        string = string.replace(item, replace_these[item])

    return string

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
        linnum = 0
        total = len(lines)
        print("Counting the frequencies in CHILDES")
        freqs = {}
        for l in lines:
            linnum += 1
            # loadingBar(linnum, total, 40)
            if linnum % 100000 == 0:
                print("On", linnum, "of", total)
            if l[0] not in ['@']:
                if not l.lower().startswith('*chi') and l.startswith("*"):
                    l = l.lower()
                    l = clean_str(l)
                    l = l.split('\t')
                    for word in nltk.word_tokenize(l[1].strip()):
                        if word not in freqs:
                            freqs[word] = 0
                        freqs[word] += 1
        return freqs

    def getUDFreqs(self, corpus):
        lines = open(corpus, 'r')
        linnum = 0
        total = 0
        for l in lines:
            total += 1
        lines.seek(0)
        print("Counting the frequencies in UDs")
        freqs = {}
        lexfreqs = {}
        lex2form = {}
        form2lex = {}
        for l in lines:
            linnum += 1
            # loadingBar(linnum, total, 40)
            if linnum % 100000 == 0:
                print("On", linnum, "of", total)
            if l[0] not in ['#']:
                l = l.lower()
                l = clean_str(l)
                l = l.split('\t')
                if len(l) > 1:
                    wordform = l[1].lower()
                    lexeme = l[2].lower()
                    if wordform not in freqs:
                        freqs[wordform] = 0
                    if lexeme not in lexfreqs:
                        lexfreqs[lexeme] = 0
                    if lexeme not in lex2form:
                        lex2form[lexeme] = set()
                    # if wordform not in form2lex:
                    # TODO how to deal with homomorphs?
                    form2lex[wordform] = lexeme
                    freqs[wordform] += 1
                    lexfreqs[lexeme] += 1
                    lex2form[lexeme].add(wordform)
        lines.close()
        return freqs, lexfreqs, lex2form, form2lex

class Balance:
    def __init__(self):
        pass

    def how_close(self, feat, poss_feats):
        diffs = {}
        for pf in poss_feats:
            diff = feat - poss_feats[pf]
            diffs[pf] = len(diff)
        argmin = min(diffs, key=diffs.get)
        if diffs[argmin] > 0:
            winner = ';'.join(list(feat))
            poss_feats[winner] = feat
        else:
            winner = argmin
        return winner, poss_feats

    def clean_feats(self, poss_feats, line):
        # line = line.upper()
        feat = set(line.split(';'))
        return self.how_close(feat, poss_feats) 
    
    def unimorphInput(self, dataDict, _file):
        print("Indexing dict with target form")
        poss_feats = {}
        array = open(_file, 'r').readlines()
        for line in array:
            feats = line.strip().split('\t')[2]
            poss_feats[feats] = set(feats.split(';'))
            line = line.lower()
            line = clean_str(line)
            line = line.strip()
            try:
                key = line.lower().split('\t')[1]
            except:
                pdb.set_trace()
            if key not in dataDict:
                dataDict[key] = {}
            dataDict[key][line] = 'unimorph'
        return dataDict, poss_feats

    def udInput(self, dataDict, _file, poss_feats):
        print("Indexing dict with target form")
        array = open(_file, 'r').readlines()
        for line in array:
            if not line.startswith("#"):
                line = line.lower()
                line = clean_str(line)
                line = line.strip().split('\t')
                if len(line) > 1:
                    try:
                        key = line[1]
                    except:
                        pdb.set_trace()
                    feats = line[5]
                    if feats != "_":
                        feats, poss_feat = self.clean_feats(poss_feats, feats)
                        entry = line[2] + '\t' + line[1] + '\t' + feats
                        if key not in dataDict:
                            dataDict[key] = {}
                        if entry not in dataDict[key]:
                            dataDict[key][entry] = 'unideps'
        return dataDict

    def load_unideps(self, corpus, data, poss_feats):
        data = self.udInput(data, corpus, poss_feats)
        return data

    def load_unimorph(self, corpus, data):
        print("Loading unimorph data")
        # edit, make this a dict
        # data = {}
        data, poss_feats = self.unimorphInput(data, corpus)
        # data = self.catInput({}, train)
        # data = self.catInput(data, dev)
        # data = self.catInput(data, test)
        # data = [x.strip() for x in data]
        return data, poss_feats


    def balance(self, cdi, data):
        print("Balancing data")
        cdiTotal = len(cdi)
        sortedOutput = []
        sortedCdi = sorted(cdi.items(), key=operator.itemgetter(1))
        # pdb.set_trace()
        sortedCdi.reverse()
        for sc in sortedCdi:
            if sc[0] in data and sc[0] not in string.punctuation:
                # gountil = cdi[sc[0]]
                # while gountil > 0:
                for line in data[sc[0]]:
                    # if len(line.split('\t')) != 3:
                        # print("This entry is missing something:\n", line)
                        # pdb.set_trace()
                    sortedOutput.append(line)
                    # gountil -= 1
        devtest = []
        for word in data:
            if word not in sortedCdi and word not in string.punctuation:
                for line in data[word]:
                    if data[word][line] == 'unimorph':
                        devtest.append(line)
        print(len(sortedOutput), "found in Childes")
        print(len(devtest), "left for dev and test")
        print("Childes coverage:", len(sortedOutput) / cdiTotal)
        return sortedOutput, devtest

    def writeout(self, found, devtest, trainfile, devfile):
        outfile = open(trainfile, 'w')
        outfile_dev_test = open(devfile, 'w')
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
    parser.add_argument('-u', '--unimorph', help="unimorph corpus", required=True)
    parser.add_argument('-d', '--unidep', help="universal dependency corpus", required=True)
    parser.add_argument('-tr', '--train', help="training output", required=True)
    parser.add_argument('-dev', '--dev', help="dev output", required=True)
    args = parser.parse_args()

    f = Freq()
    b = Balance()
    # child directed input
    cdi = f.loadfiles(args.childes)
    udfreqs = f.getUDFreqs(args.unidep)
    data, poss_feats = b.load_unimorph(args.unimorph, {})
    data = b.load_unideps(args.unidep, data, poss_feats)
    found, devtest = b.balance(cdi, data)
    b.writeout(found, devtest, args.train, args.dev)
