## Current Limitations

**SQLite**: Chosen for zero-config local development. Cannot handle concurrent writes.
Swap path: Replace SQLAlchemy's database URI with a Postgres connection string. No other code changes needed.

**No Auth**: Any client can create or cancel bookings. 
Swap path: Add a Flask-Login or JWT middleware layer at the route level. Business logic is untouched.

**No Pagination**: GET /rooms and GET /bookings return all records.
Swap path: Add `?page=` and `?limit=` query params to route handlers.

**No Frontend Validation**: The UI sends whatever the user types.
Swap path: Add Yup schema validation before the API call in api.js.

## How New Features Would Be Added

Example: Adding recurring bookings
- Add a `recurrence` field to the Booking model in models.py
- Add recurrence expansion logic as a new function in services.py
- Add a new route in bookings.py that calls the service
- No existing routes, models, or frontend components need to change
