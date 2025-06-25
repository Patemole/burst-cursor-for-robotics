# export_onnx.py
import torch

def export_policy_to_onnx(policy, env, onnx_path):
    # On récupère un exemple d'observation pour tracer le modèle
    obs = env.observation_space.sample()
    obs_tensor = torch.tensor([obs], dtype=torch.float32)

    # Export du modèle en ONNX
    torch.onnx.export(
        policy,                   # Le modèle PyTorch à exporter
        obs_tensor,               # Un exemple d'entrée
        onnx_path,                # Chemin de sortie
        export_params=True,
        opset_version=11,
        do_constant_folding=True,
        input_names=['input'],
        output_names=['output'],
        dynamic_axes={'input': {0: 'batch_size'}, 'output': {0: 'batch_size'}}
    )
    print(f"✅ Modèle exporté au format ONNX : {onnx_path}")