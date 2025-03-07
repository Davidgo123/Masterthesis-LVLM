#!/bin/bash

answerFilePath=./output/model_answers/

# - - - - - - - - - -

prompts=(
    "\"Is any <type> from the image consistent with <name>?\""
    "\"Is <type> <name> visible in the image?\""
    "\"Is <type> <name> shown in the image? Answer only with yes or no.\""
    "\"Decide which <type> is more consistent to the image: A='<name1>' or B='<name2>'. Answer only with the name of the set.\""
    "\"Decide which <type> is more consistent to the image: A='<name1>' or B='<name2>'. Answer only with the name of the set.\""
    "\"Decide which <type> is more consistent to the image: A='<name1>' or B='<name2>'. Answer only with the name of the set.\""
    "\"Decide which <types> set is more consistent to the image: A=<set1> or B=<set2>. Answer only with the name of the set.\""
    "\"Decide which <types> set is more consistent to the image: A=<set1> or B=<set2>. Answer only with the name of the set.\""
    "\"Decide which <types> set is more consistent to the image: A=<set1> or B=<set2>. Answer only with the name of the set.\""
)

# - - - - - - - - - -

counter=0
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

for (( counter=0; counter<9; counter+=3 ))
do
    activeModels=()
    newCounter=$((counter + 0))
    questionFile="$1/_questions/questions_mmg-$newCounter.jsonl"
    answerFile=11_DV-mmg-blip2$counter
    activeModels+=(${answerFile})
    if [ $3 -eq 1 ]
    then
        python ./model_scripts/blip2.py --question-file $questionFile --answer-file-path $answerFilePath --answer-file-name $answerFile &
        PID=$!
        wait $PID
    fi

    newCounter=$((counter + 1))
    questionFile="$1/_questions/questions_mmg-$newCounter.jsonl"
    answerFile=11_DV-mmg-instructBlip$counter
    activeModels+=(${answerFile})
    if [ $3 -eq 1 ]
    then
        python ./model_scripts/instructblip.py --question-file $questionFile --answer-file-path $answerFilePath --answer-file-name $answerFile &
        PID=$!
        wait $PID
    fi

    newCounter=$((counter + 2))
    questionFile="$1/_questions/questions_mmg-$newCounter.jsonl"
    modelPath=./models/llava-1.5-7b-hf/
    answerFile=11_DV-mmg-llava_15_7b$counter
    activeModels+=(${answerFile})
    if [ $3 -eq 1 ]
    then
        python ./model_scripts/llava.py --question-file $questionFile --answer-file-path $answerFilePath --model-path $modelPath --answer-file-name $answerFile &
        PID=$!
        wait $PID
    fi

    newCounter=$((counter + 2))
    questionFile="$1/_questions/questions_mmg-$newCounter.jsonl"
    modelPath=./models/llava-1.5-13b-hf/
    answerFile=11_DV-mmg-llava_15_13b$counter
    activeModels+=(${answerFile})
    if [ $3 -eq 1 ]
    then
        python ./model_scripts/llava-4bit.py --question-file $questionFile --answer-file-path $answerFilePath --model-path $modelPath --answer-file-name $answerFile &
        PID=$!
        wait $PID
    fi

    newCounter=$((counter + 2))
    questionFile="$1/_questions/questions_mmg-$newCounter.jsonl"
    modelPath=./models/llava-v1.6-mistral-7b-hf/
    answerFile=11_DV-mmg-llava_16_7b$counter
    activeModels+=(${answerFile})
    if [ $3 -eq 1 ]
    then
        python ./model_scripts/llava-1.6.py --question-file $questionFile --answer-file-path $answerFilePath --model-path $modelPath --answer-file-name $answerFile &
        PID=$!
        wait $PID
    fi

    python $1/scripts/mmg/analyze_answers.py --models ${activeModels[@]} &
    PID=$!
    wait $PID

    python $1/scripts/mmg/printResultTable.py --models ${activeModels[@]} &
    PID=$!
    wait $PID
done