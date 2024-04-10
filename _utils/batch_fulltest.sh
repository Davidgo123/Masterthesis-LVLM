createQuestions=0
runModels=0

# sbatch -w devbox5 -c 12 --mem 32G --gres=gpu:a3090:1 --output=/nfs/home/ernstd/masterthesis_scripts/_utils/_SLURM/DV-MMG.out /nfs/home/ernstd/masterthesis_scripts/0_document_verification/document_verification_mmg.sh $createQuestions $runModels
# sbatch -w devbox5 -c 12 --mem 32G --gres=gpu:a3090:1 --output=/nfs/home/ernstd/masterthesis_scripts/_utils/_SLURM/DV-News400.out /nfs/home/ernstd/masterthesis_scripts/0_document_verification/document_verification_news400.sh $createQuestions $runModels
# sbatch -w devbox5 -c 12 --mem 32G --gres=gpu:a3090:1 --output=/nfs/home/ernstd/masterthesis_scripts/_utils/_SLURM/DV-TampNews.out /nfs/home/ernstd/masterthesis_scripts/0_document_verification/document_verification_tamperedNews.sh $createQuestions $runModels

# sbatch -w devbox5 -c 12 --mem 32G --gres=gpu:a3090:1 --output=/nfs/home/ernstd/masterthesis_scripts/_utils/_SLURM/EV-MMG.out /nfs/home/ernstd/masterthesis_scripts/1_entity_verification/entity_verification_mmg.sh $createQuestions $runModels
# sbatch -w devbox5 -c 12 --mem 32G --gres=gpu:a3090:1 --output=/nfs/home/ernstd/masterthesis_scripts/_utils/_SLURM/EV-News400.out /nfs/home/ernstd/masterthesis_scripts/1_entity_verification/entity_verification_news400.sh $createQuestions $runModels
# sbatch -w devbox5 -c 12 --mem 32G --gres=gpu:a3090:1 --output=/nfs/home/ernstd/masterthesis_scripts/_utils/_SLURM/EV-TampNews.out /nfs/home/ernstd/masterthesis_scripts/1_entity_verification/entity_verification_tamperedNews.sh $createQuestions $runModels

# sbatch -w devbox5 -c 12 --mem 32G --gres=gpu:a3090:1 --output=/nfs/home/ernstd/masterthesis_scripts/_utils/_SLURM/IEV-News400.out /nfs/home/ernstd/masterthesis_scripts/2_image_entity_verification/image_entity_verification_news400.sh $createQuestions $runModels
# sbatch -w devbox5 -c 12 --mem 32G --gres=gpu:a3090:1 --output=/nfs/home/ernstd/masterthesis_scripts/_utils/_SLURM/IEV-TampNews.out /nfs/home/ernstd/masterthesis_scripts/2_image_entity_verification/image_entity_verification_tamperedNews.sh $createQuestions $runModels

sbatch -w devbox5 -c 12 --mem 32G --gres=gpu:a3090:1 --output=/nfs/home/ernstd/masterthesis_scripts/_utils/_SLURM/MIEV-TampNews.out /nfs/home/ernstd/masterthesis_scripts/3_max_image_entity_verification/max_image_entity_verification_tamperedNews.sh $createQuestions $runModels
