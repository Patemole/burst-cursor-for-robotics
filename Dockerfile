FROM python:3.10-slim

# Installe Mujoco deps
RUN apt-get update && apt-get install -y \
gcc g++ patchelf libosmesa6-dev libgl1-mesa-glx libglfw3 xvfb mesa-utils \
swig \
&& rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt ./
# Installe les dépendances Python + gymnasium extras
RUN python -m pip install --upgrade pip && \
    pip install --no-cache-dir \
      --default-timeout=120 \
      --retries 5 \
      -r requirements.txt && \
    pip install "gymnasium[classic_control]" "gymnasium[box2d]"

COPY train.py ./train.py
COPY train_sac.py ./train_sac.py     
COPY export_onnx.py ./export_onnx.py
COPY models/ ./models/
COPY scenarios/ ./scenarios/
COPY start.sh ./start.sh
RUN chmod +x ./start.sh
RUN mkdir -p output
    
CMD ["./start.sh"]