# Start from a small official Python image
FROM python:3.12-slim

# Set the working folder inside the container
WORKDIR /app

# Copy the Python app into the container
COPY Damilola.Adegbuyi.py .

# Run the app when the container starts
CMD ["python", "Damilola.Adegbuyi.py"]
