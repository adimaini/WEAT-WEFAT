#!/bin/sh
#SBATCH --time 10:00
#SBATCH -o testing%j.out
#SBATCH -e testing%j.err
#SBATCH -p small-gpu -N 2
#SBATCH --mail-user=adimaini@gwu.edu 
#SBATCH --mail-type=ALL

module load python3/3.7.2
source "/lustre/groups/caliskangrp/adimaini/deepspeech/deepspeech-env/bin/activate"
cd /lustre/groups/caliskangrp/adimaini/deepspeech/DeepSpeech

set -xe

# Force only one visible device because we have a single-sample dataset
# and when trying to run on multiple devices (like GPUs), this will break
export CUDA_VISIBLE_DEVICES=0

python -u DeepSpeech.py --noshow_progressbar \
  --train_files data/cmu/train.csv \
  --test_files data/cmu/test.csv \
  --dev_files data/cmu/dev.csv \
  --train_batch_size 1 \
  --test_batch_size 1 \
  --export_dir '/SEAS/home/adimaini/deepspeech/outputs' \
  --n_hidden 100 \
  --epochs 200 \
  --learning_rate 0.001 --dropout_rate 0.05 \
  --checkpoint_dir '/SEAS/home/adimaini/deepspeech/outputs' \
  # --audio_sample_rate 1
  # --scorer_path '/home/adimaini/deepspeech/outputs/pruned_lm.scorer' \

