from flask import Flask, request, Response
import os
import logging
from typing import Any
from data_loader import load_data  # Import our XML parsing functions
import requests 

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

# Global variables to hold the parsed data.
positional_data = {}
sighting_data = {}

# Directory where your local XML files are stored.
DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')

def to_xml(data, root_tag='response'):
    """
    Recursively converts a Python dict or list to an XML string.
    """
    import xml.etree.ElementTree as ET
    root = ET.Element(root_tag)
    
    def build_xml(elem, value):
        if isinstance(value, dict):
            for k, v in value.items():
                child = ET.SubElement(elem, k)
                build_xml(child, v)
        elif isinstance(value, list):
            for item in value:
                item_elem = ET.SubElement(elem, 'item')
                build_xml(item_elem, item)
        else:
            elem.text = str(value)
    
    build_xml(root, data)
    return ET.tostring(root, encoding='unicode')

@app.route("/", methods=["GET"])
def index() -> Response:
    logging.info("Index route queried")
    text = (
        "Welcome to the ISS Tracking API.\n\n"
        "Available endpoints:\n"
        "GET /epochs - Get all epochs from positional data.\n"
        "GET /epochs/<epoch> - Get details for a specific epoch.\n"
        "GET /countries - Get all countries from sighting data.\n"
        "GET /countries/<country> - Get details for a specific country.\n"
        "GET /countries/<country>/regions - Get regions for a given country.\n"
        "GET /countries/<country>/regions/<region> - Get details for a specific region.\n"
        "GET /countries/<country>/regions/<region>/cities - Get cities for a specific country and region.\n"
        "GET /countries/<country>/regions/<region>/cities/<city> - Get details for a specific city.\n"
        "POST /load-data - Load ISS positional and sighting data from XML files.\n"
    )
    return Response(text, mimetype="text/plain")

@app.route("/load-data", methods=["POST"])
def load_data_endpoint() -> Response:
    logging.info("POST /load-data route queried")
    try:
        positional_file = request.files.get('positional_file')
        sighting_file = request.files.get('sighting_file')

        # For positional data, use XMLsightingData_citiesUSA05.xml if not provided.
        if not positional_file:
            positional_file_path = os.path.join(DATA_DIR, 'XMLsightingData_citiesUSA05.xml')
        else:
            positional_file_path = os.path.join(DATA_DIR, 'uploaded_positional.xml')
            positional_file.save(positional_file_path)

        # For sighting data, also use XMLsightingData_citiesUSA05.xml if not provided.
        if not sighting_file:
            sighting_file_path = os.path.join(DATA_DIR, 'XMLsightingData_citiesUSA05.xml')
        else:
            sighting_file_path = os.path.join(DATA_DIR, 'uploaded_sighting.xml')
            sighting_file.save(sighting_file_path)

        global positional_data, sighting_data
        positional_data, sighting_data = load_data(positional_file_path, sighting_file_path)
        xml_response = to_xml({"message": "Data loaded successfully"})
        return Response(xml_response, mimetype="application/xml"), 200
    except Exception as e:
        logging.error(f"Error loading data: {e}")
        xml_response = to_xml({"error": "Failed to load data"})
        return Response(xml_response, mimetype="application/xml"), 500




@app.route("/epochs", methods=["GET"])
def get_epochs() -> Response:
    logging.info("GET /epochs route queried")
    if not positional_data:
        xml_response = to_xml({"error": "No positional data loaded"})
        return Response(xml_response, mimetype="application/xml"), 404
    epochs = list(positional_data.keys())
    xml_response = to_xml({"epochs": epochs})
    return Response(xml_response, mimetype="application/xml")

@app.route("/epochs/<epoch>", methods=["GET"])
def get_epoch(epoch: str) -> Response:
    logging.info(f"GET /epochs/{epoch} route queried")
    if epoch not in positional_data:
        xml_response = to_xml({"error": "Epoch not found"})
        return Response(xml_response, mimetype="application/xml"), 404
    xml_response = to_xml(positional_data[epoch], root_tag="epoch")
    return Response(xml_response, mimetype="application/xml")

@app.route("/countries", methods=["GET"])
def get_countries() -> Response:
    logging.info("GET /countries route queried")
    if not sighting_data:
        xml_response = to_xml({"error": "No sighting data loaded"})
        return Response(xml_response, mimetype="application/xml"), 404
    countries = list(sighting_data.keys())
    xml_response = to_xml({"countries": countries})
    return Response(xml_response, mimetype="application/xml")

