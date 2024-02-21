#!/bin/bash

srun --pty -w devbox5 -c 12 --mem 32G --gres=gpu:a3090:1 zsh && conda activate transformer
#srun --pty -w devbox3 -c 12 --mem 32G --gres=gpu:t2080ti:1 zsh && conda activate transformer