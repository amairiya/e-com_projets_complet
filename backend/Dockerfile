# Image Python légère
FROM python:3.14-slim

# Empêche Python de générer des fichiers .pyc
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Dossier de travail
WORKDIR /app

# Dépendances système nécessaires à pandas / openpyxl
RUN apt-get update && apt-get install -y \
    gcc \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

    # Créer un user non-root
RUN addgroup --system app && adduser --system --group app

# Copier les fichiers de dépendances
COPY requirements.txt .

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code de l'application
COPY . .

# Donner les droits à l’utilisateur
RUN chown -R app:app /app

USER app

# Exposer le port Flask
EXPOSE 5000

# Lancer l'application
CMD ["python", "app.py"]
