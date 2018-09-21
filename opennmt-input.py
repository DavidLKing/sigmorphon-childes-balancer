#!/usr/bin/env python3

import sys
import pdb

class Rearrange:
    def __init__(self):
        pass

    def format(self, data):
        formatted = []
        for line in open(data, 'r').readlines():
            line = line.strip()
            line = line.split('\t')
            assert(len(line) == 3)
            lemma = list(line[0])
            target = list(line[1])
            feats = line[2]
            feats = feats.split(';')
            _input = feats + lemma
            formatted.append([_input, target])
        return formatted

    def load_lines(self, train, dev):
        tr_pairs = self.format(train)
        dev_pairs = self.format(dev)
        return tr_pairs, dev_pairs

    def writeem(self, pairs, srcout, tgtout):
        for p in pairs:
            srcout.write(' '.join(p[0]) + '\n')
            tgtout.write(' '.join(p[1]) + '\n')


    def writeout(self, train, dev):
        dev_in = open('valid-src.txt', 'w')
        dev_out = open('valid-tgt.txt', 'w')
        train_in = open('train-src.txt', 'w')
        train_out = open('train-tgt.txt', 'w')
        self.writeem(train, train_in, train_out)
        self.writeem(dev, dev_in, dev_out)

if __name__ == '__main__':
    print("Usage: ./opennmt-input.py trainfile devfile")
    r = Rearrange()
    train, dev = r.load_lines(sys.argv[1], sys.argv[2])
    r.writeout (train, dev)