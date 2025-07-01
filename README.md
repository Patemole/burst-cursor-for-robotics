# Burst - the cursor for robotics



To see metrics
tensorboard --logdir tensorboard_logs/


Voici un **récapitulatif complet** des commandes à exécuter, étape par étape, pour configurer ton serveur EC2 GPU, transférer ton projet, lancer l'entraînement, et récupérer les résultats ✅

---

## 🧱 1. Connexion SSH à ton serveur EC2

```bash
ssh -i ~/Desktop/burst-humanoide-key.pem ubuntu@18.226.163.192
```

---

## 🐍 2. Activer l’environnement PyTorch fourni par l’AMI AWS

```bash
source /opt/pytorch/bin/activate
```

---

## 🐳 3. Installer Docker (si ce n'est pas déjà fait)

```bash
curl -fsSL https://get.docker.com -o get-docker.sh && sh get-docker.sh
sudo usermod -aG docker $USER
```

> 🔁 **Puis reconnecte-toi au SSH** pour appliquer les droits :

```bash
exit
# Puis reconnecte :
ssh -i ~/Desktop/burst-humanoide-key.pem ubuntu@18.226.163.192
```

---

## 📂 4. Transférer ton projet depuis ton Mac

```bash
scp -i ~/Desktop/burst-humanoide-key.pem -r ~/burst-cursor-for-robotics ubuntu@18.226.163.192:~/
```

---

## 🐳 5. Builder ton image Docker

```bash
cd ~/burst-cursor-for-robotics
docker build --no-cache -t burst-mvp-1 .
```

---

## 🚀 6. Lancer l'entraînement dans le conteneur Docker

```bash
docker run --rm -it --gpus all -p 6006:6006 \
  -v "$(pwd)/output:/app/output" \
  -v "$(pwd)/tensorboard_logs:/app/tensorboard_logs" \
  burst-mvp-1
```

---

## 📊 7. Visualiser TensorBoard dans le navigateur

Depuis ton Mac :

```
http://18.226.163.192:6006/
```

---

## ⬇️ 8. Télécharger les résultats (vidéos, modèle, logs)

Sur **ton Mac** :

```bash
scp -i ~/Desktop/burst-humanoide-key.pem -r \
    ubuntu@18.226.163.192:~/burst-cursor-for-robotics/output ~/Desktop/

scp -i ~/Desktop/burst-humanoide-key.pem -r \
    ubuntu@18.226.163.192:~/burst-cursor-for-robotics/tensorboard_logs ~/Desktop/
```

---

## ✅ Résultat attendu

* Le modèle exporté est dans : `output/policy.onnx`
* Les vidéos sont dans : `output/dossiers/videos/`
* TensorBoard est accessible via IP:6006
* Tu peux itérer facilement sur les modifs de ton code et rebuilder + relancer

---

Tu veux que je t’écrive tout ça en script `.sh` pour automatiser ?
