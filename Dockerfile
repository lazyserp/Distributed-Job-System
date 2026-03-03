# CHANGE: Use bullseye instead of slim for better compatibility
FROM python:3.9-bullseye

WORKDIR /app

COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "worker.py"]