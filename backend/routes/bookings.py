import logging
from flask import Blueprint, request, jsonify, abort
from werkzeug.exceptions import HTTPException
from backend.services import create_booking_service, list_bookings_service

logger = logging.getLogger(__name__)

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

    try:
        booking, error = create_booking_service(room_id, start_time, end_time)
        if error:
            message, code = error
            if code == 409:
                logger.warning(f"Conflict detected for room_id={room_id} at {start_time}-{end_time}")
            elif code == 404:
                logger.warning(f"Room not found for room_id={room_id}")
            abort(code, description=message)

        logger.info(f"Booking successfully created for room_id={room_id} from {start_time} to {end_time}")
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
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        logger.error(f"Error processing booking: {str(e)}")
        abort(500, description="Internal server error")


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
