from flask import Blueprint, request, jsonify, abort
from backend.services import create_booking_service, list_bookings_service

bookings_bp = Blueprint("bookings", __name__)

@bookings_bp.route("/bookings", methods=["POST"])
def create_booking():
    data = request.get_json() or {}

    room_id = data.get("room_id")
    start_time = data.get("start_time")
    end_time = data.get("end_time")

    if not room_id:
        abort(400, description="Room ID is required")

    if not start_time or not end_time:
        abort(400, description="Start and end time are required")

    booking, error = create_booking_service(room_id, start_time, end_time)
    if error:
        message, code = error
        abort(code, description=message)

    return jsonify({
        "data": {
            "message": "Booking created",
            "booking": {
                "id": booking.id,
                "room_id": booking.room_id,
                "start_time": booking.start_time,
                "end_time": booking.end_time
            }
        },
        "error": None
    }), 201


@bookings_bp.route("/bookings", methods=["GET"])
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

    return jsonify({
        "data": result,
        "error": None
    }), 200
