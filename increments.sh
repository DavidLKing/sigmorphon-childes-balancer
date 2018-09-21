#!/usr/bin/env bash

mkdir data
mkdir data/500
mkdir data/500/raw
head -n 500 german-task1-train.balanced > data/500/raw/german-task1-train
cp german-task1-dev.balanced data/500/raw/german-task1-dev
cd data/500/
../../opennmt-input.py raw/german-task1-train raw/german-task1-dev
cd ../..

mkdir data/1000
mkdir data/1000/raw
head -n 1000 german-task1-train.balanced > data/1000/raw/german-task1-train
cp german-task1-dev.balanced data/1000/raw/german-task1-dev
cd data/1000/
../../opennmt-input.py raw/german-task1-train raw/german-task1-dev
cd ../..

mkdir data/2000
mkdir data/2000/raw
head -n 2000 german-task1-train.balanced > data/2000/raw/german-task1-train
cp german-task1-dev.balanced data/2000/raw/german-task1-dev
cd data/2000/
../../opennmt-input.py raw/german-task1-train raw/german-task1-dev
cd ../..

mkdir data/4000
mkdir data/4000/raw
head -n 4000 german-task1-train.balanced > data/4000/raw/german-task1-train
cp german-task1-dev.balanced data/4000/raw/german-task1-dev
cd data/4000/
../../opennmt-input.py raw/german-task1-train raw/german-task1-dev
cd ../..

mkdir data/6000
mkdir data/6000/raw
head -n 6000 german-task1-train.balanced > data/6000/raw/german-task1-train
cp german-task1-dev.balanced data/6000/raw/german-task1-dev
cd data/6000/
../../opennmt-input.py raw/german-task1-train raw/german-task1-dev
cd ../..

mkdir data/8000
mkdir data/8000/raw
head -n 8000 german-task1-train.balanced > data/8000/raw/german-task1-train
cp german-task1-dev.balanced data/8000/raw/german-task1-dev
cd data/8000/
../../opennmt-input.py raw/german-task1-train raw/german-task1-dev
cd ../..

mkdir data/10000
mkdir data/10000/raw
head -n 10000 german-task1-train.balanced > data/10000/raw/german-task1-train
cp german-task1-dev.balanced data/10000/raw/german-task1-dev
cd data/10000/
../../opennmt-input.py raw/german-task1-train raw/german-task1-dev
cd ../..
