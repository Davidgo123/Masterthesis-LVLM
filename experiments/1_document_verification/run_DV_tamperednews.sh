#!/bin/bash

activeModels=()

# - - - - - - - - - -

questionFile=./experiments/1_document_verification/_questions/questions_tamperednews.jsonl
answerFilePath=./output/model_answers/

# - - - - - - - - - -

if [ $1 -eq 1 ]
then
    python ./experiments/1_document_verification/scripts/tamperednews/prepare_questions.py --question-file $questionFile &
    PID=$!
    wait $PID
fi

# - - - - - - - - - -

answerFile=DV-tamperednews-blip_2_answers
activeModels+=(${answerFile})
if [ $2 -eq 1 ]
then
    python ./model_scripts/blip2.py --question-file $questionFile --answer-file-path $answerFilePath --answer-file-name $answerFile &
    PID=$!
    wait $PID
fi

answerFile=DV-tamperednews-instructBlip_answers
activeModels+=(${answerFile})
if [ $2 -eq 1 ]
then
    python ./model_scripts/instructblip.py --question-file $questionFile --answer-file-path $answerFilePath --answer-file-name $answerFile &
    PID=$!
    wait $PID
fi

modelPath=./models/llava-1.5-7b-hf/
answerFile=DV-tamperednews-llava_1_5_7b_answers
activeModels+=(${answerFile})
if [ $2 -eq 1 ]
then
    python ./model_scripts/llava.py --question-file $questionFile --answer-file-path $answerFilePath --model-path $modelPath --answer-file-name $answerFile &
    PID=$!
    wait $PID
fi

modelPath=./models/llava-1.5-13b-hf/
answerFile=DV-tamperednews-llava_1_5_13b_answers
activeModels+=(${answerFile})
if [ $2 -eq 1 ]
then
    python ./model_scripts/llava-4bit.py --question-file $questionFile --answer-file-path $answerFilePath --model-path $modelPath --answer-file-name $answerFile &
    PID=$!
    wait $PID
fi

modelPath=./models/llava-v1.6-mistral-7b-hf/
answerFile=DV-tamperednews-llava_1_6_7b_answers
activeModels+=(${answerFile})
if [ $2 -eq 1 ]
then
    python ./model_scripts/llava.py --question-file $questionFile --answer-file-path $answerFilePath --model-path $modelPath --answer-file-name $answerFile &
    PID=$!
    wait $PID
fi

# - - - - - - - - - -

python ./experiments/1_document_verification/scripts/tamperednews/analyze_answers.py --models ${activeModels[@]} &
PID=$!
wait $PID

python ./experiments/1_document_verification/scripts/tamperednews/printResultTable.py --models ${activeModels[@]} &
PID=$!
wait $PID