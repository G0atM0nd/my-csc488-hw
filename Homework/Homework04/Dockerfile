# Step 1: Use an official Python image from the Docker Hub
FROM python:3.9-slim

# Step 2: Set the working directory in the container
WORKDIR /app

# Step 3: Copy the current directory contents into the container at /app
COPY . /app

# Step 4: Install the required dependencies
# Create a requirements.txt file with the necessary Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Step 5: Run the test suite with pytest
RUN pytest --maxfail=1 --disable-warnings -q

# Step 6: Set the command to run the script when the container starts
CMD ["python", "meteorite_sites.py", "Meteorite_Landings.json"]
