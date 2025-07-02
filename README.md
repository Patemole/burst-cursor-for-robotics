# Burst: Robotics RL Pipeline

## Overview
Burst is a modular reinforcement learning pipeline for robotics. It enables fast iteration, reproducible training, and easy deployment of RL agents. The project is containerized (Docker Compose) and supports both local and remote (GPU) execution. The backend service is included for future API or UI integration.

## Value Proposition
- One-command setup for RL training and experiment tracking
- GPU-ready, cloud-friendly (EC2, GCP, etc.)
- Modular: backend and trainer run as separate services
- Results and logs are easy to access and download

---

## Quickstart (Local)

### 1. Build and start all services
```bash
docker compose build
```
```bash
docker compose up
```

- `trainer`: runs RL training, writes logs and outputs
- `backend`: placeholder for API/UI (runs on port 8000)
- `tensorboard`: available at http://localhost:6006/

### 2. Stop all services
```bash
docker compose down
```

### 3. View logs
```bash
docker compose logs -f trainer
```

---

## Running on a Remote GPU Server (e.g. EC2)

1. SSH into your instance:
```bash
ssh -i <key.pem> ubuntu@<EC2-IP>
```
2. Install Docker & Docker Compose:
```bash
curl -fsSL https://get.docker.com -o get-docker.sh && sh get-docker.sh
sudo usermod -aG docker $USER
exit # then reconnect
```
3. Install NVIDIA Container Toolkit (for GPU):
```bash
# See https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html
```
4. Copy project from your local machine:
```bash
scp -i <key.pem> -r ~/burst-cursor-for-robotics ubuntu@<EC2-IP>:~/
```
5. Build and start:
```bash
cd burst-cursor-for-robotics
docker compose --profile gpu build
docker compose --profile gpu up
```

- Access TensorBoard at http://<EC2-IP>:6006/
- Backend API at http://<EC2-IP>:8000/

---

## Download Results

From your local machine:
```bash
scp -i <key.pem> -r ubuntu@<EC2-IP>:~/burst-cursor-for-robotics/output ./
scp -i <key.pem> -r ubuntu@<EC2-IP>:~/burst-cursor-for-robotics/tensorboard_logs ./
```

---

## Expected Outputs
- Trained model: `output/policy.onnx`
- Videos: `output/videos/`
- TensorBoard logs: `tensorboard_logs/`

---

## Troubleshooting
- If you get GPU errors, check NVIDIA drivers and container toolkit
- If ports are busy, change them in `docker-compose.yml`
- To iterate: edit code, rebuild (`docker compose build`), and restart (`docker compose up`)

---

## Project Structure
- `trainer/` : RL training logic
- `backend/` : API/UI service (placeholder)
- `output/` : trained models, videos
- `tensorboard_logs/` : logs for TensorBoard

---

For automation, consider writing a Makefile or shell script for common workflows.
