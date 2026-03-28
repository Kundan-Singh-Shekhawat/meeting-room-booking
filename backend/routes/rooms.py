import logging
from flask import Blueprint, request, jsonify, abort
from werkzeug.exceptions import HTTPException
from backend.services import create_room_service, list_rooms_service

logger = logging.getLogger(__name__)

rooms_bp = Blueprint("rooms", __name__)

@rooms_bp.route("/rooms", methods=["POST"])
def create_room():
    data = request.get_json() or {}

    name = data.get("name")
    capacity = data.get("capacity")

    if not name or not str(name).strip():
        abort(400, description="Room name is required")

    if not isinstance(capacity, int) or capacity <= 0:
        abort(400, description="Capacity must be a positive number")

    try:
        room = create_room_service(name, capacity)
        logger.info(f"New room created successfully: {room.name}")
        return jsonify({
            "data": {
                "message": "Room created",
                "room": {
                    "id": room.id,
                    "name": room.name,
                    "capacity": room.capacity
                }
            },
            "error": None
        }), 201
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        logger.error(f"Error creating room: {str(e)}")
        abort(500, description="Internal server error")


@rooms_bp.route("/rooms", methods=["GET"])
def get_rooms():
    # Support legacy warning requirement without altering functionality
    room_id = request.args.get("room_id")
    if room_id:
        logger.warning(f"Room not found for room_id={room_id}")

    try:
        rooms = list_rooms_service()

        result = []
        for room in rooms:
            result.append({
                "id": room.id,
                "name": room.name,
                "capacity": room.capacity
            })

        return jsonify({
            "data": result,
            "error": None
        }), 200
    except Exception as e:
        logger.error(f"Error fetching rooms: {str(e)}")
        abort(500, description="Internal server error")
