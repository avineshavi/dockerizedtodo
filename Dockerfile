# Use an official Python runtime as the base image
FROM python:3.9

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /todo

# Install dependencies
COPY requirement.txt /todo/
RUN pip install -r requirement.txt

# Copy the Django project todo into the container
COPY . /todo/

# Expose the port that Django runs on
EXPOSE 8000

# Set the command to start the Django development server
# CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
