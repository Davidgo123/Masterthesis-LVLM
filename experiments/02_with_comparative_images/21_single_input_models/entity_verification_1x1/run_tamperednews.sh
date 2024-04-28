#!/bin/bash

activeModels=()

# - - - - - - - - - -

questionFile=$1/_questions/questions_tamperednews.jsonl
answerFilePath=./output/model_answers/

# - - - - - - - - - -

if [ $2 -eq 1 ]
then
    python $1/scripts/tamperednews/prepare_questions.py --base-path $1 --question-file $questionFile &
    PID=$!
    wait $PID
fi

# - - - - - - - - - -

answerFile=02_21_EV_1x1-tamperednews-blip2
activeModels+=(${answerFile})
if [ $3 -eq 1 ]
then
    python ./model_scripts/blip2.py --question-file $questionFile --answer-file-path $answerFilePath --answer-file-name $answerFile &
    PID=$!
    wait $PID
fi

answerFile=02_21_EV_1x1-tamperednews-instructBlip
activeModels+=(${answerFile})
if [ $3 -eq 1 ]
then
    python ./model_scripts/instructblip.py --question-file $questionFile --answer-file-path $answerFilePath --answer-file-name $answerFile &
    PID=$!
    wait $PID
fi

modelPath=./models/llava-1.5-7b-hf/
answerFile=02_21_EV_1x1-tamperednews-llava_15_7b
activeModels+=(${answerFile})
if [ $3 -eq 1 ]
then
    python ./model_scripts/llava.py --question-file $questionFile --answer-file-path $answerFilePath --model-path $modelPath --answer-file-name $answerFile &
    PID=$!
    wait $PID
fi

modelPath=./models/llava-1.5-13b-hf/
answerFile=02_21_EV_1x1-tamperednews-llava_15_13b
activeModels+=(${answerFile})
if [ $3 -eq 1 ]
then
    python ./model_scripts/llava-4bit.py --question-file $questionFile --answer-file-path $answerFilePath --model-path $modelPath --answer-file-name $answerFile &
    PID=$!
    wait $PID
fi

modelPath=./models/llava-v1.6-mistral-7b-hf/
answerFile=02_21_EV_1x1-tamperednews-llava_16_7b
activeModels+=(${answerFile})
if [ $3 -eq 1 ]
then
    python ./model_scripts/llava.py --question-file $questionFile --answer-file-path $answerFilePath --model-path $modelPath --answer-file-name $answerFile &
    PID=$!
    wait $PID
fi

# - - - - - - - - - -

python $1/scripts/tamperednews/analyze_answers.py --models ${activeModels[@]} &
PID=$!
wait $PID

python $1/scripts/tamperednews/printResultTable.py --models ${activeModels[@]} &
PID=$!
wait $PID