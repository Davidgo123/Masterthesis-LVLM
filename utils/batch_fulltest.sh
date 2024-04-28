# # # # # # # # # # # # # # #
#         variables         #
# # # # # # # # # # # # # # #
createQuestions=1
runModels=1

basePath=(
    "./experiments/01_without_comparative_images/11_document_verification"
    "./experiments/01_without_comparative_images/12_entity_verification"
    "./experiments/02_with_comparative_images/21_single_input_models/211_entity_verification_1x1"
    "./experiments/02_with_comparative_images/21_single_input_models/212_entity_verification_1xN"
    "./experiments/02_with_comparative_images/22_multi_input_models/221_entity_verification_1x1"
    "./experiments/02_with_comparative_images/22_multi_input_models/222_entity_verification_1xN"
)


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
sbatch -w devbox5 -c 12 --mem 32G --gres=gpu:a3090:1 --output=./output/logs/211-EV-1x1-News400.out ${basePath[2]}/run_news400.sh ${basePath[2]} $createQuestions $runModels
sbatch -w devbox5 -c 12 --mem 32G --gres=gpu:a3090:1 --output=./output/logs/211-EV-1x1-Tamperednews.out ${basePath[2]}/run_tamperednews.sh ${basePath[2]} $createQuestions $runModels
sbatch -w devbox5 -c 12 --mem 32G --gres=gpu:a3090:1 --output=./output/logs/212-EV-1xN-Tamperednews.out ${basePath[3]}/run_tamperednews.sh ${basePath[3]} $createQuestions $runModels


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 


# # # # # # # # # # # # # # # # # # # # #
#       02 - with multi image - EV      #
# # # # # # # # # # # # # # # # # # # # #
sbatch -w devbox5 -c 12 --mem 32G --gres=gpu:a3090:1 --output=./output/logs/221-EV-1x1-News400.out ${basePath[4]}/run_news400.sh ${basePath[4]} $createQuestions $runModels
sbatch -w devbox5 -c 12 --mem 32G --gres=gpu:a3090:1 --output=./output/logs/221-EV-1x1-Tamperednews.out ${basePath[4]}/run_tamperednews.sh ${basePath[4]} $createQuestions $runModels
sbatch -w devbox5 -c 12 --mem 32G --gres=gpu:a3090:1 --output=./output/logs/222-EV-1xN-Tamperednews.out ${basePath[5]}/run_tamperednews.sh ${basePath[5]} $createQuestions $runModels
