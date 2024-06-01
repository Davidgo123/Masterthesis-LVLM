#!/bin/bash

activeModels=()
answerFilePath=./output/model_answers/

# - - - - - - - - - -

counter=0
prompts=(
    "\"Is any <type> from the image consistent with <name>?\""
    "\"Is <type> <name> visible in the image?\""
    "\"Is <type> <name> visible in the image? Answer only with yes or no.\""
)

for prompt in "${prompts[@]}"; do
    questionFile=$1/_questions/questions_mmg-$counter.jsonl
    if [ $2 -eq 1 ]
    then
        python $1/scripts/mmg/prepare_questions.py --base-path $1 --question-file $questionFile --prompt "$prompt" &
        PID=$!
        wait $PID
    fi
    let counter++
done

# - - - - - - - - - -

answerFile=12_EV-mmg-blip2
activeModels+=(${answerFile})
questionFile=$1/_questions/questions_mmg-0.jsonl
if [ $3 -eq 1 ]
then
    python ./model_scripts/blip2.py --question-file $questionFile --answer-file-path $answerFilePath --answer-file-name $answerFile &
    PID=$!
    wait $PID
fi

answerFile=12_EV-mmg-instructBlip
questionFile=$1/_questions/questions_mmg-1.jsonl
activeModels+=(${answerFile})
if [ $3 -eq 1 ]
then
    python ./model_scripts/instructblip.py --question-file $questionFile --answer-file-path $answerFilePath --answer-file-name $answerFile &
    PID=$!
    wait $PID
fi

modelPath=./models/llava-1.5-7b-hf/
answerFile=12_EV-mmg-llava_15_7b
questionFile=$1/_questions/questions_mmg-2.jsonl
activeModels+=(${answerFile})
if [ $3 -eq 1 ]
then
    python ./model_scripts/llava.py --question-file $questionFile --answer-file-path $answerFilePath --model-path $modelPath --answer-file-name $answerFile &
    PID=$!
    wait $PID
fi

modelPath=./models/llava-1.5-13b-hf/
answerFile=12_EV-mmg-llava_15_13b
questionFile=$1/_questions/questions_mmg-2.jsonl
activeModels+=(${answerFile})
if [ $3 -eq 1 ]
then
    python ./model_scripts/llava-4bit.py --question-file $questionFile --answer-file-path $answerFilePath --model-path $modelPath --answer-file-name $answerFile &
    PID=$!
    wait $PID
fi

modelPath=./models/llava-v1.6-mistral-7b-hf/
answerFile=12_EV-mmg-llava_16_7b
questionFile=$1/_questions/questions_mmg-2.jsonl
activeModels+=(${answerFile})
if [ $3 -eq 1 ]
then
    python ./model_scripts/llava-1.6.py --question-file $questionFile --answer-file-path $answerFilePath --model-path $modelPath --answer-file-name $answerFile &
    PID=$!
    wait $PID
fi

# - - - - - - - - - -

python $1/scripts/mmg/analyze_answers.py --models ${activeModels[@]} &
PID=$!
wait $PID

python $1/scripts/mmg/printResultTable.py --models ${activeModels[@]} &
PID=$!
wait $PID