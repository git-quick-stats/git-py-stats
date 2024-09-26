# Use the official Python image as the base image
# and setup the env vars necessary
FROM python:3.9-slim
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Set the working directory inside the container
WORKDIR /app

# Install git as it's our only dep
RUN apt-get update && apt-get install -y git && apt-get clean

# Copy the requirements and configuration files first for caching
COPY pyproject.toml setup.py MANIFEST.in ./

# Install build dependencies and the project in editable mode
RUN pip install --upgrade pip setuptools
RUN pip install -e .

# Copy the rest of the stuff
COPY . .

# Initialize a basic git repo
RUN git init && \
    git config user.name "Docker" && \
    git config user.email "docker@example.com" && \
    git add . && \
    git commit -m "Initial commit" || echo "Already a git repository"

# NOTE: Should we add dummy commits?
#       Thought - we can dogfood and clone the git-py-stats repo inside here

# Command to run the CLI tool with help option
CMD ["git-py-stats", "--help"]

