sbatch -w devbox5 -c 12 --mem 32G --gres=gpu:a3090:1 --output=./masterthesis_scripts/_utils/_SLURM/DV-MMG.out /nfs/home/ernstd/masterthesis_scripts/0_document_verification/document_verification_mmg.sh
sbatch -w devbox5 -c 12 --mem 32G --gres=gpu:a3090:1 --output=./masterthesis_scripts/_utils/_SLURM/DV-News400.out /nfs/home/ernstd/masterthesis_scripts/0_document_verification/document_verification_news400.sh
sbatch -w devbox5 -c 12 --mem 32G --gres=gpu:a3090:1 --output=./masterthesis_scripts/_utils/_SLURM/DV-TampNews.out /nfs/home/ernstd/masterthesis_scripts/0_document_verification/document_verification_tamperedNews.sh