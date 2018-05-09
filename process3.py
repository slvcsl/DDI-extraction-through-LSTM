import numpy as np
import copy
from nltk import word_tokenize
import re

'''
Remember: this file is a little bit buggy (actually, the previous one is). 
It suppose the input file is composed of blocks (delimited by \n\n), containing 
each sentence (in 1 line) + the parse (like drug present etc).
The problem is actually some of the sentences are in 2 lines, so that the parsing 
fails. These are the sentences that have a first part delimited by [] and the 
"real" sentence in the following line.
For the moment, I only removed the \n so that the parsing is ok.
There are about 5 sentences with this problem. 
Only look for "]" in the text file and fix the problem.
Obvuiously the code (possibly of the previous script) should be modified to deal
with this problem.
'''

#train = open('dataset/step1/train_data.txt', 'r')
#train = open('dataset/step1/tmp.txt', 'r')

train = open('dataset/step2/train_data.txt','r')
#train =  open('dataset/test_data2.txt','r')

fw = open('dataset/step3/train_data.txt','w')
#fw = open('dataset//test_data3.txt','w')

def preProcess(sent):
	sent = sent.replace(',',' ,')
	sent = sent.replace('-',' ')
	sent = sent.replace('/',' / ')
	sent = re.sub('\d', "dg", sent)
	sent = ' '.join(word_tokenize(sent))
	return sent

def removeFirstPart(sent, simbol):
    splitted = sent.split(" "+simbol+" ");
    if(len(splitted)) > 0:
        if ("DRUGA" not in splitted[0]) and ("DRUGB" not in splitted[0]):
           # print simbol + " " + splitted[0]
           return (" "+simbol+" ").join(splitted[1:])
    return sent
   #return sent
   
i = 0
count = 0
for s in train.read().strip().split('\n'): #for each "block"
    sent =  preProcess(s.strip().split('\n')[0])	# The sentence
    pair = "\n".join(s.strip().split('\n')[1:])
    #sent = sent.split('\t')[1]
    sent_ori = copy.copy(sent)
    #print sent
    #print
    
    # remove nested parenthesis if they do not contain DRUGA, DRUGB
    
    sent = removeFirstPart(sent, ".")
    sent = removeFirstPart(sent, ",")
    sent = removeFirstPart(sent, ":")
    sent = removeFirstPart(sent, ";")
    sent = removeFirstPart(sent, "[")
    sent = removeFirstPart(sent, "]")
    
    fw.write(sent+'\n\n')
    fw.write(pair)
    fw.write('\n\n')

fw.close
train.close

    
'''
    e_dict = [], DRUGN , general DRUGN , DRUGN such as DRUGA , DRUGN , or ot
    for p in pair:
        d1, d1_type, d1_spain, d2, d2_type, d2_spain, ddi = p.strip().split('\t')

        if d1_spain not in e_dict :
			e_dict.append(d1_spain)
        if d2_spain not in e_dict :
			e_dict.append(d2_spain)

    for p in pair :		
	   	d1, d1_type, d1_spain, d2, d2_type, d2_spain, ddi = p.strip().split('\t')
		if d1 == d2 :
			continue;
		count += 1
	   	if ( (d1_spain.find(';') == -1) and (d2_spain.find(';') == -1)) :
			d1s,d1e = d1_spain.split('-')
			d2s,d2e = d2_spain.split('-')
			d1s = int(d1s); d1e = int(d1e); d2e = int(d2e); d2s=int(d2s)

	   	elif ((d1_spain.find(';') > -1) and (d2_spain.find(';') == -1)):
			
			daa, dbb = d1_spain.split(';')
			daa_s,daa_e = daa.split('-')
			daa_s = int(daa_s); daa_e = int(daa_e);
			
			dbb_s, dbb_e = dbb.split('-')
			dbb_s = int(dbb_s); dbb_e=int(dbb_e);

			d2s, d2e = d2_spain.split('-')
			d2s = int(d2s); d2e = int(d2e)
			
			if len( set(range(daa_s,daa_e) ) & set(range(d2s,d2e) ) ) != 0:
				d1s,d1e = dbb_s,dbb_e
			elif len( set(range(dbb_s, dbb_e) ) & set(range(d2s, d2e) ) ) != 0:
				d1s, d1e = daa_s, daa_e
			else:
				d1s,d1e = daa_s, daa_e

	   	elif ((d1_spain.find(';') == -1) and (d2_spain.find(';') > -1)):
			d21s,d21e = d2_spain.split(';')[0].split('-')
			d21 = [int(d21s), int(d21e)]
			d22s,d22e = d2_spain.split(';')[1].split('-')
			d22 = [int(d22s), int(d22e)]
			
			d1s,d1e = d1_spain.split('-')
			d1s = int(d1s); d1e = int(d1e)

			if len( set(range(d21[0],d21[1]) ) & set(range(d1s,d1e) ) ) != 0:
				d2s,d2e = d22
			elif len( set(range(d22[0],d22[1]) ) & set(range(d1s, d1e) ) ) != 0:
				d2s,d2e = d21
			else:
				d2s,d2e = d21  		 

	   	elif ((d1_spain.find(';') > -1) and (d2_spain.find(';') > -1)):
	  		d2s,d2e = d2_spain.split(';')[0].split('-')
			d1s,d1e = d1_spain.split(';')[0].split('-')
			d1s = int(d1s); d1e = int(d1e); d2e = int(d2e); d2s=int(d2s)

 		
		other = set(e_dict) - set([d1_spain, d2_spain])

		aaa = 'a'* (d1e - d1s + 1)
		dsent = sent_ori[:d1s] +aaa+ sent_ori[d1e+1:]
		bbb = 'b'* (d2e-d2s + 1) 
		dsent = dsent[:d2s] +bbb+ dsent[d2e+1:]
		
		ccc_list = []
#		print other
		cnt = 0
		for x1 in other:
			if x1.find(';')> -1:
				x1 = x1.split(';')[0]
			x1s,x1e = x1.split('-')
			x1s = int(x1s); x1e = int(x1e)
			ccc = str(cnt)* (x1e - x1s + 1)
	
			ccc_list.append(ccc)
			dsent = dsent[:x1s] +ccc+ dsent[x1e+1:]
			cnt+=1
			if cnt == 10:
				cnt = 0;

		dsent = dsent.replace(aaa,' DRUGA ')
		dsent = dsent.replace(bbb,' DRUGB ')
		for ccc in ccc_list:
#			print ccc
#			print dsent
			dsent = dsent.replace(ccc,' DRUGN ')
		dsent = preProcess(dsent)
		fw.write(dsent+'\n')
		fw.write(d1 +"\t"+ d1_type +"\t"+ d2 +"\t"+ d2_type+'\n')
		fw.write(ddi +'\n')			
	 	fw.write('\n')
print 'Number pair', count
	   ''' 





