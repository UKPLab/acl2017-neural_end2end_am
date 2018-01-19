#! /usr/bin/python

import os
import sys

path = os.getcwd()

conll_folder = sys.argv[1]
outfile = sys.argv[2]

if not conll_folder.endswith('/'):
    conll_folder += '/'

workingpath = path + '/' + conll_folder
folders = os.listdir(workingpath)

output = open(outfile,'w')

folder_files = []

for folder in set(sorted([element for element in folders if '.conf' not in element])):
    os.chdir( workingpath + folder)
    files = os.listdir(workingpath + folder)
    index = 1
    for listing in sorted([element for element in files if '.conll' in element]):
        folder_files.append((folder,listing))
        log = open(workingpath + folder + '/' + listing,'r')
        lines = log.readlines()
        log.close()
        for line in lines:
            write_line = str(index) + '\t' + line.strip() + '\n'
            output.write(write_line)
            index += 1
    output.write('\n')
output.close()

print("Written" , len(folder_files), "files.")
