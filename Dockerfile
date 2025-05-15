FROM python:3.13

# Set the working directory
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

ENTRYPOINT [ "fastapi", "run", "--host", "0.0.0.0", "--port", "8000", "--reload" ]