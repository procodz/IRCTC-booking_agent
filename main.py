import http.client
import json
import geopy.distance
from geopy.geocoders import Nominatim
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Function to fetch railway stations using the IRCTC API
def fetch_railway_stations(query):
    conn = http.client.HTTPSConnection("irctc1.p.rapidapi.com")
    headers = {
        'x-rapidapi-key': os.getenv('x-rapidapi-key'),
        'x-rapidapi-host': "irctc1.p.rapidapi.com"
    }
    try:
        conn.request("GET", f"/api/v1/searchStation?query={query}", headers=headers)
        res = conn.getresponse()
        data = res.read()
        response_data = json.loads(data.decode("utf-8"))
        
        if response_data.get("status") and response_data.get("data"):
            # Extract stations from the nested structure
            stations = []
            for item in response_data["data"]:
                if isinstance(item, dict) and "name" in item:
                    stations.append({
                        "stationName": item["name"],
                        "stationCode": item.get("code", "N/A"),
                        "state": item.get("state_name", "N/A")
                    })
            return stations
        return []
    except Exception as e:
        print(f"Error fetching railway stations: {e}")
        return []
    finally:
        conn.close()

# Function to fetch user's location using geocoding
def get_user_location():
    geolocator = Nominatim(user_agent="smart_irctc_agent")
    location = geolocator.geocode("New Delhi")  # Replace with dynamic input in real use case
    return (location.latitude, location.longitude)

# Function to calculate distance between two coordinates
def calculate_distance(coord1, coord2):
    return geopy.distance.distance(coord1, coord2).km

# Main function to execute the functionality
def main():
    # Step 1: Fetch user's location
    user_location = get_user_location()
    print(f"User's Location: {user_location}")

    # Step 2: Fetch railway stations near the user's location using the IRCTC API
    query = "Delhi"  # Replace with dynamic input based on user's location
    stations_data = fetch_railway_stations(query)

    if not stations_data:
        print("No stations found. Please try a different search query.")
        return

    print("\nFound Railway Stations:")
    for station in stations_data:
        print(f"Station: {station['stationName']} ({station['stationCode']}) - {station['state']}")

if __name__ == "__main__":
    main()