# -*- coding: utf-8 -*-
import sys, re, csv, os, shutil, codecs

if len(sys.argv) < 3:
    sys.stderr.write("Usage: python %s txt parse" % sys.argv[0])
    sys.exit(0)

start = 0
end = 0
txt_cont = ""
with codecs.open(sys.argv[1], 'r', "utf-8") as txt:
    txt_cont = txt.read()

with codecs.open(sys.argv[2], 'r', "utf-8") as tsv:
    for line_list in csv.reader(tsv, delimiter="\t", quoting = csv.QUOTE_NONE): 
        if(len(line_list) > 0):
            start = int(line_list[0])
            end = int(line_list[1])
            assert len(txt_cont) >= start + (end-start), "file %r: start/end index %r/%r cause problem" % (sys.argv[1], start, end)