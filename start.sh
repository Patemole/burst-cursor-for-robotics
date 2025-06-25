#!/bin/bash
# Lance l'entraînement en arrière-plan
python train.py &
# Lance Tensorboard (sur le port 6006, accessible de l'extérieur)
tensorboard --logdir /app/tensorboard_logs --host 0.0.0.0
