#!/bin/bash
#srun --pty -w devbox5 -c 12 --mem 32G --gres=gpu:a3090:1 zsh && conda activate transformer
srun --pty -w gpu2 -c 12 --mem 32G --gres=gpu:1 zsh && conda activate transformer