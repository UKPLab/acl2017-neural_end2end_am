#! /bin/sh

data=data_CAM/joint_allfull_new/ComponentsTypesRelations/
data=data_CAM/paragraphs/
nunits=200

for i in 0 1 2 3 4; do 
  embeddings=/data/wordvecs/Glove/glove.6B.100d.txt.gz 
  ./run_bi-lstm-cnn-crf3.sh ${data}/sub/train+dev_full.dat${i}.train ${data}/sub/train+dev_full.dat${i}.dev ${data}/test_full.dat ${embeddings} MODELS/sub_paragraph${i}.mod 150 > outputs_ACL/PARA/paragraph${i}.dat
done &

for i in 5 6 7 8 9; do
  embeddings=/data/wordvecs/Glove/glove.6B.50d.txt.gz
  ./run_bi-lstm-cnn-crf3.sh ${data}/sub/train+dev_full.dat${i}.train ${data}/sub/train+dev_full.dat${i}.dev ${data}/test_full.dat ${embeddings} MODELS/sub_paragraph${i}.mod 200 > outputs_ACL/PARA/paragraph${i}.dat
done &


for i in 10 11 12 13 14; do
  embeddings=/data/wordvecs/Glove/glove.6B.200d.txt.gz
  ./run_bi-lstm-cnn-crf3.sh ${data}/sub/train+dev_full.dat${i}.train ${data}/sub/train+dev_full.dat${i}.dev ${data}/test_full.dat ${embeddings} MODELS/sub_paragraph${i}.mod 250 > outputs_ACL/PARA/paragraph${i}.dat
done &

for i in 15 16 17 18 19; do
  embeddings=/data/wordvecs/Glove/glove.6B.50d.txt.gz
  ./run_bi-lstm-cnn-crf3.sh ${data}/sub/train+dev_full.dat${i}.train ${data}/sub/train+dev_full.dat${i}.dev ${data}/test_full.dat ${embeddings} MODELS/sub_paragraph${i}.mod 125 > outputs_ACL/PARA/paragraph${i}.dat
done &

