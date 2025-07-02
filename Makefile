# Nom des services Docker Compose
COMPOSE=docker-compose
PROJECT=burst-cursor-for-robotics

# --- Commandes de base ---

# Build les images sans lancer
build:
	$(COMPOSE) build

# Lance les conteneurs avec build auto
up:
	$(COMPOSE) up --build

# Stoppe les conteneurs (grâce à Ctrl+C ou autre)
stop:
	$(COMPOSE) stop

# Stoppe et supprime les conteneurs + orphelins
down:
	$(COMPOSE) down --remove-orphans

# Clean complet (conteneurs + volumes)
clean:
	$(COMPOSE) down --volumes --remove-orphans

# Affiche les logs
logs:
	$(COMPOSE) logs -f

# Relance juste le backend (utile en dev)
restart-backend:
	$(COMPOSE) restart backend

# --- Tests unitaires / API ---
curl:
	curl http://localhost:8000

docs:
	open http://localhost:8000/docs

# --- Bonus : vérifie si Docker fonctionne ---
check:
	docker ps
