FROM python:3.13-slim

WORKDIR /app

RUN pip install poetry

COPY . .

WORKDIR /app/isp_identity_store

RUN poetry install --no-root

# Run gunicorn
CMD ["poetry", "run", "./manage.py", "runserver", "0.0.0.0:8000"]