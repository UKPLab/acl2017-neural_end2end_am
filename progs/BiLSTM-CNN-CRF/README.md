This shows the sample scripts that we used to train and evaluate our AM system based on a BILSTM-CNN-CRF tagger.

To reproduce these experiments, obtain the BILSTM-CNN-CRF tagger from here:

https://github.com/XuezheMax/LasagneNLP

Also get the mentioned embeddings, adapt the scripts and run them on data of the form given in ../../data/conll/

Once the model has made its output (e.g. stored in `outputs_ACL` in the given `runACL_paragraph_sub.sh`), 
run 

``python2 extract.py < ${output}`` 

to get the predictions on the test data. 
