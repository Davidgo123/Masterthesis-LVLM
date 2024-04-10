#!/bin/bash

activeModels=()

# - - - - - - - - - -

questionFile=/nfs/home/ernstd/masterthesis_scripts/2_image_entity_verification/_questions/questions_tamperedNews.jsonl
answerFilePath=/nfs/home/ernstd/masterthesis_scripts/2_image_entity_verification/model_answers/tamperedNews/

# - - - - - - - - - -

if [ $1 -eq 1 ]
then
    python /nfs/home/ernstd/masterthesis_scripts/2_image_entity_verification/scripts/tamperedNews/prepare_questions.py --question-file $questionFile &
    PID=$!
    wait $PID
fi

# - - - - - - - - - -

answerFile=blip_2_answers
activeModels+=(${answerFile})
if [ $2 -eq 1 ]
then
    python /nfs/home/ernstd/masterthesis_scripts/model_scripts/blip2_dv.py --question-file $questionFile --answer-file-path $answerFilePath --answer-file-name $answerFile &
    PID=$!
    wait $PID
fi

answerFile=instructBlip_answers
activeModels+=(${answerFile})
if [ $2 -eq 1 ]
then
    python /nfs/home/ernstd/masterthesis_scripts/model_scripts/instructblip_dv.py --question-file $questionFile --answer-file-path $answerFilePath --answer-file-name $answerFile &
    PID=$!
    wait $PID
fi

modelPath=/nfs/home/ernstd/models/llava-1.5-7b-hf/
answerFile=llava_1_5_7b_answers
activeModels+=(${answerFile})
if [ $2 -eq 1 ]
then
    python /nfs/home/ernstd/masterthesis_scripts/model_scripts/llava_dv.py --question-file $questionFile --answer-file-path $answerFilePath --model-path $modelPath --answer-file-name $answerFile &
    PID=$!
    wait $PID
fi

modelPath=/nfs/home/ernstd/models/llava-1.5-13b-hf/
answerFile=llava_1_5_13b_answers
activeModels+=(${answerFile})
if [ $2 -eq 1 ]
then
    python /nfs/home/ernstd/masterthesis_scripts/model_scripts/llava-4bit_dv.py --question-file $questionFile --answer-file-path $answerFilePath --model-path $modelPath --answer-file-name $answerFile &
    PID=$!
    wait $PID
fi

modelPath=/nfs/home/ernstd/models/llava-v1.6-mistral-7b-hf/
answerFile=llava_1_6_7b_answers
activeModels+=(${answerFile})
if [ $2 -eq 1 ]
then
    python /nfs/home/ernstd/masterthesis_scripts/model_scripts/llava_dv.py --question-file $questionFile --answer-file-path $answerFilePath --model-path $modelPath --answer-file-name $answerFile &
    PID=$!
    wait $PID
fi

# - - - - - - - - - -

python /nfs/home/ernstd/masterthesis_scripts/2_image_entity_verification/scripts/tamperedNews/analyze_answers.py --models ${activeModels[@]} &
PID=$!
wait $PID

python /nfs/home/ernstd/masterthesis_scripts/2_image_entity_verification/scripts/tamperedNews/printResultTable.py --models ${activeModels[@]} &
PID=$!
wait $PID