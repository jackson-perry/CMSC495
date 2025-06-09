# Use official Python image
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Copy files
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your app
COPY . /app/

# Expose port (Gunicorn will run on this port)
EXPOSE 8080

# Start Gunicorn server
CMD ["gunicorn", "-w", "1", "-b", "0.0.0.0:8080", "app:create_app()"]
