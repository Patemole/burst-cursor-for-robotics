#!/bin/bash
# Lance l'entraînement sous Xvfb pour le rendu offscreen
xvfb-run -s "-screen 0 1280x1024x24" python3 train_sac.py &
# Lance Tensorboard (sur le port 6006, accessible de l'extérieur)
python -m tensorboard.main --logdir /app/tensorboard_logs --host 0.0.0.0
