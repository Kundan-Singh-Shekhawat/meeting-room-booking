# AI Agent Rules — Meeting Room Booking

## Non-negotiable constraints
- All API responses MUST use the envelope: {"data": ..., "error": null} for success, {"data": null, "error": "msg"} for failure
- Never put business logic inside route handlers — it belongs in services.py
- Never use print() for logging — use Python's logging module
- All components must be .jsx files with JSDoc annotations
- Never use inline styles in JSX — use index.css only

## Allowed
- Adding new service functions in services.py
- Adding new route files in backend/routes/
- Adding new React components in frontend/src/

## Not allowed without explicit instruction
- Changing the API envelope format
- Modifying the has_booking_conflict function signature
- Adding new dependencies without updating requirements.txt
