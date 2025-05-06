#!/bin/bash

if [[ "${1}" == "celery" ]]; then
  echo "Starting Celery worker..."
  celery -A tasks.celery worker --loglevel=info
elif [[ "${1}" == "flower" ]]; then
  echo "Starting Flower..."
  celery -A tasks.celery flower
fi