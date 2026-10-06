FROM python:3.12-slim

WORKDIR /app

COPY requirements-docker-backend.txt .

RUN pip install --no-cache-dir -r requirements-docker-backend.txt

COPY api ./api

COPY *.pkl ./

EXPOSE 8000

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]