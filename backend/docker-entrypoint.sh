#!/bin/sh
# Démarre Gunicorn (workers Uvicorn) en HTTP (Kubernetes : TLS terminé à l'Ingress).
set -e
exec runuser -u fastapi -- /usr/local/bin/gunicorn \
  -c /app/gunicorn_conf.py \
  app.main:application
