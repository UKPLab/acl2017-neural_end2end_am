#! /usr/bin/python

import sys

def readDocs(fn):
  docs=[]
  doc=[]
  for line in open(fn):
	line = line.strip()
	if line=="":
	  if doc!=[]: docs.append(doc)
	  doc=[]
	else:
	  doc.append(line)
  if doc!=[]:
	docs.append(doc)
  return docs

def readDocsFine(fn,field=5):
  docs=[]
  doc=[[]]
  lastLabel = None
  for line in open(fn):
        line = line.strip()
        if line=="":
          if doc!=[[]]: docs.append(doc)
          doc=[[]]
	  lastLabel = None
        else:
	  x = line.split("\t")
	  label = x[field]
#	  print label
	  if label.startswith("B-"): # and lastLabel!="O" and lastLabel:
		if doc[-1]!=[]:
		  doc.append([])
	  elif label.startswith("O") and lastLabel!="O" and lastLabel:
		if doc[-1]!=[]:
		  doc.append([])
          doc[-1].append(line)
	  lastLabel = label[0]
  if doc!=[[]]:
        docs.append(doc)
  return docs

def readDocsFine2(fn,field):
  docs=[]
  doc=[[]]
  argTypes = []
  atype = []
  lastLabel = None
  for line in open(fn):
        line = line.strip()
        if line=="":
          if doc!=[[]]:
                docs.append(doc)
                argTypes.append(atype)
          doc=[[]]
          atype = []
          lastLabel = None
        else:
          x = line.split("\t")
          #print x
          label = x[field]
          if label.startswith("B-"): # and lastLabel!="O" and lastLabel:
                atype.append(label.split(":")[0])
                if doc[-1]!=[]:
                  doc.append([])
          elif label.startswith("O") and lastLabel!="O" and lastLabel:
                atype.append(None)
                if doc[-1]!=[]:
                  doc.append([])
          elif label.startswith("O") and lastLabel!="O":
                atype.append(None)
          doc[-1].append(line)
          lastLabel = label[0]
  if doc!=[[]]:
        docs.append(doc)
        argTypes.append(atype)
  return docs,argTypes



if __name__ == "__main__":

  import random

  docs = readDocs(sys.argv[1])
  random.shuffle(docs)
  n = int(sys.argv[2])
  for doc in docs[:n]:
	for line in doc:
	  x = line.split("\t")
	  x[0] = x[0].split("_")[-1]
	  print("\t".join(x))
	print
  for doc in docs[n:]:
	for line in doc:
          x = line.split("\t")
          x[0] = x[0].split("_")[-1]
          sys.stderr.write("\t".join(x)+"\n")
        sys.stderr.write("\n")


  sys.exit(1)

  docs=readDocsFine(sys.argv[1])
  n=int(sys.argv[2])
  print len(docs[n])
  print docs[n]
  for comp in docs[n]:
	for line in comp:
	  print line
