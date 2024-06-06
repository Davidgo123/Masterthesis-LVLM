basePath=(
    "./experiments/01_without_comparative_images/11_document_verification"
    "./experiments/01_without_comparative_images/12_entity_verification"
    "./experiments/02_with_comparative_images/21_single_1xN"
    "./experiments/02_with_comparative_images/22_multi_1xN"
    "./experiments/03_fine_tuning/32_document_verification"
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
# path=./experiments/00_prompt_analytics
# sbatch -w devbox5 -c 12 --mem 32G --gres=gpu:a3090:1 --output=./output/logs/00-EV-News400.out $path/run_news400.sh $path $createQuestions $runModels


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
# sbatch -w devbox5 -c 12 --mem 32G --gres=gpu:a3090:1 --output=./output/logs/21-EV-1xN-News400.out ${basePath[2]}/run_news400.sh ${basePath[2]} $createQuestions $runModels
# sbatch -w devbox5 -c 12 --mem 32G --gres=gpu:a3090:1 --output=./output/logs/21-EV-1xN-Tamperednews.out ${basePath[2]}/run_tamperednews.sh ${basePath[2]} $createQuestions $runModels


# # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 


# # # # # # # # # # # # # # # # # # # # # #
# #       02 - with multi image - EV      #
# # # # # # # # # # # # # # # # # # # # # #
# sbatch -w devbox5 -c 12 --mem 32G --gres=gpu:a3090:1 --output=./output/logs/22-EV-1xN-News400.out ${basePath[3]}/run_news400.sh ${basePath[3]} $createQuestions $runModels
# sbatch -w devbox5 -c 12 --mem 32G --gres=gpu:a3090:1 --output=./output/logs/22-EV-1xN-Tamperednews.out ${basePath[3]}/run_tamperednews.sh ${basePath[3]} $createQuestions $runModels


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 


# # # # # # # # # # # # # # # # # # # # # # # # #
#       03 - without images - DV - trained      #
# # # # # # # # # # # # # # # # # # # # # # # # #
# checkpointPath=/nfs/home/ernstd/masterthesis_scripts/experiments/03_fine_tuning/31_train/InstructBLIP_PEFT/output/results/tamperedNews/tamperedNews_37/20240531204/checkpoint_best.pth
# sbatch -w gpu2 -c 12 --mem 32G --gres=gpu:1 --output=./output/logs/32-DV-MMG.out ${basePath[4]}/run_mmg.sh ${basePath[4]} $createQuestions $runModels $checkpointPath
# sbatch -w gpu2 -c 12 --mem 32G --gres=gpu:1 --output=./output/logs/32-DV-News400.out ${basePath[4]}/run_news400.sh ${basePath[4]} $createQuestions $runModels $checkpointPath
# sbatch -w gpu2 -c 12 --mem 32G --gres=gpu:1 --output=./output/logs/32-DV-Tamperednews.out ${basePath[4]}/run_tamperednews.sh ${basePath[4]} $createQuestions $runModels $checkpointPath
