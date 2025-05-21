# -*- Dockerfile -*-
# Author: Shibo Li
# Date: 2025-05-21

FROM python:3.11-slim

# Environment
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy project code
COPY . .

# Inform Docker that this container exposes port 9000
EXPOSE 9000

# Default command (run FastAPI app)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "9000"]
