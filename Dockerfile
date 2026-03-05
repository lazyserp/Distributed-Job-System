# Use bullseye instead of slim for better compatibility
FROM python:3.9-bullseye

# The working directory
WORKDIR /app

# requirements 
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt


#Copy all code
COPY . .

# Run the image
CMD ["python", "worker.py"]