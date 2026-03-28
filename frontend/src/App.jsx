import Rooms from "./pages/Rooms";
import BookingForm from "./pages/BookingForm";
import Bookings from "./pages/Bookings";
import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";

/**
 * Main application component.
 * @returns {JSX.Element}
 */
function App() {
  return (
    <Router>
      <div>
        <h1>Meeting Room Booking System</h1>

        <nav className="main-nav">
          <Link to="/" className="nav-link">Rooms</Link>
          <Link to="/book" className="nav-link">Book Room</Link>
          <Link to="/bookings" className="nav-link">Bookings</Link>
        </nav>

        <Routes>
          <Route path="/" element={<Rooms />} />
          <Route path="/book" element={<BookingForm />} />
          <Route path="/bookings" element={<Bookings />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;