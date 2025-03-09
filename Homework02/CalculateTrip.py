import json
import math

def great_circle_distance(lat1, lon1, lat2, lon2, radius=3389.5):
    def to_radians(degrees):
        return degrees * (math.pi / 180)
    
    lat1, lon1, lat2, lon2 = map(to_radians, [lat1, lon1, lat2, lon2])
    
    delta_lat = lat2 - lat1
    delta_lon = lon2 - lon1
    
    a = math.sin(delta_lat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(delta_lon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    return radius * c

def calculate_travel_time(data, speed=10):
    start_lat, start_lon = 16.0, 82.0
    total_time = 0
    num_legs = 0
    
    sampling_times = {"stony": 1, "iron": 2, "stony-iron": 3}
    
    print("Mars Exploration Travel Log")
    print("===========================")
    
    for site in data["sites"]:
        num_legs += 1
        distance = great_circle_distance(start_lat, start_lon, site["latitude"], site["longitude"])
        travel_time = distance / speed
        sample_time = sampling_times[site["composition"]]
        total_time += travel_time + sample_time
        
        print(f"leg = {num_legs}, time to travel = {travel_time:.2f} hr, time to sample = {sample_time} hr")
        
        start_lat, start_lon = site["latitude"], site["longitude"]
    
    print("===============================")
    print(f"number of legs = {num_legs}, total time elapsed = {total_time:.2f} hr")

if __name__ == "__main__":
    with open("meteorite_sites.json", "r") as f:
        meteorite_data = json.load(f)
    
    calculate_travel_time(meteorite_data)
