#! /usr/bin/python

import os
import sys
from nltk.tokenize import TweetTokenizer     # Simple tokenizer

tknzr = TweetTokenizer()
path = os.getcwd()
infolder = sys.argv[1]

# Add separator or not (depends on the input)
if not infolder.endswith('/'):
    infolder+='/'

workingpath = path + '/' + infolder
folders = os.listdir(workingpath)

for folder in [element for element in folders if '.conf' not in element]:  # Ignore brat config files
    os.chdir( workingpath + folder)
    files = os.listdir(workingpath + folder)
    for listing in set(files):
        # Write one merged conll file for each .ann, .txt file!
        name,extension = listing.split('.') 
        # Ignore files with the conll extension
        if   'conll' in extension:
            continue
        else:
            # Read the actual text
            textlog = open( name + '.txt','r')
            text = textlog.read()
            textlog.close()
            # Read the corresponding annotations
            annotationlog = open( name + '.ann','r')
            annotation = annotationlog.read()
            annotationlog.close()
            # If there are no annotations, just tokenize the text and write it:
            if annotation.strip() == '' :
                outlog = open(name + '.conll','w')
                for token in tknzr.tokenize(text):
                    outlog.write(token + '\tO\n')
                outlog.close()
                continue
            # Annotation format is: <element> \t <label> \t <start-offset end-offset;...> \t text
            annotations = [element.split('\t') for element in annotation.split('\n')]
            annotation_marks = [element[1] for element in annotations if len(element) > 1]
            annotation_dict = dict()
            for annot in annotation_marks:
                label = annot.split()[0]
                # Add entry to label dictionary if required:
                try:
                    annotation_dict[label]
                except (KeyError, TypeError):
                    annotation_dict[label] = []
                # For each annotation get the according text chunks:
                if ';' in annot:
                    numbers = annot.replace(label+' ','').split(';')
                    for number in numbers:
                        begin, end = number.split()
                        annotation_dict[label].append(begin)
                        annotation_dict[label].append(end)
                else:
                    begin, end = annot.replace(label+' ','').split()
                    annotation_dict[label].append(begin)
                    annotation_dict[label].append(end)
            annotations_listed = []
            for key,value in annotation_dict.items():
                for i,k in zip(value[0::2], value[1::2]):
                    annotations_listed.append((int(i),int(k),key))
            prev_end = -1
            # Create sorted list of all text offsets
            sorted_text_list = []
            for (begin,end,anot_label) in sorted(annotations_listed):
                # Add the current annotation
                if begin-1 == prev_end:
                    prev_end = end
                    sorted_text_list.append((begin,end,anot_label))
                elif begin > prev_end:
                    # Add not annotated data tagged as O
                    sorted_text_list.append((prev_end+1,begin-1,'O'))
                    # Add the current data 
                    sorted_text_list.append((begin,end,anot_label))
                    prev_end = end
            # Add last text chunk, if there are O annotations at the end:
            if prev_end < len(text):
                sorted_text_list.append((prev_end,len(text)-1,'O'))
            text_label_list = []
            # Get the annotation text for each chunk and tokenize it
            for (begin,end,anot_label) in sorted_text_list:
                anot_text = text[begin:end]
                text_label_list.append((anot_label,tknzr.tokenize(anot_text)))
            # Write the tokenized text in conll file:
            outlog = open(name + '.conll','w')
            for (anot_label,text_splits) in text_label_list:
                if [] == text_splits:
                    continue
                # Use BIO scheme for all annotations
                if 'O' not in anot_label:
                    outstring =  text_splits[0] + '\t' + 'B-'+anot_label + '\n'
                    outlog.write(outstring)
                    for element in text_splits[1:]:
                        outstring = element + '\t' + 'I-'+anot_label + '\n'
                        outlog.write(outstring)
                else:
                    for element in text_splits:
                        outstring =  element + '\t' + 'O' + '\n'
                        outlog.write(outstring)
            outlog.close()
