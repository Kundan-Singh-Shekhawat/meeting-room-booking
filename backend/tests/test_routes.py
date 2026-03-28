import pytest

def test_home(client):
    res = client.get("/")
    assert res.status_code == 200
    assert "data" in res.json
    assert "error" in res.json
    assert res.json["data"]["message"] == "API is running"

def test_create_and_get_room(client):
    res = client.post("/rooms", json={"name": "Huddle", "capacity": 4})
    assert res.status_code == 201
    assert res.json["data"]["message"] == "Room created"

    # Testing failing condition
    res_fail = client.post("/rooms", json={"name": ""})
    assert res_fail.status_code == 400
    assert res_fail.json["error"] == "Room name is required"

    res_get = client.get("/rooms")
    assert res_get.status_code == 200
    assert len(res_get.json["data"]) == 1
    assert res_get.json["data"][0]["name"] == "Huddle"

def test_create_booking(client):
    res_room = client.post("/rooms", json={"name": "ConfRoom", "capacity": 10})
    room_id = res_room.json["data"]["room"]["id"]

    res_book = client.post("/bookings", json={
        "room_id": room_id,
        "start_time": "10:00",
        "end_time": "11:00"
    })
    
    assert res_book.status_code == 201
    assert res_book.json["data"]["message"] == "Booking created"

    res_fail = client.post("/bookings", json={
        "room_id": room_id,
        "start_time": "10:30",
        "end_time": "11:30"
    })
    assert res_fail.status_code == 409
    assert res_fail.json["error"] == "Time slot already booked"
