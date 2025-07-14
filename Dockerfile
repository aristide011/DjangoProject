FROM python:3.12-slim

# Imposta la directory di lavoro
WORKDIR /app

# Copia il file requirements.txt
COPY requirements.txt .



# Aggiorna pip
RUN python -m pip install --upgrade pip
#Installa le dipendenze
RUN python -m pip install --no-cache-dir -r requirements.txt






# Copia il resto dell'applicazione
COPY . .

# Comando di avvio della tua applicazione
CMD ["waitress-serve", "--host=0.0.0.0", "--port=8000", "Back_end.wsgi:application"]



