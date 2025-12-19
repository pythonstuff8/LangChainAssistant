FROM python:3.11-slim

WORKDIR /app

# Install system dependencies (build-essential for some python packages)
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Expose port 3005
EXPOSE 3005

# Run the application
CMD ["python", "main.py"]
