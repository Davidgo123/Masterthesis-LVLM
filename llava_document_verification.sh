#!/bin/bash

python /nfs/home/ernstd/masterthesis_scripts/document_verification/prepare_questions.py &
pid1=$!
wait $pid1

# - - - - - - - - - -

python /nfs/home/ernstd/masterthesis_scripts/document_verification/model_scripts/instructblip_dv.py &
pid2=$!
wait $pid2

python /nfs/home/ernstd/masterthesis_scripts/document_verification/model_scripts/llava-7b_dv.py &
pid3=$!
wait $pid3

python /nfs/home/ernstd/masterthesis_scripts/document_verification/model_scripts/llava-13b_dv.py &
pid4=$!
wait $pid4

# - - - - - - - - - -

python /nfs/home/ernstd/masterthesis_scripts/document_verification/analyze_answers.py &
pid5=$!
wait $pid5