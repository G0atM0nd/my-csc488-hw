import os
import xml.etree.ElementTree as ET
import logging
from typing import Dict, Any, Tuple

def load_positional_data(file_path: str) -> Dict[str, Any]:
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
        # You would update this logic based on the actual structure of your positional XML file.
        # For now, we'll use a placeholder.
        return {"2025-03-26T12:00:00Z": {"latitude": 0.0, "longitude": 0.0, "altitude": 408}}
    except Exception as e:
        logging.error(f"Error parsing positional XML: {e}")
        return {}

def load_sighting_data(file_path: str) -> Dict[str, Any]:
    data = {}
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
        # Iterate over each <visible_pass> element in the XML.
        for vp in root.findall('visible_pass'):
            # Extract fields, using "Unknown" or empty string as fallback.
            country = vp.find('country').text.strip() if vp.find('country') is not None else "Unknown"
            region = vp.find('region').text.strip() if vp.find('region') is not None else "Unknown"
            city = vp.find('city').text.strip() if vp.find('city') is not None else "Unknown"
            
            sighting_info = {
                "spacecraft": vp.find('spacecraft').text.strip() if vp.find('spacecraft') is not None else "",
                "sighting_date": vp.find('sighting_date').text.strip() if vp.find('sighting_date') is not None else "",
                "duration_minutes": vp.find('duration_minutes').text.strip() if vp.find('duration_minutes') is not None else "",
                "max_elevation": vp.find('max_elevation').text.strip() if vp.find('max_elevation') is not None else "",
                "enters": vp.find('enters').text.strip() if vp.find('enters') is not None else "",
                "exits": vp.find('exits').text.strip() if vp.find('exits') is not None else "",
                "utc_offset": vp.find('utc_offset').text.strip() if vp.find('utc_offset') is not None else "",
                "utc_time": vp.find('utc_time').text.strip() if vp.find('utc_time') is not None else "",
                "utc_date": vp.find('utc_date').text.strip() if vp.find('utc_date') is not None else ""
            }
            
            # Organize data hierarchically: country > region > city.
            if country not in data:
                data[country] = {}
            if region not in data[country]:
                data[country][region] = {}
            if city not in data[country][region]:
                data[country][region][city] = []
            data[country][region][city].append(sighting_info)
        
        return data
    except Exception as e:
        logging.error(f"Error parsing sighting XML: {e}")
        return {}

def load_data(positional_file_path: str, sighting_file_path: str) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    return load_positional_data(positional_file_path), load_sighting_data(sighting_file_path)
