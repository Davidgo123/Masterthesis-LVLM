#!/bin/bash

activeModels=()

# - - - - - - - - - -

questionFile=$1/_questions/questions_news400.jsonl
answerFilePath=./output/model_answers/

# - - - - - - - - - -

if [ $2 -eq 1 ]
then
    python $1/scripts/news400/prepare_questions.py --base-path $1 --question-file $questionFile &
    PID=$!
    wait $PID
fi

# - - - - - - - - - -

modelPath=./models/instructblip-flan-t5-xl/
answerFile=311_DV-news400-instructBlip_base
activeModels+=(${answerFile})
if [ $3 -eq 1 ]
then
    python ./model_scripts/instructblip.py --question-file $questionFile --answer-file-path $answerFilePath --model-path $modelPath --answer-file-name $answerFile &
    PID=$!
    wait $PID
fi

modelPath=./models/instructblip-flan-trained-qformer-250-10/
answerFile=311_DV-news400-instructBlip_qformer
activeModels+=(${answerFile})
if [ $3 -eq 1 ]
then
    python ./model_scripts/instructblip.py --question-file $questionFile --answer-file-path $answerFilePath --model-path $modelPath --answer-file-name $answerFile &
    PID=$!
    wait $PID
fi

# - - - - - - - - - -

python $1/scripts/news400/analyze_answers.py --models ${activeModels[@]} &
PID=$!
wait $PID

python $1/scripts/news400/printResultTable.py --models ${activeModels[@]} &
PID=$!
wait $PID