#!/bin/sh
#SBATCH --time 24:00:00
#SBATCH -o testing%j.out
#SBATCH -e testing%j.err
#SBATCH -p large-gpu -N 6
#SBATCH --mail-user=adimaini@gwu.edu 
#SBATCH --mail-type=ALL

module load python3/3.7.2
source "/lustre/groups/caliskangrp/adimaini/deepspeech/deepspeech2-env/bin/activate"
cd /lustre/groups/caliskangrp/adimaini/deepspeech/DeepSpeech

python -u DeepSpeech.py --noshow_progressbar \
  --train_files data/cmu/train.csv \
  --test_files data/cmu/test.csv \
  --dev_files data/cmu/dev.csv \
  --train_batch_size 40 \
  --dev_batch_size 40 \
  --test_batch_size 40 \
  --n_hidden 100 \
  --early_stop True \
  --export_dir '/SEAS/home/adimaini/deepspeech/outputs' \
  --epochs 600 \
  --learning_rate 0.001 --dropout_rate 0.15 \
  --checkpoint_dir '/SEAS/home/adimaini/deepspeech/outputs' 
  # --audio_sample_rate 1
  # --scorer_path '/home/adimaini/deepspeech/outputs/pruned_lm.scorer' \

