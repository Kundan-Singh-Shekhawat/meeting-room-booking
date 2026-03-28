import pytest
from backend.services import (
    create_room_service,
    list_rooms_service,
    create_booking_service,
    list_bookings_service,
    has_booking_conflict
)
from backend.models import Room, Booking

def test_create_room_service(app_context):
    room = create_room_service("Boardroom", 10)
    assert room.id is not None
    assert room.name == "Boardroom"
    assert room.capacity == 10

def test_list_rooms_service(app_context):
    create_room_service("A", 5)
    create_room_service("B", 10)
    rooms = list_rooms_service()
    assert len(rooms) == 2

def test_has_booking_conflict_no_conflict(app_context):
    room = create_room_service("C", 10)
    # Existing booking 10:00 to 11:00
    create_booking_service(room.id, "10:00", "11:00")
    
    # 09:00 to 10:00 should not conflict
    assert not has_booking_conflict(room.id, "09:00", "10:00")
    # 11:00 to 12:00 should not conflict
    assert not has_booking_conflict(room.id, "11:00", "12:00")

def test_has_booking_conflict_exact_conflict(app_context):
    room = create_room_service("D", 10)
    create_booking_service(room.id, "13:00", "14:00")
    
    # Exact same slot
    assert has_booking_conflict(room.id, "13:00", "14:00")

def test_has_booking_conflict_partial_overlap(app_context):
    room = create_room_service("E", 10)
    create_booking_service(room.id, "15:00", "16:00")
    
    # Starts before, ends during
    assert has_booking_conflict(room.id, "14:30", "15:30")
    
    # Starts during, ends after
    assert has_booking_conflict(room.id, "15:30", "16:30")

    # Fully encapsulated
    assert has_booking_conflict(room.id, "15:15", "15:45")

def test_create_booking_service(app_context):
    room = create_room_service("F", 10)
    booking, err = create_booking_service(room.id, "09:00", "10:00")
    assert err is None
    assert booking.start_time == "09:00"

def test_list_bookings_service(app_context):
    room = create_room_service("G", 10)
    create_booking_service(room.id, "09:00", "10:00")
    bookings = list_bookings_service()
    assert len(bookings) == 1
