#!/usr/bin/env python
# coding: utf-8

# In[1]:


import sys
import numpy as np
import nltk
import pandas as pd
import pdb
from balance import Freq


# In[2]:


childes_data = open('childes-spanish/childes-spanish.txt', 'r').readlines()
ud_data = open('ud-spanish/spanish.conllu', 'r').readlines()
unimorph = open('uni-spanish/spa.txt', 'r').readlines()
overreg = open('Comp.Morph Participles.tsv.csv', 'r').readlines()


# In[3]:


twitter_data = pd.read_excel('Comp-Morph_Twitter data.xlsx')


# In[4]:


# print(ud_data[0:10])
def uniforms(unis, forms, freq_count):
    counts = {}
    for line in unis:
        line = line.strip().split('\t')
        if len(line) > 1:
            lemma = line[0]
            wordform = line[1]
            if wordform not in forms:
                if lemma in freq_count:
                    # print(lemma, wordform)
                    # print(lemma, freq_count[lemma])
                    if lemma not in counts:
                        counts[lemma] = 0
                    counts[lemma] += 1
    return counts


# In[5]:


def tweet_freq(tweets):
    total = 0
    counts = {}
    for doc in tweets[['text']].values.tolist():
        for line in doc:
            line = nltk.word_tokenize(line.strip())
            for word in line:
                if word not in counts:
                    counts[word] = 0
                counts[word] += 1
                total += 1
    return counts, total
        


# In[6]:


tw_freqs, tw_totals = tweet_freq(twitter_data)
#twitter_data[['text']].values.tolist()
# tw_freqs


# In[7]:


len(childes_data)


# In[8]:


len(ud_data)


# In[9]:


len(unimorph)


# In[10]:


f = Freq()


# In[11]:


ch_freqs = f.getFreqs(childes_data)


# In[12]:


ud_freqs, ud_lex_freqs, ud_lex2form, ud_form2lex = f.getUDFreqs(ud_data)


# In[13]:


# ud_lex_freqs['presidente']
ud_totals = sum(list(ud_lex_freqs.values()))
ch_totals = sum(list(ch_freqs.values()))
print("ch_totals", ch_totals)
print("ud_totals", ud_totals)
print("tw_totals", tw_totals)
# sum(list(tw_freqs.values())) ==  tw_totals


# In[14]:


def get_forms(annotations):
    # Kind of on inverted paradigm: {wordform: lemma...} more of a lookup table
    regs = []
    irregs = []
    for line in annotations:
        # if not line[3].startswith('supplet'):
        line = line.strip().split('\t')
        lemma = line[0]
        form = line[1]
        reg = line[2]
        regs.append((reg, lemma))
        irregs.append((form, lemma))
        # if reg not in regs:
        #     regs[reg] = lemma
        # if form not in irregs:
        #     irregs[form] = lemma
        # print(line)
    return regs, irregs


# In[12]:


overreg[1].strip().split('\t')


# In[15]:


reg_forms, irreg_forms = get_forms(overreg)
assert(len(irreg_forms) == len(reg_forms))


# In[16]:


def build_counts(irreg_forms, reg_forms, count_dict):
    data_list = []
    for irr, reg in zip(irreg_forms, reg_forms):
        lemma = irr[1]
        if irr[0] in count_dict:
            irr_freq = count_dict[irr[0]]
        else:
            irr_freq = 0
        if reg[0] in count_dict:
            reg_freq = count_dict[reg[0]]
        else:
            reg_freq = 0
        # pdb.set_trace()
        total = reg_freq + irr_freq
        if total > 0:
            if irr[0][0] != reg[0][0]:
                pdb.set_trace()
            data_list.append([lemma,
                              irr[0],
                              irr_freq,
                              irr_freq / total,
                              reg[0],
                              reg_freq,
                              reg_freq / total])
    data_frame = pd.DataFrame(data_list, columns=['lemma', 'irreg_form',
                                                  'irreg_count', 'irreg_ratio',
                                                  'reg_form', 'reg_count',
                                                  'reg_ratio'])
    return data_frame


# In[17]:


df_ud = build_counts(irreg_forms, reg_forms, ud_freqs)

# In[18]:


df_ch = build_counts(irreg_forms, reg_forms, ch_freqs)


# In[19]:


df_ud[['reg_ratio']].mean()


# In[20]:


df_ud[['irreg_ratio']].mean()


# In[21]:


df_ch[['reg_ratio']].mean()


# In[22]:


df_ch[['irreg_ratio']].mean()


# In[23]:


# freq = sum tokens / total corpus
df_ud[['reg_count']].sum() / ud_totals


# In[24]:


df_ud[['irreg_count']].sum() / ud_totals


# In[25]:


df_ch[['reg_count']].sum() / ch_totals


# In[26]:


df_ch[['irreg_count']].sum() / ch_totals


# In[36]:


df_ud.loc[df_ud['reg_count'] > 0]


# In[39]:


pd.options.display.max_rows = 4000
df_ud.loc[df_ud['irreg_count'] > 0]

