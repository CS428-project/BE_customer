# Pull a base image. This example uses Python 3.9, but you can choose an appropriate one.
FROM python:3.9

# Set environment variables.
# Ensure that Python output is sent straight to terminal without being buffered.
ENV PYTHONUNBUFFERED=1

# Create a directory for your application.
WORKDIR /app

COPY install.sh .
RUN sh install.sh

# Copy requirements.txt file (if you have one) into the docker image.
COPY requirements.txt .

# Install dependencies.
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the code into the image.
COPY . .

# Expose the port that your app runs on. FastAPI typically runs on port 8000.
EXPOSE 8000

# Use the uvicorn server to serve the app. 
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
