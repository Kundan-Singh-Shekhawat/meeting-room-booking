from flask import Blueprint, request, jsonify, abort
from backend.services import create_room_service, list_rooms_service

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

    room = create_room_service(name, capacity)

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


@rooms_bp.route("/rooms", methods=["GET"])
def get_rooms():
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
