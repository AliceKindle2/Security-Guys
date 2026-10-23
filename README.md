# SecurityGuys
SecurityGuys is a mock medical patient portal that is intentionally non-compliant with GDPR and CCPA/CPRA. Every violation is deliberate and annotated in `backend/models.py` with the article or section it breaks. Do not deploy or enter real personal data.

## OS Requirements
Any OS that runs Python 3.10+ which includes macOS, Windows 10/11, or Linux.

## Programming Languages
- Python 3.10+ (backend)

## Required Software and Dependencies
- Python 3.10 or newer
- Git to clone the repo
- Python packages:
  - FastAPI: web framework
  - Uvicorn: ASGI server
  - SQLAlchemy: ORM and database tooling
  - Pydantic: request validation

SQLite is used as the database (included with Python.)

## Installation
1. Clone the repo and enter it:
   ```bash
   git clone https://github.com/teaBag024/SecurityGuys
   cd SecurityGuys
   ```
2. In the root directory of the project, create a venv:
   ```bash
   python3 -m venv .venv
   ```
3. Activate it:
   - macOS/Linux: `source .venv/bin/activate`
   - Windows: `.venv\Scripts\activate`
4. Install dependencies:
   ```bash
   pip install -r backend/requirements.txt
   ```

## Running the Program
The server must be started from inside `backend/` (the database path is relative to it):
```bash
cd backend
uvicorn main:app --reload
```

- The API runs at http://127.0.0.1:8000
- API docs are at http://127.0.0.1:8000/docs
- On first run, an SQLite database is created at `backend/app.db`. To reset all data, delete this file.

### Endpoints
| Method | Path      | Description                                  |
|--------|-----------|----------------------------------------------|
| GET    | `/health` | Health check, returns `{"status": "ok"}`     |
| POST   | `/signup` | Creates a user account                       |

## Login Credentials for Testing
No accounts are pre-seeded. Create a test account with `/signup`, either from the `/docs` page or with curl:

```bash
curl -X POST http://127.0.0.1:8000/signup \
  -H "Content-Type: application/json" \
  -d '{
    "full_name": "Test User",
    "email": "test@example.com",
    "password": "password123",
    "ssn": "123-45-6789",
    "date_of_birth": "1990-01-01",
    "address": "123 Main St",
    "phone": "555-666-7777",
    "medical_history": "None"
  }'
```

| Email              | Password      |
|--------------------|---------------|
| test@example.com   | password123   |

Use fake data only, as passwords and SSNs are stored in plaintext intentionally.

## Current Incomplete Features
- **Login / authentication**: there is no login endpoint or session/token handling yet, so the credentials above can't be used to sign in yet.
- **Frontend**: frontend is WIP and has not yet been merged into main.
- **Appointments, prescriptions, third-party data broker logs, and audit logs**: the database tables exist in `models.py` but there are no API endpoints to create or read them.
- **Account management**: no endpoints to view, update, or delete a user.
- **Seed data**: no script to pre-populate test users or records.
- **Automated tests**: none yet.
