FROM python:3.10.6-alpine

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app/

# Copy the project files to the working directory
COPY . .

# Create and activate virtualenv
RUN python -m venv venv
RUN . venv/bin/activate

# Install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expose the container's port (change this if your Django project uses a different port)
EXPOSE 8005
