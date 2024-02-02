#!/bin/bash

#srun --pty --mem 48G --gres=gpu:1 zsh && conda activate transformer
srun --pty -w devbox5 --mem 48G --gres=gpu:1 zsh && conda activate transformer

