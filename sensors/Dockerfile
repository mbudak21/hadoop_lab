# Use an official lightweight Python image.
FROM python:3.9-slim

# Set the working directory.
WORKDIR /app

# Copy sensor.py and requirements.txt into the container.
COPY sensor.py requirements.txt ./

# Install required Python packages.
RUN pip install --no-cache-dir -r requirements.txt

# Default command uses the config.env file that will be mounted.
CMD ["python", "sensor.py", "config.env"]

