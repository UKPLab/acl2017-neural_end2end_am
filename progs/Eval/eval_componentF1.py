#! /usr/bin/python

import sys,numpy as np
from docReader import readDocsFine2 as readDocsFine 

# SAMPLE RUN
# python2 eval_componentF1.py prediction/maj_best10.out.corr.abs ../../data/conll/Essay_Level/test.dat.abs 0.999 
# alpha = 0.999 is the F1 level as described in the paper

def extractComponents(lst,types):
  h = {}
  index = 0
  #print lst,types
  for ic,c in enumerate(lst):
	if types[ic]!=None:
	  h[index] = (types[ic],len(c))
	index += len(c)
  return h

# compute TP, FP, and FN
# as described in "End-to-End Argumentation Mining in Student Essays"
def getTP(pred,truth):
  TP = 0
  FP = 0
  FN = 0 
  for x in pred:
	if x in truth:
	  if truth[x]==pred[x]: 
		print x,truth[x]
		TP+=1
	  else:
		FP += 1
	else:
	  FP += 1
  for x in truth:
	if x not in pred:
	  FN += 1
	else:
	  if truth[x]!=pred[x]:
		FN += 1
  return TP,FP,FN

def checkApproxMatch( a,b , ratio=0.5 ):
  start_pos_a = a[0]
  start_pos_b = b[0]
  type_a = a[1][0]
  type_b = b[1][0]
  len_a = a[1][1]
  len_b = b[1][1]

  if type_a!=type_b: return False
  a_tok = set(range(start_pos_a,start_pos_a+len_a))
  b_tok = set(range(start_pos_b,start_pos_b+len_b))
  n = len(a_tok.intersection(b_tok))*1.0
  if n/max(len(a_tok),len(b_tok))>ratio: return True
  return False
 
def getTP_approx(pred,truth):
  TP = 0
  FP = 0
  FN = 0
  for x in pred:
        if x in truth:
          if truth[x]==pred[x]:
                print x,truth[x]
                TP+=1
          else:
		found = False
		for y in truth:
			if checkApproxMatch( (x,pred[x]),(y,truth[y]) ):
	                  TP+=1
        	          found = True
			  break
		if found==True: continue
                FP += 1
        else:
	  found = False
	  for y in truth:
		if checkApproxMatch( (x,pred[x]),(y,truth[y]) ): 
		  TP+=1
		  found = True
		  break
	  if found==True: continue
          FP += 1
  for x in truth:
	found = False
	for y in pred:
	  if checkApproxMatch( (x,truth[x]), (y,pred[y]) ):
		found = True
		break
	if found==True: continue
	FN += 1
  return TP,FP,FN


def getTP_approx_simple(pred,truth,ratio=0.5,verbose=False):
  TP = 0
  FP = 0
  FN = 0
  for x in pred:
	found = False
	for y in truth:
	  if checkApproxMatch( (x,pred[x]),(y,truth[y]), ratio=ratio ):
		found = True
		if pred[x]!=truth.get(x,None) and verbose==True: 
			print "APPROX_MATCH",(x,pred[x]),(y,truth[y])
		break
	if found==False: FP+=1
  for x in truth:
        found = False
        for y in pred:
          if checkApproxMatch( (x,truth[x]), (y,pred[y]), ratio=ratio ):
                found = True
                break
        if found==True: 
		TP += 1
	else:
        	FN += 1
  return TP,FP,FN



predDocs,argTypesDocs = readDocsFine(sys.argv[1],2)
truthDocs,argTypesDocsTruth = readDocsFine(sys.argv[2],2) # 4

TPS=0
FPS=0
FNS=0
printLocalF1=False
lengths=[]
try:
  ratio = float(sys.argv[3])
except IndexError:
  ratio=0.5
for idoc,doc in enumerate(predDocs):
  #print doc
  if len(doc)!=len(argTypesDocs[idoc]):
	print "PROBLEM",idoc
  try:
    pred_c = extractComponents(doc,argTypesDocs[idoc])
    truth_c = extractComponents(truthDocs[idoc],argTypesDocsTruth[idoc])
  except IndexError:
    sys.stderr.write("ERROR in doc %d\n"%(idoc))
    continue
  for q in truth_c:
	lengths.append(truth_c[q][-1])
  TP,FP,FN = getTP_approx_simple( pred_c,truth_c,ratio=ratio )
  TPS += TP
  FPS += FP
  FNS += FN
  if printLocalF1:
        denom = max(2*TP+FP+FN,1)
	print ":::",2*TP*1.0/denom
F1 = 2*TPS*1.0/(2*TPS+FPS+FNS)
print "#True Positives, False Positives, False Negatives, F1"
print TPS,FPS,FNS,F1
#print np.mean(lengths)
