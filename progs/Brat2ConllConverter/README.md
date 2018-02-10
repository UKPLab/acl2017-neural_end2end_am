# A Brat to Conll converter

This is due to Ji-Ung Lee. A similar script has been used to convert the original Student Essay corpus into CONLL (tab separated) format. (**NB** This does not work for relations. If you want to also transform the relations into CONLL format, you have to adapt the script, or else use DKpro.)

From Ji-Ung's description:

It's a python script, you can execute it with:

``python3 convert_brat_conll.py [path-to-folder-containing-annotation-folders]``

In my use case, I had subfolders with several annotation files inside folders, so I iterate over a list of subfolders and over each file inside the subfolder. 
The annotations always consisted of an `.ann` file and a `.txt` file and had the following format:

``<ID> \t <label> \t <start-offset end-offset;start-offset end-offset;...> \t text``

The script writes the text file with the annotations into a `.conll` file of the same name inside the subfolder.
Annotations are converted to IOB tags, so unannotated text is tagged with O.
The text is tokenized using the `nltk TweetTokenizer`.

Note that the script does not handle overlapping annotations, it just writes the first annotation it finds to a given text chunk. 
Depending on your use case, you may want to change that. 

I also added a python script for merging all conll files produced with the first script. It also writes token indices into the first column.
You can call it with:

``python3 merge_conll.py [path-to-folder-containing-annotation-folders] [output.file]``
