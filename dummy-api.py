from flask import Flask, jsonify, request

app = Flask(__name__)

# Mock data for railway stations
MOCK_STATIONS = [
    {"name": "NEW DELHI", "code": "NDLS", "latitude": 28.6421, "longitude": 77.2207},
    {"name": "OLD DELHI", "code": "DLI", "latitude": 28.6619, "longitude": 77.2273},
    {"name": "DELHI CANTT", "code": "DEC", "latitude": 28.5800, "longitude": 77.3300},
    {"name": "DELHI SARAI ROHILLA", "code": "DEE", "latitude": 28.6700, "longitude": 77.2000},
    {"name": "DELHI SHAHDARA", "code": "DSA", "latitude": 28.6700, "longitude": 77.3000},
]

# Mock data for trains
MOCK_TRAINS = [
    {"train_number": "12001", "name": "SHATABDI EXP", "origin": "NDLS", "destination": "CNB", "departure": "06:00", "arrival": "12:00"},
    {"train_number": "12002", "name": "SHATABDI EXP", "origin": "CNB", "destination": "NDLS", "departure": "14:00", "arrival": "20:00"},
    {"train_number": "14011", "name": "JANSHATABDI EXP", "origin": "NDLS", "destination": "JUC", "departure": "15:00", "arrival": "21:00"},
]

# Mock data for seat availability
MOCK_SEAT_AVAILABILITY = [
    {"train_number": "12001", "date": "2023-11-01", "class": "AC", "seats_available": 10},
    {"train_number": "12001", "date": "2023-11-01", "class": "Sleeper", "seats_available": 50},
    {"train_number": "12002", "date": "2023-11-01", "class": "AC", "seats_available": 5},
    {"train_number": "12002", "date": "2023-11-01", "class": "Sleeper", "seats_available": 30},
]

# Mock data for train routes
MOCK_TRAIN_ROUTES = {
    "12001": [
        {"station_code": "NDLS", "arrival": "06:00", "departure": "06:15"},
        {"station_code": "GZB", "arrival": "06:45", "departure": "06:50"},
        {"station_code": "CNB", "arrival": "12:00", "departure": None},
    ],
    "12002": [
        {"station_code": "CNB", "arrival": "14:00", "departure": "14:15"},
        {"station_code": "GZB", "arrival": "19:45", "departure": "19:50"},
        {"station_code": "NDLS", "arrival": "20:00", "departure": None},
    ],
}

# Mock data for train prices
MOCK_TRAIN_PRICES = [
    {"train_number": "12001", "class": "AC", "price": 1500},
    {"train_number": "12001", "class": "Sleeper", "price": 800},
    {"train_number": "12002", "class": "AC", "price": 1500},
    {"train_number": "12002", "class": "Sleeper", "price": 800},
    {"train_number": "14011", "class": "AC", "price": 1200},
    {"train_number": "14011", "class": "Sleeper", "price": 700},
]

@app.route("/api/v1/searchStation", methods=["GET"])
def search_station():
    query = request.args.get("query", "").upper()
    filtered_stations = [station for station in MOCK_STATIONS if query in station["name"]]
    return jsonify({"status": True, "message": "Success", "data": filtered_stations})

@app.route("/api/v1/trainSchedule", methods=["GET"])
def train_schedule():
    origin = request.args.get("origin", "").upper()
    destination = request.args.get("destination", "").upper()
    filtered_trains = [train for train in MOCK_TRAINS if train["origin"] == origin and train["destination"] == destination]
    return jsonify({"status": True, "message": "Success", "data": filtered_trains})

@app.route("/api/v1/seatAvailability", methods=["GET"])
def seat_availability():
    train_number = request.args.get("train_number", "")
    date = request.args.get("date", "")
    filtered_seats = [seat for seat in MOCK_SEAT_AVAILABILITY if seat["train_number"] == train_number and seat["date"] == date]
    return jsonify({"status": True, "message": "Success", "data": filtered_seats})

@app.route("/api/v1/trainRoute", methods=["GET"])
def train_route():
    train_number = request.args.get("train_number", "")
    route = MOCK_TRAIN_ROUTES.get(train_number, [])
    return jsonify({"status": True, "message": "Success", "data": route})

@app.route("/api/v1/trainDetails", methods=["GET"])
def train_details():
    train_number = request.args.get("train_number", "")
    train = next((train for train in MOCK_TRAINS if train["train_number"] == train_number), None)
    return jsonify({"status": True, "message": "Success", "data": train})

@app.route("/api/v1/trainPrice", methods=["GET"])
def train_price():
    train_number = request.args.get("train_number", "")
    train_class = request.args.get("class", "")
    price = next((price for price in MOCK_TRAIN_PRICES if price["train_number"] == train_number and price["class"] == train_class), None)
    return jsonify({"status": True, "message": "Success", "data": price})

if __name__ == "__main__":
    print("Starting Flask server...")
    app.run(debug=True)