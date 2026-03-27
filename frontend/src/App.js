import Rooms from "./pages/Rooms";
import BookingForm from "./pages/BookingForm";
import Bookings from "./pages/Bookings";

function App() {
  return (
    <div>
      <h1>Meeting Room Booking System</h1>

      <Rooms />
      <BookingForm />
      <Bookings />
    </div>
  );
}

export default App;