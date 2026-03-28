import logging
from typing import List, Tuple, Optional
from backend.database import db
from backend.models import Room, Booking

logger = logging.getLogger(__name__)

def create_room_service(name: str, capacity: int) -> Room:
    """Create a new room and store it in the database."""
    room = Room(name=name, capacity=capacity)
    db.session.add(room)
    db.session.commit()
    logger.info(f"Room created with id={room.id}")
    return room

def list_rooms_service() -> List[Room]:
    """Retrieve all rooms from the database."""
    return Room.query.all()

def has_booking_conflict(room_id: int, start_time: str, end_time: str) -> bool:
    """Check if the requested time slot conflicts with existing bookings for the room."""
    existing_bookings = Booking.query.filter_by(room_id=room_id).all()
    for b in existing_bookings:
        # A conflict occurs if there is an overlap.
        # The two periods overlap if BOTH: start_time < b.end_time AND end_time > b.start_time
        # Or alternatively: NOT (new_end <= existing_start OR new_start >= existing_end)
        if not (end_time <= b.start_time or start_time >= b.end_time):
            return True
    return False

def create_booking_service(room_id: int, start_time: str, end_time: str) -> Tuple[Optional[Booking], Optional[Tuple[str, int]]]:
    """
    Attempt to create a new booking for a room.
    Returns (Booking, None) on success, or (None, (error_message, status_code)) on failure.
    """
    logger.info(f"Creating booking for room {room_id} from {start_time} to {end_time}")
    
    room = db.session.get(Room, room_id)
    if not room:
        return None, ("Room not found", 404)

    if start_time >= end_time:
        return None, ("Start time must be before end time", 400)

    if len(start_time) != 5 or len(end_time) != 5:
        return None, ("Invalid time format. Use HH:MM", 400)

    if has_booking_conflict(room_id, start_time, end_time):
        logger.warning(f"Conflict detected for room {room_id} at {start_time}-{end_time}")
        return None, ("Time slot already booked", 409)

    booking = Booking(
        room_id=room_id,
        start_time=start_time,
        end_time=end_time
    )
    db.session.add(booking)
    db.session.commit()
    return booking, None

def list_bookings_service() -> List[Booking]:
    """Retrieve all bookings from the database."""
    return Booking.query.all()
