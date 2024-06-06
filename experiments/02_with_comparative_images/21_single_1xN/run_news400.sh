#!/bin/bash

answerFilePath=./output/model_answers/

# - - - - - - - - - -

prompts=(
    "\"Does the red part of the image show the same <type> as the blue part of the image?\""
    "\"Does the two images show the same <type>?\""
    "\"Is the <type> in the two pictures consistent?\""
)
counter=0

# - - - - - - - - - -

for prompt in "${prompts[@]}"; do
    activeModels=()

    questionFile=$1/_questions/questions_news400-$counter.jsonl
    if [ $2 -eq 1 ]
    then
        python $1/scripts/news400/prepare_questions.py --base-path $1 --question-file $questionFile --prompt "$prompt" &
        PID=$!
        wait $PID
    fi


    answerFile=21_EV_1xN-news400-blip2$counter
    activeModels+=(${answerFile})
    if [ $3 -eq 1 ]
    then
        python ./model_scripts/blip2.py --question-file $questionFile --answer-file-path $answerFilePath --answer-file-name $answerFile &
        PID=$!
        wait $PID
    fi

    answerFile=21_EV_1xN-news400-instructBlip$counter
    activeModels+=(${answerFile})
    if [ $3 -eq 1 ]
    then
        python ./model_scripts/instructblip.py --question-file $questionFile --answer-file-path $answerFilePath --answer-file-name $answerFile &
        PID=$!
        wait $PID
    fi

    modelPath=./models/llava-1.5-7b-hf/
    answerFile=21_EV_1xN-news400-llava_15_7b$counter
    activeModels+=(${answerFile})
    if [ $3 -eq 1 ]
    then
        python ./model_scripts/llava.py --question-file $questionFile --answer-file-path $answerFilePath --model-path $modelPath --answer-file-name $answerFile &
        PID=$!
        wait $PID
    fi

    modelPath=./models/llava-1.5-13b-hf/
    answerFile=21_EV_1xN-news400-llava_15_13b$counter
    activeModels+=(${answerFile})
    if [ $3 -eq 1 ]
    then
        python ./model_scripts/llava-4bit.py --question-file $questionFile --answer-file-path $answerFilePath --model-path $modelPath --answer-file-name $answerFile &
        PID=$!
        wait $PID
    fi

    modelPath=./models/llava-v1.6-mistral-7b-hf/
    answerFile=21_EV_1xN-news400-llava_16_7b$counter
    activeModels+=(${answerFile})
    if [ $3 -eq 1 ]
    then
        python ./model_scripts/llava-1.6.py --question-file $questionFile --answer-file-path $answerFilePath --model-path $modelPath --answer-file-name $answerFile &
        PID=$!
        wait $PID
    fi

    python $1/scripts/news400/analyze_answers.py --models ${activeModels[@]} &
    PID=$!
    wait $PID

    python $1/scripts/news400/printResultTable.py --models ${activeModels[@]} &
    PID=$!
    wait $PID

    let counter++
done


