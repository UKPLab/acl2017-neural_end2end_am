#! /bin/sh

train=~/projects/ComponentSeg/LasagneNLP/data_CAM/paragraphs/Parsing/train_full.dat.corr.abs.full.pars.lstmparser
dev=~/projects/ComponentSeg/LasagneNLP/data_CAM/paragraphs/Parsing/dev_full.dat.corr.abs.full.pars.lstmparser

embed1=sskip.100.vectors
embed2=/data/wordvecs/Glove/glove.6B.100d.txt.header
embed3=/data/wordvecs/ExtendedDependencyBasedSkip-gram/wiki_extvec_words.header
embed4=/data/wordvecs/Glove/glove.6B.50d.txt.header

../parser/lstm-parse --cnn-mem 20000 -T ${train} -d ${dev} --hidden_dim 100 --lstm_input_dim 100 -w ${embed1} --pretrained_dim 100 --rel_dim 40 --action_dim 20 -t -P 
../parser/lstm-parse --cnn-mem 20000 -T ${train} -d ${dev} --hidden_dim 100 --lstm_input_dim 100 -w ${embed2} --pretrained_dim 100 --rel_dim 40 --action_dim 20 -t -P 
../parser/lstm-parse --cnn-mem 20000 -T ${train} -d ${dev} --hidden_dim 100 --lstm_input_dim 100 -w ${embed3} --pretrained_dim 300 --rel_dim 40 --action_dim 20 -t -P 
../parser/lstm-parse --cnn-mem 20000 -T ${train} -d ${dev} --hidden_dim 100 --lstm_input_dim 100 -w ${embed4} --pretrained_dim 50 --rel_dim 40 --action_dim 20 -t -P


