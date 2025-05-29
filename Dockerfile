# Use official Python image
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    FLASK_ENV=production \
    port=8080

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
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8080", "--access-logfile", "-", "--error-logfile", "-",  "app:app"]
