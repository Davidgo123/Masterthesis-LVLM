#!/bin/bash

iterations=1
modus=("multiLabel", "pairLabel", "pairEntity", "singleEntity")
activeModels=()

# - - - - - - - - - -

questionFile=/nfs/home/ernstd/masterthesis_scripts/document_verification/data/questions.jsonl
answerFilePath=/nfs/home/ernstd/masterthesis_scripts/document_verification/model_answers/

# - - - - - - - - - -

#python /nfs/home/ernstd/masterthesis_scripts/document_verification/scripts/prepare_questions_news400.py --question-file $questionFile &
#pid1=$!
#wait $pid1

#python /nfs/home/ernstd/masterthesis_scripts/document_verification/scripts/prepare_questions_mmg.py --question-file $questionFile &
#pid2=$!
#wait $pid2

# - - - - - - - - - -

for ((VAR=0;VAR<$iterations;VAR=VAR+1));
do
    answerFile=instructBlip_answers
    activeModels+=(${answerFile})
    #python /nfs/home/ernstd/masterthesis_scripts/document_verification/model_scripts/instructblip_dv.py --iteration $VAR --question-file $questionFile --answer-file-path $answerFilePath --answer-file-name $answerFile &
    #pid3=$!
    #wait $pid3

    answerFile=blip_2_answers
    activeModels+=(${answerFile})
    #python /nfs/home/ernstd/masterthesis_scripts/document_verification/model_scripts/blip2_dv.py --iteration $VAR --question-file $questionFile --answer-file-path $answerFilePath --answer-file-name $answerFile &
    #pid4=$!
    #wait $pid4

    modelPath=/nfs/home/ernstd/models/llava-1.5-7b-hf/
    answerFile=llava_1_5_7b_answers
    activeModels+=(${answerFile})
    #python /nfs/home/ernstd/masterthesis_scripts/document_verification/model_scripts/llava_dv.py --iteration $VAR --question-file $questionFile --answer-file-path $answerFilePath --model-path $modelPath --answer-file-name $answerFile &
    #pid5=$!
    #wait $pid5

    modelPath=/nfs/home/ernstd/models/llava-1.5-13b-hf/
    answerFile=llava_1_5_13b_answers
    activeModels+=(${answerFile})
    #python /nfs/home/ernstd/masterthesis_scripts/document_verification/model_scripts/llava-4bit_dv.py --iteration $VAR --question-file $questionFile --answer-file-path $answerFilePath --model-path $modelPath --answer-file-name $answerFile &
    #pid6=$!
    #wait $pid6
done

# - - - - - - - - - -

python /nfs/home/ernstd/masterthesis_scripts/document_verification/scripts/analyze_answers.py --iterations $iterations --models ${activeModels[@]} &
pid7=$!
wait $pid7

python /nfs/home/ernstd/masterthesis_scripts/document_verification/scripts/printResultTable.py &
pid8=$!
wait $pid8