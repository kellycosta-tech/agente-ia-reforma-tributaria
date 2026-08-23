FROM python:3.13-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY app ./app
COPY ingestion ./ingestion
COPY vectorstore ./vectorstore
COPY data/vector_store ./data/vector_store
COPY catalog ./catalog
COPY evaluation ./evaluation
COPY scripts ./scripts
COPY docs ./docs

EXPOSE 8501

CMD ["streamlit", "run", "app/main.py", "--server.address=0.0.0.0", "--server.port=8501"]