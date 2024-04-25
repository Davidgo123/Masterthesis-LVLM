createQuestions=1
runModels=1

# # # document verification
sbatch -w devbox5 -c 12 --mem 32G --gres=gpu:a3090:1 --output=./output/logs/DV-MMG.out ./experiments/1_document_verification/run_DV_mmg.sh $createQuestions $runModels
sbatch -w devbox5 -c 12 --mem 32G --gres=gpu:a3090:1 --output=./output/logs/DV-News400.out ./experiments/1_document_verification/run_DV_news400.sh $createQuestions $runModels
sbatch -w devbox5 -c 12 --mem 32G --gres=gpu:a3090:1 --output=./output/logs/DV-Tamperednews.out ./experiments/1_document_verification/run_DV_tamperednews.sh $createQuestions $runModels

# # # entity verification
sbatch -w devbox5 -c 12 --mem 32G --gres=gpu:a3090:1 --output=./output/logs/EV-MMG.out ./experiments/2_entity_verification/run_EV_mmg.sh $createQuestions $runModels
sbatch -w devbox5 -c 12 --mem 32G --gres=gpu:a3090:1 --output=./output/logs/EV-News400.out ./experiments/2_entity_verification/run_EV_news400.sh $createQuestions $runModels
sbatch -w devbox5 -c 12 --mem 32G --gres=gpu:a3090:1 --output=./output/logs/EV-Tamperednews.out ./experiments/2_entity_verification/run_EV_tamperednews.sh $createQuestions $runModels

# # # image based entity verification
sbatch -w devbox5 -c 12 --mem 32G --gres=gpu:a3090:1 --output=./output/logs/IEV-News400.out ./experiments/3_image_entity_verification/run_IEV_news400.sh $createQuestions $runModels
sbatch -w devbox5 -c 12 --mem 32G --gres=gpu:a3090:1 --output=./output/logs/IEV-Tamperednews.out ./experiments/3_image_entity_verification/run_IEV_tamperednews.sh $createQuestions $runModels

# # # multi image based entity verification
sbatch -w devbox5 -c 12 --mem 32G --gres=gpu:a3090:1 --output=./output/logs/MIEV-Tamperednews.out ./experiments/4_multi_image_entity_verification/run_MIEV_tamperednews.sh $createQuestions $runModels
