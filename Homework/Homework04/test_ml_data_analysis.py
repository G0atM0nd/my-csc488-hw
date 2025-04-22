import pytest
import json
from meteorite_sites import *  # Import functions from the main script

# Example test cases for meteorite analysis

def test_northern_eastern():
    test_data = {
        "meteors": [
            {"location": {"latitude": 34.0, "longitude": -118.0}},
            {"location": {"latitude": 40.0, "longitude": -75.0}},
        ]
    }
    # Mock the data loading process
    data = test_data
    northern_eastern = 0
    for meteor in data['meteors']:
        lat = meteor['location']['latitude']
        lon = meteor['location']['longitude']
        if lat > 0 and lon > 0:
            northern_eastern += 1

    assert northern_eastern == 1  # Expecting 1 meteor in Northern & Eastern quadrant

def test_northern_western():
    test_data = {
        "meteors": [
            {"location": {"latitude": 34.0, "longitude": -118.0}},
        ]
    }
    data = test_data
    northern_western = 0
    for meteor in data['meteors']:
        lat = meteor['location']['latitude']
        lon = meteor['location']['longitude']
        if lat > 0 and lon < 0:
            northern_western += 1

    assert northern_western == 1  # Expecting 1 meteor in Northern & Western quadrant

def test_southern_eastern():
    test_data = {
        "meteors": [
            {"location": {"latitude": -33.0, "longitude": 151.0}},
        ]
    }
    data = test_data
    southern_eastern = 0
    for meteor in data['meteors']:
        lat = meteor['location']['latitude']
        lon = meteor['location']['longitude']
        if lat < 0 and lon > 0:
            southern_eastern += 1

    assert southern_eastern == 1  # Expecting 1 meteor in Southern & Eastern quadrant

def test_southern_western():
    test_data = {
        "meteors": [
            {"location": {"latitude": -45.0, "longitude": -75.0}},
        ]
    }
    data = test_data
    southern_western = 0
    for meteor in data['meteors']:
        lat = meteor['location']['latitude']
        lon = meteor['location']['longitude']
        if lat < 0 and lon < 0:
            southern_western += 1

    assert southern_western == 1  # Expecting 1 meteor in Southern & Western quadrant

# Add more tests as needed to validate your logic
