#! /usr/bin/python

import sys
sys.path.append("Eval")
from docReader import readDocsFine

# Correct the following:
# A link may "go beyond" the number of argumentative components

# SAMPLE USAGE:
# python2 corrector2.py toFix2.dat

field=2

docs = readDocsFine(sys.argv[1],field=field)

def countArgumentative(doc,field=5):
  cnt = 0
  for c in doc:
	if c[0].strip().split("\t")[field].startswith("B"): cnt+=1
  return cnt

for doc in docs:
  ncomp = countArgumentative(doc,field)
  argindex = 0
  for comp in doc:
    for line in comp:
	line = line.strip()
	x = line.split("\t")
	label = x[field]
	if label.startswith("O"):
	  print line
	elif label.startswith("B"):
	  newlink = None
	  try:
		a,b,c = label.split(":")
		if int(b)+argindex>=ncomp or int(b)+argindex<0:
		  b = str(ncomp-argindex-1)
		  if b==0: b = -1
		  newlink = b
		label = ":".join([a,b,c])
	  except ValueError:
		pass
	  argindex += 1
	  x[field] = label
	  print "\t".join(x)
	else:
	  if newlink is not None:
		a,b,c = label.split(":")
		b = newlink
		label = ":".join([a,b,c])
		x[field] = label
	  print "\t".join(x)
  print
	

