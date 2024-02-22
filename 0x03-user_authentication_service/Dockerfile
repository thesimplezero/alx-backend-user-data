# Use Ubuntu 18.04 as the base image
FROM ubuntu:18.04

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install required system packages
RUN apt-get update && \
    apt-get install -y python3 python3-pip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Upgrade pip
RUN pip3 install --no-cache-dir --upgrade pip

# Install Python packages
RUN pip3 install --no-cache-dir \
    certifi==2024.2.2 \
    chardet==3.0.4 \
    click==8.0.4 \
    Flask==1.1.2 \
    Flask-Cors==3.0.8 \
    idna==2.6 \
    itsdangerous \
    Jinja2==2.11.2 \
    MarkupSafe \
    pycodestyle==2.5 \
    requests \
    six \
    urllib3 \
    Werkzeug

# Define environment variable
ENV USERAUTH true

# Attach to bash environment
CMD ["/bin/bash"]
