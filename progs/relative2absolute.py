#! /usr/bin/python

import sys

# convert relative distances to absolute links in relations between argument components

# SAMPLE USAGE:
# ./relative2absolute.py ../data/conll/Essay_Level/dev.dat


def readComponents(lst):
    arguments = []
    index = 0
    rel2abs = {}
    for line in lst:
        line = line.strip()
        myindex,token,_,_,label = line.split()
        if label.startswith("B-"):
            tt = label.split(":")
            relation = None
            if len(tt)>1:
                try:
                    relation = int(tt[1])
                except ValueError:
                    relation = None
            arguments.append((index,relation))
            #rel2abs[index] = relation
        index += 1
    for (q,x) in enumerate(arguments):
        i,rel = x
        if rel!=None:
            #print q,i,x
            absolute = arguments[q+rel][0]
        else:
            absolute = None
        rel2abs[i] = absolute
    return arguments,rel2abs

def rewriteAbs(lst,rel2abs):
    i = 0
    for line in lst:
        line = line.strip()
        j = i+1
        myindex,token,_,_,label = line.split()
        if label.startswith("B-"):
            absposition = rel2abs[i]
        elif label.startswith("O"):
            absposition = None
        if absposition!=None:
            q = label.split(":")
            q[1] = str(absposition+1)
            label = ":".join(q)
        print "\t".join([str(j),token,label])
        i+=1

def readDocs(fn):
  docs = []
  doc = []
  for line in open(fn):
	if line.strip()=="":
		if doc!=[]: docs.append(doc)
		doc = []
	else:
		doc.append(line)
  if doc!=[]: docs.append(doc)
  return docs

if __name__ == "__main__":

    docs = readDocs(sys.argv[1])
    for doc in docs:
      #print doc
      args = readComponents(doc)
      rel2abs = args[1]
      rewriteAbs(doc,rel2abs)
      print 
