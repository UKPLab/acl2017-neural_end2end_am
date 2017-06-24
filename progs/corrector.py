#! /usr/bin/python

import sys
sys.path.append("Eval")
from docReader import readDocs

# FIX the following:
# 1) Something starts with "I-"
# 2) A component is not homogenous

# SAMPLE RUN:
# python2 corrector.py Eval/prediction/maj_best10.out.corr.abs 
# (note that this won't fix anything, because the file already has proper format)
# also try out this: python2 corrector.py toFix.dat

def fixBegins(doc,field=2):
  prev = "O"
  newdoc = []
  for line in doc:
	x = line.split("\t")
	label = x[field]
	m = label.split("-")
	l = m[0]
	if l=="I" and prev=="O":
	  m[0]="B"
	  x[field] = "-".join(m)
	prev = l
	newdoc.append("\t".join(x))
  return newdoc

def getMajority(lst):
  h = {}
  for el in lst:
	h[el] = h.get(el,0)+1
#  if len(h)>1: print "LEN>1"
  return sorted([(v,k) for k,v in h.iteritems()],reverse=True)[0][-1]

def fixLabels(doc,field=2):
  component = []
  components = {}
  cindex = 0
  for line in doc:
	x = line.split("\t")
	label = x[field]
	if label.startswith("B"):
	  if component!=[]:
		components[cindex] = getMajority(component)
		cindex += 1
		component = []
	  #l = label[1:]
	  component.append(label[1:])
	elif label.startswith("I"):
	  component.append(label[1:])
  if component!=[]:
	components[cindex] = getMajority(component)
  #print components
  cindex = 0
  for line in doc:
	x = line.split("\t")
	label = x[field]
	#if label.startswith("O"): print line
	if label.startswith("B"):
	  majLabel = components[cindex]
	  cindex += 1
	  #print majLabel; sys.exit(1)
	  x[field] = x[field][0]+majLabel
	elif label.startswith("I"):
	  x[field] = x[field][0]+majLabel
	print "\t".join(x)
	  
	  

docs = readDocs(sys.argv[1])
for doc in docs:
  newdoc = fixBegins(doc)
  fixLabels(newdoc)
  print 
