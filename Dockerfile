FROM python:3.12-slim

# Imposta la directory di lavoro
WORKDIR /app

# Copia il file requirements.txt
COPY requirements.txt .

# Aggiorna pip e installa le dipendenze
RUN python -m pip install --upgrade pip && \
    python -m pip install --no-cache-dir -r requirements.txt

# Copia il resto dell'applicazione
COPY . .

# Comando di avvio della tua applicazione
CMD ["python", "manage.py","runserver", "0.0.0.0:8000"]