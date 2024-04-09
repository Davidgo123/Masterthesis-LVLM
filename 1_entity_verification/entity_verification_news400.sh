#!/bin/bash

activeModels=()

# - - - - - - - - - -

questionFile=/nfs/home/ernstd/masterthesis_scripts/1_entity_verification/_questions/questions_news400.jsonl
answerFilePath=/nfs/home/ernstd/masterthesis_scripts/1_entity_verification/model_answers/news400/

# - - - - - - - - - -

python /nfs/home/ernstd/masterthesis_scripts/1_entity_verification/scripts/news400/prepare_questions.py --question-file $questionFile &
PID=$!
wait $PID

# - - - - - - - - - -

answerFile=blip_2_answers
activeModels+=(${answerFile})
python /nfs/home/ernstd/masterthesis_scripts/model_scripts/blip2_dv.py --question-file $questionFile --answer-file-path $answerFilePath --answer-file-name $answerFile &
PID=$!
wait $PID

answerFile=instructBlip_answers
activeModels+=(${answerFile})
python /nfs/home/ernstd/masterthesis_scripts/model_scripts/instructblip_dv.py --question-file $questionFile --answer-file-path $answerFilePath --answer-file-name $answerFile &
PID=$!
wait $PID

modelPath=/nfs/home/ernstd/models/llava-1.5-7b-hf/
answerFile=llava_1_5_7b_answers
activeModels+=(${answerFile})
python /nfs/home/ernstd/masterthesis_scripts/model_scripts/llava_dv.py --question-file $questionFile --answer-file-path $answerFilePath --model-path $modelPath --answer-file-name $answerFile &
PID=$!
wait $PID

modelPath=/nfs/home/ernstd/models/llava-1.5-13b-hf/
answerFile=llava_1_5_13b_answers
activeModels+=(${answerFile})
python /nfs/home/ernstd/masterthesis_scripts/model_scripts/llava-4bit_dv.py --question-file $questionFile --answer-file-path $answerFilePath --model-path $modelPath --answer-file-name $answerFile &
PID=$!
wait $PID

modelPath=/nfs/home/ernstd/models/llava-v1.6-mistral-7b-hf/
answerFile=llava_1_6_7b_answers
activeModels+=(${answerFile})
python /nfs/home/ernstd/masterthesis_scripts/model_scripts/llava_dv.py --question-file $questionFile --answer-file-path $answerFilePath --model-path $modelPath --answer-file-name $answerFile &
PID=$!
wait $PID

# - - - - - - - - - -

python /nfs/home/ernstd/masterthesis_scripts/1_entity_verification/scripts/news400/analyze_answers.py --models ${activeModels[@]} &
PID=$!
wait $PID

python /nfs/home/ernstd/masterthesis_scripts/1_entity_verification/scripts/news400/printResultTable.py --models ${activeModels[@]} &
PID=$!
wait $PID