@app.route("/countries/<country>", methods=["GET"])
def get_country(country: str) -> Response:
    logging.info(f"GET /countries/{country} route queried")
    if country not in sighting_data:
        xml_response = to_xml({"error": "Country not found"})
        return Response(xml_response, mimetype="application/xml"), 404
    xml_response = to_xml(sighting_data[country], root_tag="country")
    return Response(xml_response, mimetype="application/xml")

@app.route("/countries/<country>/regions", methods=["GET"])
def get_regions(country: str) -> Response:
    logging.info(f"GET /countries/{country}/regions route queried")
    if country not in sighting_data:
        xml_response = to_xml({"error": "Country not found"})
        return Response(xml_response, mimetype="application/xml"), 404
    regions = list(sighting_data[country].keys())
    xml_response = to_xml({"regions": regions})
    return Response(xml_response, mimetype="application/xml")

@app.route("/countries/<country>/regions/<region>", methods=["GET"])
def get_region(country: str, region: str) -> Response:
    logging.info(f"GET /countries/{country}/regions/{region} route queried")
    if country not in sighting_data:
        xml_response = to_xml({"error": "Country not found"})
        return Response(xml_response, mimetype="application/xml"), 404
    if region not in sighting_data[country]:
        xml_response = to_xml({"error": "Region not found"})
        return Response(xml_response, mimetype="application/xml"), 404
    xml_response = to_xml(sighting_data[country][region], root_tag="region")
    return Response(xml_response, mimetype="application/xml")

@app.route("/countries/<country>/regions/<region>/cities", methods=["GET"])
def get_cities(country: str, region: str) -> Response:
    logging.info(f"GET /countries/{country}/regions/{region}/cities route queried")
    if country not in sighting_data:
        xml_response = to_xml({"error": "Country not found"})
        return Response(xml_response, mimetype="application/xml"), 404
    if region not in sighting_data[country]:
        xml_response = to_xml({"error": "Region not found"})
        return Response(xml_response, mimetype="application/xml"), 404
    cities = list(sighting_data[country][region].keys())
    xml_response = to_xml({"cities": cities})
    return Response(xml_response, mimetype="application/xml")

@app.route("/countries/<country>/regions/<region>/cities/<city>", methods=["GET"])
def get_city(country: str, region: str, city: str) -> Response:
    logging.info(f"GET /countries/{country}/regions/{region}/cities/{city} route queried")
    if country not in sighting_data:
        xml_response = to_xml({"error": "Country not found"})
        return Response(xml_response, mimetype="application/xml"), 404
    if region not in sighting_data[country]:
        xml_response = to_xml({"error": "Region not found"})
        return Response(xml_response, mimetype="application/xml"), 404
    if city not in sighting_data[country][region]:
        xml_response = to_xml({"error": "City not found"})
        return Response(xml_response, mimetype="application/xml"), 404
    xml_response = to_xml(sighting_data[country][region][city], root_tag="city")
    return Response(xml_response, mimetype="application/xml")

import requests  # make sure requests is installed

@app.route("/fetch-nasa-data", methods=["GET"])
def fetch_nasa_data() -> Response:
    # Replace this URL with the correct NASA API endpoint that returns XML.
    nasa_url = "https://data.nasa.gov/Space-Science/ISS_COORDS_2022-02-13/r6u8-bhhq"  
    try:
        nasa_response = requests.get(nasa_url)
        if nasa_response.status_code != 200:
            return Response(
                f"<error>Failed to fetch NASA data; status code: {nasa_response.status_code}</error>",
                mimetype="application/xml",
                status=nasa_response.status_code
            )
        
        xml_data = nasa_response.text
        
        # Define the file path to write the XML data
        file_path = os.path.join(DATA_DIR, "nasa_iss_data.xml")
        with open(file_path, "w") as f:
            f.write(xml_data)
        
        return Response(
            f"<message>NASA data fetched and written to {file_path}</message>",
            mimetype="application/xml",
            status=200
        )
    except Exception as e:
        logging.error(f"Error fetching NASA data: {e}")
        return Response(
            f"<error>Error fetching NASA data: {e}</error>",
            mimetype="application/xml",
            status=500
        )


if __name__ == "__main__":
    app.run(debug=True)
