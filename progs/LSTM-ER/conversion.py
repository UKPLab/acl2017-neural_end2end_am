# -*- coding: utf-8 -*-
import sys, re, csv, os, shutil, codecs#

# (quick-and-dirty) converts conll-like input files into .ann and .txt files, writes output into folders called "result" and "fixed"

if len(sys.argv) < 2:
    sys.stderr.write("Usage: python %s input_file" % sys.argv[0])
    sys.exit(0)
    
replace_char_dir = {"‘":"'","’":"'","“":"\"","”":"\"","–":"-","—":"-","…":"...","é":"e"}    
    
# init string vars
txt_doc = ann_doc = line = suffix = current_tokens = file_list = file_list_fixed = current_relation = ""

# init counters
doc_nr = comp_nr = tok_nr = begin = 0

# init lists 
component_head_dir = {}
relation_dir = {}

# delete result folder if present
if os.path.exists("result"):
    shutil.rmtree("result")
os.mkdir("result") 

# files with substring "dev", "test" and "train" will be labeled as such
if("dev" in os.path.basename(sys.argv[1])):
    suffix = "dev"
if("train" in os.path.basename(sys.argv[1])):
    suffix = "train"
if("test" in os.path.basename(sys.argv[1])):
    suffix = "test"    

# these files holding filenames are expected by subsequent scripts
out_filelist = codecs.open("file_list", 'w', "utf-8")
out_filelist_fixed = codecs.open("file_list_fixed", 'w', "utf-8")

# replace chars which could become a problem later on
lines = []
with open(sys.argv[1]) as infile:
    for aline in infile:
        for src, target in replace_char_dir.items():
            aline = aline.replace(src, target)
        lines.append(aline)
with open(sys.argv[1]+".tmp", 'w') as outfile:
    for aline in lines:
        outfile.write(aline)

with codecs.open(sys.argv[1]+".tmp", 'r', "utf-8") as tsv:
    for line_list in csv.reader(tsv, delimiter="\t", quoting = csv.QUOTE_NONE): 
        tok_nr += 1
        if(len(line_list) == 0 and len(txt_doc) > 1): # empty line & non-empty text buffer => create new document
            out_txt = codecs.open("result/"+ suffix + "_" + str(doc_nr) + ".txt", 'w', "utf-8")
            out_ann = codecs.open("result/"+ suffix + "_" + str(doc_nr) + ".ann", 'w', "utf-8")
            file_list += "result/"+ suffix + "_" + str(doc_nr)+ ".txt" + "\n"
            file_list_fixed += "fixed/"+ suffix + "_" + str(doc_nr)+ ".txt" + "\n"
            out_txt.write(txt_doc)
            if(len(line) > 0):
                ann_doc += line + str(begin + len(current_tokens)) + "\t" + current_tokens + "\n"
            # transform and append relations
            idx = 0
            for k, v in relation_dir.items():
                if(v.split("_")[0] in component_head_dir):
                    # idx_of_relation \t relation_type \w Arg1:name_of_comp \w Arg2:name_of_comp
                    ann_doc += "R" + suffix + "_" + str(doc_nr) + "-R" + str(idx) + "-1" + "\t" + v.split("_")[1] + " Arg1:" + k + " Arg2:" + str(component_head_dir[v.split("_")[0]]) + "\n"  
                idx += 1
            out_ann.write(ann_doc)
            out_txt.close()
            out_ann.close()
            # reset
            txt_doc = ann_doc = line = current_tokens = ""
            comp_nr = tok_nr = 0
            component_head_dir = {}
            relation_dir = {}
            doc_nr += 1
            continue
        token = line_list[1]
        txt_doc += token+" "
        tag = line_list[2] 
        if(tag != "O"): # not O --> need to process
            iob = tag.split("-")[0]
            if(iob == "B"): # new segment
                current_relation = ""
                head = ""
                if(len(tag.split(":")) == 3): # Prem relation exists --> need to process
                    current_relation = tag.split(":")[2]
                    head = str(tag.split(":")[1])
                if(len(tag.split(":")) == 2): # Claim relation exists --> need to process
                    current_relation = tag.split(":")[1]
                    head = "MJ"
                if(len(current_tokens) > 0): # write last line
                    line += str(begin+len(current_tokens)) + "\t" + current_tokens 
                    ann_doc += line+"\n"
                begin = len(txt_doc)-len(token+" ")
                component_type = tag.split("-")[1].split(":")[0]
                # Tname_of_file-X-Y \t component_type \w begin \w
                comp_name = "T" + suffix + "_" + str(doc_nr) + "-E" + str(comp_nr) + "-" + str(tok_nr)
                line = comp_name + "\t" + component_type + " " + str(begin) + " "
                if(component_type == "MajorClaim"):
                    component_head_dir["MJ"] = comp_name
                else:
                    component_head_dir[line_list[0]] = comp_name
                if(len(current_relation) > 0):
                    relation_dir[comp_name] = head + "_" + current_relation
                    current_relation = ""
                current_tokens = token
                comp_nr += 1
            if(iob == "I"):
                current_tokens += " "+token
# write files and finish                
out_filelist.write(file_list)
out_filelist_fixed.write(file_list_fixed)
out_filelist.close()
out_filelist_fixed.close()                
print("Done. Processed %s documents." % doc_nr)