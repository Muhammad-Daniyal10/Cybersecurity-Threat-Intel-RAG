# Use an official, lightweight Python 3.12 image
FROM python:3.12-slim

# Set the working directory inside the container
WORKDIR /app

# Install system dependencies (build tools and poppler for PDF processing)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    poppler-utils \
    tesseract-ocr \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .

# Force the lightweight CPU-only version of PyTorch first
RUN pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu

# Install the rest of the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application files
COPY . .

# Expose port 8000
EXPOSE 8000

# Start Uvicorn bound to 0.0.0.0
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]