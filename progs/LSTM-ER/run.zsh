#!/bin/zsh
## Adapted from: https://github.com/tticoin/LSTM-ER/blob/master/data/ace2005/run.zsh
# split & parse
mkdir text
java -cp ".:../common/stanford-corenlp-full-2015-04-20/*" edu.stanford.nlp.pipeline.StanfordCoreNLP -props ../common/props_ssplit -outputFormat conll -filelist file_list -outputDirectory text/
# conll to text
for i in text/*.conll
do
    echo $i && python3 ../common/conll2txt.py $i >! text/`basename $i .txt.conll`.split.txt
done
# adjust offsets
for i in text/*.split.txt
do
    echo $i && python3 ../common/standoff.py result/`basename $i .split.txt`.txt result/`basename $i .split.txt`.ann $i >! text/`basename $i .split.txt`.split.ann
done
# fix sentence split errors
mkdir fixed
for i in text/*.split.txt
do
    echo $i && python3 ../common/fix_sentence_break.py $i text/`basename $i .split.txt`.split.ann fixed/`basename $i .split.txt`.txt
done
# parse ssplit-fixed text
java -cp ".:../common/stanford-corenlp-full-2015-04-20/*" edu.stanford.nlp.pipeline.StanfordCoreNLP -props ../common/props_fixed -outputFormat conll -filelist file_list_fixed -outputDirectory fixed/
for i in fixed/*.conll
do
    python3 ../common/conll2txt.py $i >! fixed/`basename $i .txt.conll`.split.txt
done
# collect data
mkdir corpus
cd corpus
#ln -s ../result/*.txt .
#ln -s ../result/*.ann .
#ln -s ../fixed/*.split.txt .
# MODIFIED SE
cp ../result/*.txt .
cp ../result/*.ann .
cp ../fixed/*.split.txt .

cd ..
# adjust offsets
for i in corpus/*.split.txt
do
    echo $i && python3 ../common/standoff.py corpus/`basename $i .split.txt`.txt corpus/`basename $i .split.txt`.ann $i >! corpus/`basename $i .split.txt`.split.ann
done
# conll to so
for i in fixed/*.split.txt
do
    echo $i && perl ../common/dep2so.prl fixed/`basename $i .split.txt`.txt.conll $i >! corpus/`basename $i .txt`.stanford.so
done
for i in corpus/*.split.txt
do
    python3 ../common/sanity_check.py $i corpus/`basename $i .split.txt`.split.stanford.so
done
