#!/usr/bin/env python3

import sys
from operator import itemgetter
import pdb

sigmorphtrain = open(sys.argv[1], 'r').readlines()
unimorphtrain = open(sys.argv[2], 'r').readlines()

def sig2unim(feats):
    unifeats = []
    feats = feats.split(',')
    for f in feats:
        f = f.split('=')
        if len(f) > 1:
            unifeats.append(f[1])
    newfeats = ';'.join(unifeats)
    return newfeats
    

def get_feats(data, field, factor_sep):
    group_feats = []
    factored_feats = []
    for datum in data:
        datum = datum.strip()
        datum = datum.split('\t')
        feats = datum[field]
        if factor_sep == ',':
            feats = sig2unim(feats)
        group_feats.append(feats)
        for f in feats.split(';'):
            factored_feats.append(f)
    return group_feats, factored_feats

def get_counts(feats):
    total = len(feats)
    counts = []
    for element in sorted(set(feats)):
        counts.append((element, feats.count(element)))
    counts = sorted(counts, key=lambda x: x[1])
    # return counts
    for c in counts:
        print('\t'.join([c[0], str(c[1]), str(c[1] / total)]))

def missing(uni, sig):
    # TODO CHANGE VARIABLE NAMES, THESE SWAP
    uni = set(uni)
    sig = set(sig)
    for feat in uni:
        if feat not in sig:
            print(feat)

sig_group, sig_fact = get_feats(sigmorphtrain, 1, ',')
uni_group, uni_fact = get_feats(unimorphtrain, 2, ';')

print("sig-group")
sg = get_counts(sig_group)
print()
print("uni-group")
ug = get_counts(uni_group)
print()
print("sig-fact")
sf = get_counts(sig_fact)
print()
print("uni-fact")
uf = get_counts(uni_fact)
print()

print("sig groups not in uni groups")
missing(sig_group, uni_group)
print()
print("uni groups not in sig")
missing(uni_group, sig_group)
print()
print("sig feats not in uni")
missing(sig_fact, uni_fact)
print()
print("uni feats not in sig")
missing(uni_fact, sig_fact)


# pdb.set_trace()

