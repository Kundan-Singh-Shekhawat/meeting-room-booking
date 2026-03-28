
import { useEffect, useState } from "react";
import { getRooms } from "../services/api";

/**
 * Component to list all available rooms.
 * @returns {JSX.Element}
 */
function Rooms() {
  const [rooms, setRooms] = useState([]);

  useEffect(() => {
    fetchRooms();
  }, []);

  async function fetchRooms() {
    const json = await getRooms();
    console.log(json);
    if (json.data) {
      setRooms(json.data);
    }
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