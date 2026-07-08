FROM python:3.11-slim

# Faster, quieter, reproducible Python in containers.
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

# Install dependencies first so the layer is cached across code changes.
COPY requirements.txt .
# CPU-only torch: the default PyPI wheel drags in the full CUDA stack
# (~2GB of unused GPU libraries) for a model that only ever runs on CPU here.
RUN pip install --timeout 120 --retries 5 torch --index-url https://download.pytorch.org/whl/cpu \
    && pip install --timeout 120 --retries 5 -r requirements.txt

# Application code.
COPY app ./app

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
