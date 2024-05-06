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

answerFile=221_EV_1x1-news400-mantis
activeModels+=(${answerFile})
if [ $3 -eq 1 ]
then
   python ./model_scripts/mantis/mantis.py --question-file $questionFile --answer-file-path $answerFilePath --answer-file-name $answerFile &
   PID=$!
   wait $PID
fi

answerFile=221_EV_1x1-news400-deepseek
activeModels+=(${answerFile})
if [ $3 -eq 1 ]
then
    python ./model_scripts/DeepSeek/deepseek.py --question-file $questionFile --answer-file-path $answerFilePath --answer-file-name $answerFile &
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