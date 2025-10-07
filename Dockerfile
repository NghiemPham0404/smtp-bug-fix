FROM python:3.11-slim

WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY ./requirements.txt /app

RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the source code
COPY ./src /app/src

# Copy the templates files
COPY ./templates /app/templates

EXPOSE 8000

# Run service with 4 workers
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
