#!/bin/bash

activeModels=()

# - - - - - - - - - -

questionFile=$1/_questions/questions_tamperednews.jsonl
answerFilePath=./output/model_answers/

# - - - - - - - - - -

prompt="\"Decide which <types> set is more consistent to the image: A=<set1> or B=<set2>. Answer only with the name of the set.\""

# - - - - - - - - - -

if [ $2 -eq 1 ]
then
    python $1/scripts/tamperednews/prepare_questions.py --base-path $1 --question-file $questionFile --prompt "$prompt" &
    PID=$!
    wait $PID
fi

# - - - - - - - - - -

modelPath=./models/instructblip-vicuna-7b/
answerFile=32_DV-tamperednews-instructBlip_base
activeModels+=(${answerFile})
if [ $3 -eq 1 ]
then
    python ./model_scripts/instructblip.py --question-file $questionFile --answer-file-path $answerFilePath --model-path $modelPath --answer-file-name $answerFile &
    PID=$!
    wait $PID
fi

modelPath=./models/instructblip-vicuna-trained-backup/
answerFile=32_DV-tamperednews-instructBlip_trained
activeModels+=(${answerFile})
if [ $3 -eq 1 ]
then
    python /nfs/home/ernstd/masterthesis_scripts/experiments/03_fine_tuning/310_train/InstructBLIP_PEFT/instructblip-lavis.py --question-file $questionFile --answer-file-path $answerFilePath --model-path $modelPath --answer-file-name $answerFile --checkpoint $4 &
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