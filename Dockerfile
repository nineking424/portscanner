# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1  # Prevents Python from writing pyc files to disk
ENV PYTHONUNBUFFERED 1         # Ensures logs are output immediately

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the current directory contents into the container
COPY src/* .

# Create a non-root user and switch to it
RUN useradd -m nonrootuser
USER nonrootuser

# Open the ports required for your application (default to a range if needed)
EXPOSE 8080 8000-8005

# Run the application using a specific entrypoint
ENTRYPOINT ["python", "portlistener.py"]
CMD ["8080,8000-8005"]