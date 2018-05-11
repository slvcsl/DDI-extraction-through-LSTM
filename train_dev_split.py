# -*- coding: utf-8 -*-
import numpy as np

dev_percentage = 0.05 # portion of the data to include in the dev set
train_percentage = 1-dev_percentage # portion of the data to include in the train ser 

fr = open('dataset/step2/train_data.txt','r')
fval = open('dataset/train/train_data05.txt', 'w')
ftrain = open('dataset/train/train_data95.txt', 'w')

all_sentences =  fr.read().strip().split('\n\n') #"blocks"
N = len(all_sentences)

dev_indices = np.random.randint(0, N, int(np.floor(dev_percentage*N)))
dev_files = [all_sentences[i] for i in dev_indices]
train_files = [x for x in all_sentences if x not in dev_files]

for sentence in dev_files:
    fval.write(sentence+"\n\n")

for sentence in train_files:
    ftrain.write(sentence+"\n\n")

fr.close()
fval.close()
ftrain.close()