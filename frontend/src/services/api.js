const BASE_URL = "http://127.0.0.1:5000";

export async function getRooms() {
  const res = await fetch(`${BASE_URL}/rooms`);
  return res.json();
}

export async function createBooking(data) {
  const res = await fetch(`${BASE_URL}/bookings`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  });

  return res.json();
}

export async function getBookings() {
  const res = await fetch(`${BASE_URL}/bookings`);
  return res.json();
}