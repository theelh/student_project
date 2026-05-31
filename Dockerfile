FROM python:3.12-slim AS builder
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements.txt .
RUN pip install --upgrade pip \
    && pip install --prefix=/install --no-cache-dir -r requirements.txt

FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY --from=builder /install /usr/local
COPY . .

# Dossier dédié pour la base SQLite
RUN mkdir -p /app/data

EXPOSE 8000
CMD ["gunicorn", "monprojet.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "2"]