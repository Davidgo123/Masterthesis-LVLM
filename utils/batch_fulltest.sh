basePath=(
    "./experiments/01_without_comparative_images/11_document_verification"
    "./experiments/01_without_comparative_images/12_entity_verification"
    "./experiments/02_with_comparative_images/21_single_input_models/211_entity_verification_1x1"
    "./experiments/02_with_comparative_images/21_single_input_models/212_entity_verification_1xN"
    "./experiments/02_with_comparative_images/22_multi_input_models/221_entity_verification_1x1"
    "./experiments/02_with_comparative_images/22_multi_input_models/222_entity_verification_1xN"
    "./experiments/03_fine_tuning/311_document_verification"
)


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 


# # # # # # # # # # # # # # #
#         variables         #
# # # # # # # # # # # # # # #
createQuestions=0
runModels=0


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 


# # # # # # # # # # # # # # # # # # # #
#       01 - Prompt checking - EV      #
# # # # # # # # # # # # # # # # # # # #
# path=./experiments/00_prompt_analytics/01_entity_verification
# sbatch -w devbox5 -c 12 --mem 32G --gres=gpu:a3090:1 --output=./output/logs/01-EV-News400.out $path/run_news400.sh $path $createQuestions $runModels


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 


# # # # # # # # # # # # # # # # # # # #
#       01 - without images - DV      #
# # # # # # # # # # # # # # # # # # # #
# sbatch -w devbox5 -c 12 --mem 32G --gres=gpu:a3090:1 --output=./output/logs/11-DV-MMG.out ${basePath[0]}/run_mmg.sh ${basePath[0]} $createQuestions $runModels
# sbatch -w devbox5 -c 12 --mem 32G --gres=gpu:a3090:1 --output=./output/logs/11-DV-News400.out ${basePath[0]}/run_news400.sh ${basePath[0]} $createQuestions $runModels
# sbatch -w devbox5 -c 12 --mem 32G --gres=gpu:a3090:1 --output=./output/logs/11-DV-Tamperednews.out ${basePath[0]}/run_tamperednews.sh ${basePath[0]} $createQuestions $runModels


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 


# # # # # # # # # # # # # # # # # # # #
#       01 - without images - EV      #
# # # # # # # # # # # # # # # # # # # #
# sbatch -w devbox5 -c 12 --mem 32G --gres=gpu:a3090:1 --output=./output/logs/12-EV-MMG.out ${basePath[1]}/run_mmg.sh ${basePath[1]} $createQuestions $runModels
# sbatch -w devbox5 -c 12 --mem 32G --gres=gpu:a3090:1 --output=./output/logs/12-EV-News400.out ${basePath[1]}/run_news400.sh ${basePath[1]} $createQuestions $runModels
# sbatch -w devbox5 -c 12 --mem 32G --gres=gpu:a3090:1 --output=./output/logs/12-EV-Tamperednews.out ${basePath[1]}/run_tamperednews.sh ${basePath[1]} $createQuestions $runModels


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 


# # # # # # # # # # # # # # # # # # # # # 
#       02 - with single image - EV     #
# # # # # # # # # # # # # # # # # # # # # 
# sbatch -w gpu3 -c 12 --mem 32G --gres=gpu:1 --output=./output/logs/212-EV-1xN-News400.out ${basePath[3]}/run_news400.sh ${basePath[3]} $createQuestions $runModels
# sbatch -w gpu3 -c 12 --mem 32G --gres=gpu:1 --output=./output/logs/212-EV-1xN-Tamperednews.out ${basePath[3]}/run_tamperednews.sh ${basePath[3]} $createQuestions $runModels


# # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 


# # # # # # # # # # # # # # # # # # # # # #
# #       02 - with multi image - EV      #
# # # # # # # # # # # # # # # # # # # # # #
# sbatch -w gpu3 -c 12 --mem 32G --gres=gpu:1 --output=./output/logs/222-EV-1xN-News400.out ${basePath[5]}/run_news400.sh ${basePath[5]} $createQuestions $runModels
# sbatch -w gpu3 -c 12 --mem 32G --gres=gpu:1 --output=./output/logs/222-EV-1xN-Tamperednews.out ${basePath[5]}/run_tamperednews.sh ${basePath[5]} $createQuestions $runModels


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 


# # # # # # # # # # # # # # # # # # # # # # # # #
#       03 - without images - DV - trained      #
# # # # # # # # # # # # # # # # # # # # # # # # #
checkpointPath=/nfs/home/ernstd/masterthesis_scripts/experiments/03_fine_tuning/310_train/InstructBLIP_PEFT/output/results/tamperedNews/tamperedNews_37/20240531204/checkpoint_best.pth
sbatch -w gpu2 -c 12 --mem 32G --gres=gpu:1 --output=./output/logs/311-DV-MMG.out ${basePath[6]}/run_mmg.sh ${basePath[6]} $createQuestions $runModels $checkpointPath
sbatch -w gpu2 -c 12 --mem 32G --gres=gpu:1 --output=./output/logs/311-DV-News400.out ${basePath[6]}/run_news400.sh ${basePath[6]} $createQuestions $runModels $checkpointPath
sbatch -w gpu2 -c 12 --mem 32G --gres=gpu:1 --output=./output/logs/311-DV-Tamperednews.out ${basePath[6]}/run_tamperednews.sh ${basePath[6]} $createQuestions $runModels $checkpointPath
