
import { useEffect, useState } from "react";
import { getBookings } from "../services/api";

function Bookings() {
  const [bookings, setBookings] = useState([]);

  useEffect(() => {
    fetchBookings();
  }, []);

  async function fetchBookings() {
    const data = await getBookings();
    setBookings(data);
  }

  return (
    <div>
      <h2>Bookings</h2>
      <ul>
        {bookings.map((b) => (
          <li key={b.id}>
            Room {b.room_id} | {b.start_time} - {b.end_time}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default Bookings;