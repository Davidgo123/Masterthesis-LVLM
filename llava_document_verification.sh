#!/bin/bash

python /nfs/home/ernstd/scripts/document_verification/1_prepare_questions.py &
pid1=$!
wait $pid1

# - - - - - - - - - -

python /nfs/home/ernstd/models/instructblip-vicuna-7b/document_verification.py &
pid2=$!
wait $pid2

python /nfs/home/ernstd/models/llava-1.5-7b-hf/document_verification.py &
pid3=$!
wait $pid3

python /nfs/home/ernstd/models/llava-1.5-13b-hf/document_verification.py &
pid4=$!
wait $pid4

# - - - - - - - - - -

#python /nfs/home/ernstd/scripts/document_verification/2_analyze_answers.py &
#pid5=$!
#wait $pid5