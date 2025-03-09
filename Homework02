import random
import json

def generate_meteorite_sites(num_sites=5):
    compositions = ["stony", "iron", "stony-iron"]
    sites = []
    
    for i in range(1, num_sites + 1):
        site = {
            "site_id": i,
            "latitude": round(random.uniform(16.0, 18.0), 6),
            "longitude": round(random.uniform(82.0, 84.0), 6),
            "composition": random.choice(compositions)
        }
        sites.append(site)
    
    return {"sites": sites}

def save_to_json(data, filename="meteorite_sites.json"):
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)

if __name__ == "__main__":
    meteorite_data = generate_meteorite_sites()
    save_to_json(meteorite_data)
    print(f"Meteorite landing sites data saved to meteorite_sites.json")
