import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import sys
import pdb

sig = open('sig-input/german-task1-train', 'r')
uni = open('unimorph/deu/deu', 'r')

def sig_extract(sig_lines):
    corpus_feats = []
    for line in sig_lines:
        line = line.split()
        feats = line[1]
        feats = feats.split(',')
        feats = [f.split('=')[1] for f in feats]
        corpus_feats.append(feats)
    return corpus_feats


def uni_extract(uni_lines):
    corpus_feats = []
    for line in uni_lines:
        line = line.strip().split('\t')
        feats = line[2].split(';')
        corpus_feats.append(feats)
    return corpus_feats


def bag(feats, array):
    for f in feats:
        array += f
    return array

sig_feats = sig_extract(sig)
uni_feats = uni_extract(uni)

sig_bag = bag(sig_feats, [])
sig_bag = dict(pd.value_counts(sig_bag))
# list(zip(*np.unique(sig_bag, return_counts=True)))
uni_bag = bag(uni_feats, [])
uni_bag = dict(pd.value_counts(uni_bag))
# list(zip(*np.unique(uni_bag, return_counts=True)))


sig_series = pd.Series(sig_bag)
print(sig_series.describe())

uni_series = pd.Series(uni_bag)
print(uni_series.describe())

sns.distplot([int(x) for x in sig_bag.values()])

pdb.set_trace()