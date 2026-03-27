
import { useEffect, useState } from "react";
import { getRooms } from "../services/api";

function Rooms() {
  const [rooms, setRooms] = useState([]);

  useEffect(() => {
    fetchRooms();
  }, []);

  async function fetchRooms() {
    const data = await getRooms();
    console.log(data);
    setRooms(data);
  }

  return (
    <div>
      <h2>Rooms</h2>
      <ul>
        {rooms.map((room) => (
          <li key={room.id}>
            {room.name} (Capacity: {room.capacity})
          </li>
        ))}
      </ul>
    </div>
  );
}
export default Rooms;