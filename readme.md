# Meeting Room Booking System

### 1. Project Overview
This is a full-stack web application designed for booking meeting rooms efficiently. It allows users to view a list of available rooms, create new room definitions, and confidently book time slots for specific rooms while guaranteeing no double-bookings or time slot overlaps occur. It was built specifically as a self-contained software engineering assessment project.

### 2. Tech Stack
- **Backend:** Python, Flask, SQLAlchemy, SQLite
- **Frontend:** React (.jsx components)
- **Testing:** pytest

### 3. Key Technical Decisions
- **Why SQLite (not Postgres):** SQLite was explicitly chosen for its simplicity in local development and because it perfectly suites the scope of a fast bootstrapping assessment without requiring external deployment infrastructure.
- **Why a unified API envelope `{data, error}`:** Standardizing all responses around a single JSON payload guarantees predictable parsing on the frontend and provides a single unwrap point, greatly reducing parsing logic errors for unexpected errors.
- **Why conflict logic is isolated in `services.py`:** Extracting pure business logic away from Flask ensures it remains highly testable in isolation and separates mathematical/database logic from HTTP routing.
- **Why routes are split into `rooms.py` and `bookings.py`:** A modular layout enforces the single-responsibility principle, prevents the application factory from bloating, and makes adding future API resources drastically easier.

### 4. Known Tradeoffs & Weaknesses
- SQLite does not support concurrent writes — not suitable for production scaling.
- No authentication or authorization — any user can blindly book or delete any room.
- No pagination on list endpoints — performance will aggressively degrade as the database grows with large data.
- No frontend input validation beyond what the API rejects post-flight.

### 5. How to Run
**Backend:** 
```bash
PYTHONPATH=. .venv/bin/python backend/app.py
```
*(Runs securely on localhost:5000)*

**Frontend:** 
```bash
cd frontend && npm start
```
*(Runs intuitively on localhost:3000)*

### 6. Running Tests
```bash
PYTHONPATH=. .venv/bin/pytest backend/tests/
```

### 7. AI Usage
- **Tool used:** Gemini (Antigravity Agent)
- **What it was used for:** Scaffolding the route structure, generating the exhaustive test cases, refactoring the legacy monolith into MVC, and producing these developer documents.
- **How output was reviewed:** Every generated file was read line by line. The time-slot conflict logic was manually verified, and entire test suites were aggressively run after each iteration.
- **What was NOT delegated to AI:** Final overarching business logic decisions and the strict architectural splitting rules.
