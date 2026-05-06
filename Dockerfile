FROM python:3.13-slim

WORKDIR /app

RUN pip install gunicorn

COPY . .

RUN pip install ./isp_identity_store

# Run gunicorn
CMD ["gunicorn", "isp_identity_store.wsgi", "--bind", "0.0.0.0:8000"]