# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Install Node.js for the filesystem server
RUN apt-get update && apt-get install -y curl && \
    curl -fsSL https://deb.nodesource.com/setup_16.x | bash - && \
    apt-get install -y nodejs

# Install TypeScript and other dependencies for the filesystem server
RUN npm install -g typescript && \
    cd enterprise_mcp_mvp_demo/mcp_servers/filesystem && \
    npm install && \
    npm run build

# Expose the port the app runs on
EXPOSE 8000

# Define environment variable
ENV PYTHONUNBUFFERED=1

# Set the working directory to enterprise_mcp_mvp_demo
WORKDIR /app/enterprise_mcp_mvp_demo

# Run the FastAPI app
CMD ["python", "main.py"]