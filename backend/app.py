from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import request, jsonify
import logging

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)


app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    capacity = db.Column(db.Integer, nullable=False)


class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'), nullable=False)
    start_time = db.Column(db.String(50), nullable=False)
    end_time = db.Column(db.String(50), nullable=False)


# --- Simple service helpers (rookie-friendly separation) ---

def create_room_service(name, capacity):
    room = Room(name=name, capacity=capacity)
    db.session.add(room)
    db.session.commit()
    logging.info(f"Room created with id={room.id}")
    return room

def list_rooms_service():
    return Room.query.all()

def create_booking_service(room_id, start_time, end_time):
    
    logging.info(f"Creating booking for room {room_id} from {start_time} to {end_time}")
    # Check if room exists
    room = Room.query.get(room_id)
    if not room:
        return None, ("Room not found", 404)

    # Validate time order
    if start_time >= end_time:
        return None, ("Start time must be before end time", 400)

    # Basic time format check (HH:MM)
    if len(start_time) != 5 or len(end_time) != 5:
        return None, ("Invalid time format. Use HH:MM", 400)


    # Conflict detection
    existing_bookings = Booking.query.filter_by(room_id=room_id).all()
    for b in existing_bookings:
        if not (end_time <= b.start_time or start_time >= b.end_time):
            logging.warning(f"Conflict detected for room {room_id} at {start_time}-{end_time}")
            return None, ("Time slot already booked", 400)

    booking = Booking(
        room_id=room_id,
        start_time=start_time,
        end_time=end_time
    )
    db.session.add(booking)
    db.session.commit()
    return booking, None

def list_bookings_service():
    return Booking.query.all()

@app.route("/")
def home():
    return {"message": "API is running"}
@app.route("/rooms", methods=["POST"])
def create_room():
    data = request.get_json() or {}

    name = data.get("name")
    capacity = data.get("capacity")

    if not name or not name.strip():
        return jsonify({"error": "Room name is required"}), 400

    if not isinstance(capacity, int) or capacity <= 0:
        return jsonify({"error": "Capacity must be a positive number"}), 400

    room = create_room_service(name, capacity)

    return jsonify({"message": "Room created"}), 201


@app.route("/rooms", methods=["GET"])
def get_rooms():
    rooms = list_rooms_service()

    result = []
    for room in rooms:
        result.append({
            "id": room.id,
            "name": room.name,
            "capacity": room.capacity
        })

    return jsonify(result)

@app.route("/bookings", methods=["POST"])
def create_booking():
    data = request.get_json() or {}

    room_id = data.get("room_id")
    start_time = data.get("start_time")
    end_time = data.get("end_time")

    if not room_id:
        return jsonify({"error": "Room ID is required"}), 400

    if not start_time or not end_time:
        return jsonify({"error": "Start and end time are required"}), 400

    booking, error = create_booking_service(room_id, start_time, end_time)
    if error:
        message, code = error
        return jsonify({"error": message}), code

    return jsonify({"message": "Booking created"}), 201

@app.route("/bookings", methods=["GET"])
def get_bookings():
    bookings = list_bookings_service()

    result = []
    for b in bookings:
        result.append({
            "id": b.id,
            "room_id": b.room_id,
            "start_time": b.start_time,
            "end_time": b.end_time
        })

    return jsonify(result)

with app.app_context():
    db.create_all()
if __name__ == "__main__":
    app.run(debug=True)
