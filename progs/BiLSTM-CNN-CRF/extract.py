#! /usr/bin/python

import sys

doRead=False
A=[]
for line in sys.stdin:
  line = line.strip()
  if line.startswith("Epoch"):
	doRead = True
	epoch = line
	#print "Epoch is",epoch
	continue
  if len(line)>0 and line[0]=="1":
	z = line.split("\t")
	if z[0]!="1": 
		x = A[-1]
		x.append(line)
		continue
	if doRead==True:
	  A = []
	  doRead=False
	A.append([])
	x = A[-1]
	x.append(line)
  elif len(line)>0:
	z = line.split("\t")
	try: new = int(z[0])
	except ValueError: continue
	x = A[-1]
	x.append(line)

for essay in A:
	if len(essay)==0: continue 
	for word in essay:
	  print word.strip()
	print
