# train_sac.py  —  version SAC + SubprocVecEnv
'''
import os, gymnasium as gym
from stable_baselines3 import SAC
from stable_baselines3.common.vec_env import SubprocVecEnv
from gymnasium.wrappers import RecordVideo
from export_onnx import export_policy_to_onnx


def main():
    OUTPUT_DIR = "output"
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    ENV_ID   = "MountainCarContinuous-v0"
    N_ENVS   = int(os.getenv("N_ENVS", 8))
    STEPS    = int(os.getenv("TOTAL_STEPS", 15_000_000))

    def make_env():
        env = gym.make(ENV_ID, render_mode="rgb_array")
        env = RecordVideo(
            env,
            video_folder=os.path.join(OUTPUT_DIR, "videos"),
            episode_trigger=lambda ep: ep % 5000 == 0
        )
        return env

    vec_env = SubprocVecEnv([make_env for _ in range(N_ENVS)])

    policy_kwargs = dict(net_arch=[512, 512])

    model = SAC(
        "MlpPolicy",
        vec_env,
        learning_rate   = 3e-4,
        batch_size      = 1024,
        buffer_size     = 1_000_000,
        train_freq      = (256, "step"),
        gradient_steps  = 256,
        policy_kwargs   = policy_kwargs,
        tensorboard_log = "./tensorboard_logs",
        device          = "cuda",
        verbose         = 1
    )

    model.learn(total_timesteps=STEPS)

    onnx_path = os.path.join(OUTPUT_DIR, "policy.onnx")
    export_policy_to_onnx(model.policy, vec_env, onnx_path)
    print(f"✅ Modèle SAC exporté : {onnx_path}")
    vec_env.close()

if __name__ == "__main__":
    main()
'''


import os
import gymnasium as gym
from stable_baselines3 import SAC
from stable_baselines3.common.vec_env import SubprocVecEnv, VecMonitor
from stable_baselines3.common.monitor import Monitor
from gymnasium.wrappers import RecordVideo
from export_onnx import export_policy_to_onnx
import re

def get_next_run_id(log_dir: str, prefix: str = "SAC") -> str:
    os.makedirs(log_dir, exist_ok=True)
    runs = [d for d in os.listdir(log_dir) if os.path.isdir(os.path.join(log_dir, d)) and d.startswith(prefix)]
    run_ids = [int(re.findall(rf"{prefix}_(\d+)", d)[0]) for d in runs if re.findall(rf"{prefix}_(\d+)", d)]
    next_id = max(run_ids) + 1 if run_ids else 1
    return f"{prefix}_{next_id}"

def main():
    OUTPUT_DIR = "output"
    TENSORBOARD_DIR = "tensorboard_logs"
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    ENV_ID   = "MountainCarContinuous-v0"
    N_ENVS   = int(os.getenv("N_ENVS", 8))
    STEPS    = int(os.getenv("TOTAL_STEPS", 15_000_000))

    run_name = get_next_run_id(TENSORBOARD_DIR, prefix="SAC")
    run_video_dir = os.path.join(OUTPUT_DIR, run_name, "videos")

    def make_env(rank):
        def _init():
            env = gym.make(ENV_ID, render_mode="rgb_array")
            env = Monitor(env)

            if rank == 0:
                env = RecordVideo(
                    env,
                    video_folder=run_video_dir,
                    episode_trigger=lambda ep: ep % 5000 == 0
                )
            return env
        return _init

    vec_env = SubprocVecEnv([make_env(i) for i in range(N_ENVS)])
    vec_env = VecMonitor(vec_env)

    policy_kwargs = dict(net_arch=[512, 512])

    model = SAC(
        "MlpPolicy",
        vec_env,
        learning_rate   = 3e-4,
        batch_size      = 1024,
        buffer_size     = 1_000_000,
        train_freq      = (256, "step"),
        gradient_steps  = 256,
        policy_kwargs   = policy_kwargs,
        tensorboard_log = TENSORBOARD_DIR,
        device          = "cuda",
        verbose         = 1
    )

    model.learn(total_timesteps=STEPS, tb_log_name=run_name)

    onnx_path = os.path.join(OUTPUT_DIR, run_name, "policy.onnx")
    export_policy_to_onnx(model.policy, vec_env, onnx_path)
    print(f"✅ Modèle SAC exporté : {onnx_path}")
    vec_env.close()

if __name__ == "__main__":
    main()


