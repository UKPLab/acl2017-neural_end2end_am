# Running experiments with LSTM-ER

Steps to reproduce:

1. clone https://github.com/tticoin/LSTM-ER and run preparation steps from https://github.com/tticoin/LSTM-ER/tree/master/data (download Stanford Core NLP & POS tagger)

2. convert ```.dat.abs``` data (replace ```dev``` by ```train```/```test```, and ```Essay_Level```by ```Paragraph_Level```)

```
cd progs/LSTM-ER
python3 conversion.py ../../data/conll/Essay_Level/dev.dat.abs
mkdir dev;mv file_list* dev/;mv result/ dev/;cp run.zsh dev/
cd dev
zsh run.zsh
```

The files you need to run LSTM-ER are contained in the ```corpus``` folder of the respective dev/test/train directories.

3. to train/test, follow instructions at https://github.com/tticoin/LSTM-ER

```
build/relation/RelationExtraction --train -y yaml/parameter-stab2016.yaml
build/relation/RelationExtraction --test -y yaml/parameter-stab2016.yaml
```

Note: code is tested only under Fedora 25.
Most scripts in the ```common``` folder are derived from https://github.com/tticoin/LSTM-ER/tree/master/data/common.


## YAML file for LSTM-ER

The yaml file holding the configuration we used for the experiments is included in `params-acl2017.yaml`
