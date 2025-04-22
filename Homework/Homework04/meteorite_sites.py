import argparse
import json

# Create argument parser to accept the JSON file as a command-line argument
parser = argparse.ArgumentParser(description='Analyze Meteorite Landing Data')
parser.add_argument('json_file', help='Path to the meteorite landing data JSON file')
args = parser.parse_args()

# Load the data from the provided file
with open(args.json_file) as f:
    data = json.load(f)

# Initialize counters for each quadrant
northern_eastern = 0
northern_western = 0
southern_eastern = 0
southern_western = 0

# Iterate through the meteor data and classify based on latitude and longitude
for meteor in data['meteors']:
    lat = meteor['location']['latitude']
    lon = meteor['location']['longitude']
    
    # Determine quadrant and update counters
    if lat > 0 and lon > 0:
        northern_eastern += 1
    elif lat > 0 and lon < 0:
        northern_western += 1
    elif lat < 0 and lon > 0:
        southern_eastern += 1
    else:
        southern_western += 1

# Print summary data with some nice formatting
print("\n" + "="*50)
print("Summary Data Following Meteorite Analysis:")
print("="*50)
print(f"\nHemisphere summary data:\n")
print(f" - Northern & Eastern: {northern_eastern} meteors")
print(f" - Northern & Western: {northern_western} meteors")
print(f" - Southern & Eastern: {southern_eastern} meteors")
print(f" - Southern & Western: {southern_western} meteors")
print("="*50)
