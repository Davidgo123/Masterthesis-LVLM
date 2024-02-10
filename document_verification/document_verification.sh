#!/bin/bash

iterations=1
entityModus=multi_entity
#entityModus=single_entity

# - - - - - - - - - -

questionFile=/nfs/home/ernstd/data/news400/document_verification/$entityModus/questions.jsonl
answerFilePath=/nfs/home/ernstd/data/news400/document_verification/$entityModus/

# - - - - - - - - - -

python /nfs/home/ernstd/masterthesis_scripts/document_verification/$entityModus/prepare_questions.py &
pid1=$!
wait $pid1

# - - - - - - - - - -

for ((VAR=0;VAR<$iterations;VAR=VAR+1));
do
    python /nfs/home/ernstd/masterthesis_scripts/document_verification/model_scripts/instructblip_dv.py --iteration $VAR --question-file $questionFile --answer-file-path $answerFilePath &
    pid2=$!
    wait $pid2

    #python /nfs/home/ernstd/masterthesis_scripts/document_verification/model_scripts/blip2_dv.py --iteration $VAR --question-file $questionFile --answer-file-path $answerFilePath &
    #pid3=$!
    #wait $pid3

    #python /nfs/home/ernstd/masterthesis_scripts/document_verification/model_scripts/llava-7b_dv.py --iteration $VAR --question-file $questionFile --answer-file-path $answerFilePath &
    #pid4=$!
    #wait $pid4

    #python /nfs/home/ernstd/masterthesis_scripts/document_verification/model_scripts/llava-13b_dv.py --iteration $VAR --question-file $questionFile --answer-file-path $answerFilePath &
    #pid5=$!
    #wait $pid5
done

# - - - - - - - - - -

python /nfs/home/ernstd/masterthesis_scripts/document_verification/$entityModus/analyze_answers.py --iterations $iterations &
pid6=$!
wait $pid6