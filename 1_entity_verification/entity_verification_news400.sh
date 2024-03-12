#!/bin/bash

activeModels=()

# - - - - - - - - - -

questionFile=/nfs/home/ernstd/masterthesis_scripts/0_document_verification/_questions/questions_news400.jsonl
answerFilePath=/nfs/home/ernstd/masterthesis_scripts/0_document_verification/model_answers/news400/

# - - - - - - - - - -

python /nfs/home/ernstd/masterthesis_scripts/0_document_verification/scripts/news400/prepare_questions.py --question-file $questionFile &
pid1=$!
wait $pid1

# - - - - - - - - - -

answerFile=blip_2_answers
activeModels+=(${answerFile})
python /nfs/home/ernstd/masterthesis_scripts/model_scripts/blip2_dv.py --question-file $questionFile --answer-file-path $answerFilePath --answer-file-name $answerFile &
pid4=$!
wait $pid4

answerFile=instructBlip_answers
activeModels+=(${answerFile})
python /nfs/home/ernstd/masterthesis_scripts/model_scripts/instructblip_dv.py --question-file $questionFile --answer-file-path $answerFilePath --answer-file-name $answerFile &
pid5=$!
wait $pid5

modelPath=/nfs/home/ernstd/models/llava-1.5-7b-hf/
answerFile=llava_1_5_7b_answers
activeModels+=(${answerFile})
python /nfs/home/ernstd/masterthesis_scripts/model_scripts/llava_dv.py --question-file $questionFile --answer-file-path $answerFilePath --model-path $modelPath --answer-file-name $answerFile &
pid5=$!
wait $pid5

modelPath=/nfs/home/ernstd/models/llava-1.5-13b-hf/
answerFile=llava_1_5_13b_answers
activeModels+=(${answerFile})
python /nfs/home/ernstd/masterthesis_scripts/model_scripts/llava-4bit_dv.py --question-file $questionFile --answer-file-path $answerFilePath --model-path $modelPath --answer-file-name $answerFile &
pid6=$!
wait $pid6

# - - - - - - - - - -

python /nfs/home/ernstd/masterthesis_scripts/0_document_verification/scripts/news400/analyze_answers.py --models ${activeModels[@]} &
pid7=$!
wait $pid7

python /nfs/home/ernstd/masterthesis_scripts/0_document_verification/scripts/news400/printResultTable.py --models ${activeModels[@]} &
pid8=$!
wait $pid8