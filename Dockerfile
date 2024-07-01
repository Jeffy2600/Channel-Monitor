# Base image for your bot (replace with your specific Python version)
FROM python:3.8-slim

# Set the working directory within the container
WORKDIR /app

# Copy requirements.txt to install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy your bot code to the working directory
COPY . .

# Define the command to run your bot
CMD [ "python", "bot.py" ]
