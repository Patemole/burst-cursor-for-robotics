import os
import gymnasium as gym
from gymnasium.wrappers import RecordVideo
from stable_baselines3 import PPO
from export_onnx import export_policy_to_onnx

# 🎯 Chemins
OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 🦾 Charge ton humanoïde dans Mujoco
# Remplace 'Humanoid-v4' par ton env spécifique le cas échéant
env_id = "Humanoid-v4"

env = gym.make(env_id, render_mode="rgb_array")
#env = gym.make(env_id)

# 🎥 Enregistre une vidéo pendant le training

env = RecordVideo(
    env,
    video_folder=os.path.join(OUTPUT_DIR, "videos"),
    #episode_trigger=lambda ep: True  # Capture au 1er épisode
    episode_trigger=lambda ep: ep % 3000 == 0  # Une vidéo tous les 15 épisodes
    #episode_trigger=lambda ep: ep == (N-1)  # N = nombre d'épisodes total Pour enregistrer que une video a la fin
)


# 🧠 Initialise le modèle PPO
model = PPO(
    policy="MlpPolicy",
    env=env,
    verbose=1,
    tensorboard_log="./tensorboard_logs"
)

# 🏃‍♂️ Lance l’entraînement sur 50 000 steps
model.learn(total_timesteps=5_500_000)

# 💾 Sauvegarde le policy au format ONNX
onnx_path = os.path.join(OUTPUT_DIR, "policy.onnx")

#model.policy.export(onnx_path) #Need to change this. 
export_policy_to_onnx(model.policy, env, onnx_path)

print(f"✅ Modèle exporté : {onnx_path}")

env.close()
print(f"🎥 Vidéos sauvegardées dans {os.path.join(OUTPUT_DIR, 'videos')}")
