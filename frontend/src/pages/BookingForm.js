import { useState } from "react";
import { createBooking } from "../services/api";

function BookingForm() {
  const [roomId, setRoomId] = useState("");
  const [startTime, setStartTime] = useState("");
  const [endTime, setEndTime] = useState("");
  const [message, setMessage] = useState("");

  async function handleSubmit(e) {
    e.preventDefault();

    const res = await createBooking({
      room_id: Number(roomId),
      start_time: startTime,
      end_time: endTime,
    });

    if (res.error) {
      setMessage(res.error);
    } else {
      setMessage("Booking created!");
    }
  }

  return (
    <div>
      <h2>Create Booking</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="number"
          placeholder="Room ID"
          value={roomId}
          onChange={(e) => setRoomId(e.target.value)}
        />
        <br />
        <input
          type="text"
          placeholder="Start Time (HH:MM)"
          value={startTime}
          onChange={(e) => setStartTime(e.target.value)}
        />
        <br />
        <input
          type="text"
          placeholder="End Time (HH:MM)"
          value={endTime}
          onChange={(e) => setEndTime(e.target.value)}
        />
        <br />
        <button type="submit">Book</button>
      </form>

      <p>{message}</p>
    </div>
  );
}

export default BookingForm;