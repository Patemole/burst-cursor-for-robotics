FROM python:3.10-slim

# Installe Mujoco deps
RUN apt-get update && apt-get install -y \
gcc g++ patchelf libosmesa6-dev libgl1-mesa-glx libglfw3 xvfb mesa-utils && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY train.py ./train.py
COPY export_onnx.py ./export_onnx.py
COPY models/ ./models/
COPY scenarios/ ./scenarios/
COPY start.sh ./start.sh
RUN chmod +x ./start.sh
RUN mkdir -p output
    
CMD ["./start.sh"]