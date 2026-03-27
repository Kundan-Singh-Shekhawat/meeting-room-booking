# Meeting Room Booking System

A full-stack web application that enables users to view meeting rooms, create bookings, and automatically prevents overlapping reservations through conflict detection logic.

---

## Project Structure

```
meeting-room-booking/
├── backend/
│   ├── app.py                 # Flask app entry point
│   ├── models.py              # SQLAlchemy ORM models
│   ├── services.py            # Business logic & conflict detection
│   ├── routes.py              # REST API endpoints
│   └── requirements.txt
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── pages/
│   │   │   ├── Rooms.jsx        # Displays all rooms
│   │   │   ├── BookingForm.jsx  # Creates a booking
│   │   │   └── Bookings.jsx     # Displays all bookings
│   │   ├── services/
│   │   │   └── api.js           # Fetch-based API layer
│   │   └── App.jsx
│   └── package.json
└── .gitignore
```

---

## Architecture

```
React (UI)  →  Flask REST API (Business Logic)  →  SQLite (Data Storage)
```

---

## Features

- View all available meeting rooms
- Create bookings for a specific room and time slot
- Prevent overlapping bookings via conflict detection
- View all existing bookings

---

## Core Entities

### Room
| Field | Type | Description |
|-------|------|-------------|
| `id` | Integer | Primary key |
| `name` | String | Room name (must not be empty) |
| `capacity` | Integer | Maximum capacity (must be a positive integer) |

### Booking
| Field | Type | Description |
|-------|------|-------------|
| `id` | Integer | Primary key |
| `room_id` | Integer | Foreign key referencing Room |
| `start_time` | String | Format: `HH:MM` |
| `end_time` | String | Format: `HH:MM` |

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/rooms` | Retrieve all rooms |
| `POST` | `/rooms` | Create a new room |
| `GET` | `/bookings` | Retrieve all bookings |
| `POST` | `/bookings` | Create a booking (with conflict detection) |

### Example — Create a Booking

**Request**
```json
POST /bookings
{
  "room_id": 1,
  "start_time": "09:00",
  "end_time": "10:30"
}
```

**Success Response** `201 Created`
```json
{
  "id": 5,
  "room_id": 1,
  "start_time": "09:00",
  "end_time": "10:30"
}
```

**Conflict Response** `409 Conflict`
```json
{
  "error": "Booking conflicts with an existing reservation."
}
```

---

## Conflict Detection Logic

A new booking is rejected if it overlaps with any existing booking for the same room.

The overlap condition is evaluated as follows:

```
NOT (new_end <= existing_start OR new_start >= existing_end)
```

Two bookings are considered non-overlapping only when the new booking ends at or before the existing one starts, or begins at or after the existing one ends. Any other case is treated as a conflict and the request is rejected.

---

## Validation Rules

| Field | Rule |
|-------|------|
| Room name | Must not be empty |
| Capacity | Must be a positive integer |
| Start time | Must be in `HH:MM` format |
| End time | Must be in `HH:MM` format |
| Time order | `start_time` must be earlier than `end_time` |
| Booking slot | Must not overlap with any existing booking for the same room |

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | React (functional components, `useState`, `useEffect`) |
| Backend | Python, Flask (REST API) |
| Database | SQLite via SQLAlchemy ORM |
| API Communication | `fetch()` in `services/api.js` |
| Cross-Origin Requests | CORS enabled on Flask |

---

## Getting Started

### Prerequisites

- Python 3.8+
- Node.js 16+ and npm

---

### Backend Setup

```bash
# 1. Navigate to the backend directory
cd backend

# 2. Create and activate a virtual environment
python -m venv venv

# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Start the Flask development server
python app.py
```

The backend server will be available at `http://127.0.0.1:5000`.

---

### Frontend Setup

```bash
# 1. Navigate to the frontend directory
cd frontend

# 2. Install dependencies
npm install

# 3. Start the React development server
npm start
```

The frontend will be available at `http://localhost:3000`.

> Note: The Flask backend must be running before launching the frontend.

---

## Known Limitations

- No authentication or user management system
- Time values are stored as strings (`HH:MM`) rather than proper `datetime` objects
- No timezone support
- Minimal UI with no styling framework or calendar view

---

## Future Improvements

- [ ] Implement JWT-based authentication and user login
- [ ] Migrate to `datetime` objects for more robust time handling
- [ ] Develop a calendar-based booking interface
- [ ] Introduce email or push notifications for booking reminders
- [ ] Improve UI/UX with a styling framework such as Tailwind CSS
- [ ] Add timezone awareness

---

## AI Usage

- AI tooling was used for scaffolding and boilerplate generation
- Core logic, particularly conflict detection, was manually reviewed and validated
- Code conventions were kept simple and readable, with no unnecessary abstractions

---

## Design Philosophy

The project prioritises correctness and readability over complexity. Business logic is separated from route handlers through a basic service layer, and invalid states are prevented through strict input validation at the API level.

---

## Author

**Kundan Singh Shekhawat**  
GitHub: [@Kundan-Singh-Shekhawat](https://github.com/Kundan-Singh-Shekhawat)
