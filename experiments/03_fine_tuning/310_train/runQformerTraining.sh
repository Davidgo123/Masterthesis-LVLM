#!/bin/bash

modelPath=/nfs/home/ernstd/masterthesis_scripts/models/instructblip-flan-t5-xl/

#  01  #
epochs=20
sampleSize=250
outputModelPath=/nfs/home/ernstd/masterthesis_scripts/models/instructblip-flan-trained
python /nfs/home/ernstd/masterthesis_scripts/experiments/03_fine_tuning/310_train/train.py --model-path $modelPath --model-path-tuned $outputModelPath --sample-size $sampleSize --epochs $epochs &
PID=$!
wait $PID


#python /nfs/home/ernstd/masterthesis_scripts/experiments/03_fine_tuning/310_train/train.py  --model-path '/nfs/home/ernstd/masterthesis_scripts/models/instructblip-flan-t5-xl/' --model-path-tuned '/nfs/home/ernstd/masterthesis_scripts/models/instructblip-flan-trained' --sample-size 3 --epochs 10
