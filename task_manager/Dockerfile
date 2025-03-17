# Use official Python image
FROM python:3.11

# Set the working directory inside the container
WORKDIR /app

# Copy requirements first (for caching dependencies)
COPY requirements.txt . 

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Now copy the rest of the project files
COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput

# Expose Django's default port
EXPOSE 8000

# Start Django server
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
