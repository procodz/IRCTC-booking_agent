import http.client
import json
from geopy.distance import geodesic as distance
import requests

# Ollama API endpoint
OLLAMA_API_URL = "http://localhost:11434/api/generate"

# Dummy Flask API base URL
API_BASE_URL = "http://localhost:5000"  # Ensure the URL is correct


# Function to fetch railway stations using the dummy API
def fetch_railway_stations(query):
    conn = http.client.HTTPConnection(API_BASE_URL.split("://")[-1])
    try:
        conn.request("GET", f"/api/v1/searchStation?query={query}")
        res = conn.getresponse()
        
        if res.status != 200:
            print(f"API Error: {res.status} - {res.reason}")
            return None

        data = res.read()
        response_json = json.loads(data.decode("utf-8"))
        return response_json.get("data", [])
    except Exception as e:
        print(f"Error fetching railway stations: {e}")
        return None


# Function to calculate distance between coordinates
def calculate_distance(coord1, coord2):
    return distance(coord1, coord2).km


# Function to create a cluster of nearby railway stations
def create_station_cluster(user_location, stations, max_travel_time_hours=2, avg_speed_kmh=30):
    max_distance_km = max_travel_time_hours * avg_speed_kmh
    nearby_stations = []

    for station in stations:
        station_coords = (station["latitude"], station["longitude"])
        dist = calculate_distance(user_location, station_coords)
        if dist <= max_distance_km:
            nearby_stations.append({
                "name": station["name"],
                "code": station["code"],
                "distance_km": dist,
            })

    return nearby_stations


# Function to interact with Ollama for decision-making
def consult_ollama(user_query, context):
    prompt = f"""
    You are a smart railway booking assistant. The user's query is "{user_query}". 

    Here is the context:
    - Nearby Stations: {context['nearby_stations']}
    - User Location: {context['user_location']}
    - User Preferences: {context['preferences']}

    Suggest the best railway station for the user and provide a detailed explanation based on distance, convenience, and user preferences.
    """
    try:
        headers = {
            "Content-Type": "application/json"
        }
        data = {
            "model": "qwen2.5:3b",  # Use the Qwen2.5:3b model
            "prompt": prompt,
            "stream": False
        }
        response = requests.post(OLLAMA_API_URL, headers=headers, json=data)
        response.raise_for_status()
        response_json = response.json()
        return response_json.get("response", "Sorry, I couldn't fetch a recommendation right now.")
    except Exception as e:
        print(f"Error communicating with Ollama: {e}")
        return "Sorry, I couldn't fetch a recommendation right now."


# Function to get user preferences
def get_user_preferences():
    print("Please enter your preferences (e.g., 'I want the nearest station', 'I prefer fewer transfers'): ")
    preferences = input("> ")
    return preferences


# Main function to execute the full agent functionality
def agent_1_functionality():
    # User's mock location (New Delhi)
    user_location = (28.6139, 77.2090)
    print(f"User's Location: {user_location}")

    # Fetch railway stations
    query = "DELHI"
    stations_data = fetch_railway_stations(query)

    if not stations_data:
        print("Failed to fetch railway stations.")
        return

    # Create a cluster of nearby stations
    nearby_stations = create_station_cluster(user_location, stations_data)
    if not nearby_stations:
        print("No nearby stations found within a 2-hour travel radius.")
        return

    print("\nNearby Railway Stations:")
    for station in nearby_stations:
        print(f"{station['name']} ({station['code']}): {station['distance_km']:.2f} km away")

    # Get user preferences
    user_preferences = get_user_preferences()

    # Consult the Ollama for decision-making
    user_query = f"Find me the best station based on my preferences: {user_preferences}"
    context = {
        "nearby_stations": nearby_stations,
        "user_location": user_location,
        "preferences": user_preferences,
    }

    ollama_recommendation = consult_ollama(user_query, context)
    print("\nOllama Recommendation:")
    print(ollama_recommendation)


# Run the agent
if __name__ == "__main__":
    agent_1_functionality()