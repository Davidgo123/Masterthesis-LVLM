#!/bin/bash

iterations=1
modus=("multiLabel", "pairLabel", "pairEntity", "singleEntity")
activeModels=()

# - - - - - - - - - -

questionFile=/nfs/home/ernstd/data/news400/document_verification/questions.jsonl
answerFilePath=/nfs/home/ernstd/data/news400/document_verification/

# - - - - - - - - - -

python /nfs/home/ernstd/masterthesis_scripts/document_verification/prepare_questions.py --question-file $questionFile &
pid1=$!
wait $pid1

# - - - - - - - - - -

for ((VAR=0;VAR<$iterations;VAR=VAR+1));
do
    #answerFile=instructBlip_answers
    #activeModels+=(${answerFile})
    #python /nfs/home/ernstd/masterthesis_scripts/document_verification/model_scripts/instructblip_dv.py --iteration $VAR --question-file $questionFile --answer-file-path $answerFilePath --answer-file-name $answerFile &
    #pid2=$!
    #wait $pid2

    answerFile=blip_2_answers
    activeModels+=(${answerFile})
    python /nfs/home/ernstd/masterthesis_scripts/document_verification/model_scripts/blip2_dv.py --iteration $VAR --question-file $questionFile --answer-file-path $answerFilePath --answer-file-name $answerFile &
    pid3=$!
    wait $pid3

    #modelPath=/nfs/home/ernstd/models/llava-1.5-7b-hf/
    #answerFile=llava_1_5_7b_answers
    #activeModels+=(${answerFile})
    #python /nfs/home/ernstd/masterthesis_scripts/document_verification/model_scripts/llava_dv.py --iteration $VAR --question-file $questionFile --answer-file-path $answerFilePath --model-path $modelPath --answer-file-name $answerFile &
    #pid4=$!
    #wait $pid4

    #modelPath=/nfs/home/ernstd/models/llava-1.5-13b-hf/
    #answerFile=llava_1_5_13b_answers
    #activeModels+=(${answerFile})
    #python /nfs/home/ernstd/masterthesis_scripts/document_verification/model_scripts/llava-4bit_dv.py --iteration $VAR --question-file $questionFile --answer-file-path $answerFilePath --model-path $modelPath --answer-file-name $answerFile &
    #pid5=$!
    #wait $pid5

    #modelPath=/nfs/home/ernstd/models/llava-v1.6-vicuna-13b/
    #answerFile=llava_1_6_13b_vicuna_answers
    #activeModels+=(${answerFile})
    #python /nfs/home/ernstd/masterthesis_scripts/document_verification/model_scripts/llava_dv.py --iteration $VAR --question-file $questionFile --answer-file-path $answerFilePath --model-path $modelPath --answer-file-name $answerFile &
    #pid6=$!
    #wait $pid6
done

# - - - - - - - - - -

python /nfs/home/ernstd/masterthesis_scripts/document_verification/analyze_answers.py --iterations $iterations --models ${activeModels[@]} &
pid8=$!
wait $pid8