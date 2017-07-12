#! /usr/bin/python

import sys,codecs

# This converts LSTM-ER output to CONLL data.
# This is specialized code for Argumentation Mining. It uses heuristics to link arguments in case of AM structure violations.

# SAMPLE USAGE:
# ./toconll.py out_txt/test_0.split.txt test_0.split.pred.ann > conll/test_0.conll

def readPredictions(fn):
    components = {}
    relations = {}
    component2Name = {}
    for line in open(fn):
        line = line.strip()
        if line.startswith("T"):
            # component
            x = line.split("\t")
            ctype,start,end = x[1].split()
            components[int(start)] = (int(end),ctype)
            component2Name[x[0]] = int(start)
        elif line.startswith("R"):
            # relation
            x = line.split("\t")
            relation,arg1,arg2 = x[1].split()
            _,r1 = arg1.split(":")
            _,r2 = arg2.split(":")
            #print r1,r2,component2Name[r1],component2Name[r2]
            link1,link2 = component2Name[r1],component2Name[r2]
            if link1 in relations:
                if abs(link1-link2)<abs(link1-relations[link1][0]):
                    relations[link1] = (link2,relation)
            else:
                relations[link1] = (link2,relation)
    return components,relations

def readText(fn):
    return codecs.open(fn,"r","utf-8").read().strip()

def findClosestClaim(lst):
    myclosest = {}
    for x in lst:
        if lst[x][-1]=="Premise":
            closest = None
            closest_val = float("inf")
            for p in lst:
		if p==x: 
		#  print "CNT"
		  continue # added SE
                if lst[p][-1]=="Claim":
                    if abs(p-x)<closest_val:
                        closest_val = abs(p-x)
                        closest = p
                    #print x,p,abs(p-x),closest_val
            myclosest[x] = closest
            if myclosest[x] is None:
              closest = None
              closest_val = float("inf")
              for p in lst:
		if p==x: continue
                if lst[p][-1]=="Premise":
                    if abs(p-x)<closest_val:
                        closest_val = abs(p-x)
                        closest = p
              myclosest[x] = closest
    #print myclosest
    return myclosest


text = readText(sys.argv[1])
components,relations = readPredictions(sys.argv[2])
closest = findClosestClaim(components)

#print components,relations,closest

tokenized = text.split()
i = 0
token_id = 0
label = "O"
curEnd = None
curComp = None
textid2tokenid = {}
for token in tokenized:
    token_id += 1
    if i in components:
        textid2tokenid[i] = token_id
    i += len(token)+1
        
token_id = 0
i=0

for token in tokenized:
    token_id += 1
    if i in components:
        curEnd = components[i][0]
        curComp = components[i]
        label = "B-"+components[i][-1]
        if i in relations:
            curRel = relations[i]
            pointer = textid2tokenid[curRel[0]]
            rtype = relations[i][-1]
            if components[i][-1]=="Premise":
                rest = ":"+str(pointer)+":"+rtype
            elif components[i][-1]=="Claim":
                rest = ":"+rtype
            else:
                rest = ""
            #label = label+rest
        else:
	    # if it's not in the relation set, we do some heuristics
            if components[i][-1]=="Claim":
                rest = ":For" # heuristically add "For"
            elif components[i][-1]=="Premise":
		try:
                  dist = str(textid2tokenid[closest[i]])
		except KeyError:
		  dist = "None"
                rest = ":%s:Support"%(dist)
            else:
                rest = ""
        label = label+rest
        i += len(token)+1
        print "\t".join([str(token_id),token,label])
        continue
    if curEnd is not None and i>curEnd:
        label = "O"
    elif curEnd is not None:
        label = "I-"+curComp[-1]+rest
    i += len(token)+1 
    print "\t".join([str(token_id),token,label])
