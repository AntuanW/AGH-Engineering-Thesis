# Wybór podstawowego obrazu z Pythonem i Node.js
FROM python:3.12-slim as python-base

# Instalacja Node.js w tym samym kontenerze
RUN apt-get update && apt-get install -y curl && \
    curl -fsSL https://deb.nodesource.com/setup_18.x | bash - && \
    apt-get install -y nodejs && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Ustawienie katalogu roboczego
WORKDIR /app

# --- Backend ---
# Skopiowanie backendu
COPY backend/ ./backend/

# Instalacja zależności Pythona
RUN python3 -m venv /venv && \
    /venv/bin/pip install --upgrade pip && \
    /venv/bin/pip install -e ./backend

# --- Frontend ---
# Skopiowanie frontendowych plików
COPY frontend/ ./frontend/

# Instalacja zależności Node.js
WORKDIR /app/frontend
RUN npm install && npm run build

# --- Powrót do katalogu głównego ---
WORKDIR /app

# Eksponowanie portów
EXPOSE 8000 3000

# Skrypt startowy
CMD ["sh", "-c", "/venv/bin/start-app & npm start --prefix /app/frontend"]
