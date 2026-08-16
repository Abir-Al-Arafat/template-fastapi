# FastAPI Template Application

A production-ready FastAPI project boilerplate utilizing async patterns, dependency injection, and clean layered architecture.

## Server Overview & Architecture

This repository follows a clean, layered architectural pattern designed to enforce separation of concerns, improve testability, and decouple database operations from HTTP routing.

```mermaid
graph TD
    Client[Client / Frontend] -->|HTTP Request| Endpoints[API Endpoints / Routes]
    Endpoints -->|Validation / Auth| Dependencies[Dependencies / Guards]
    Endpoints -->|Invokes| Services[Service Layer]
    Services -->|Orchestrates Business Logic| Repositories[Repositories]
    Repositories -->|Queries / Mutates| Database[(Database via SQLAlchemy)]

    subgraph Data Schemas & Models
        Schemas[Pydantic Schemas] -.->|Validates / Serializes| Endpoints
        Models[SQLAlchemy Models] -.->|Maps tables| Repositories
    end
```

### Layer Breakdown

1. **API Endpoints (`app/api/`)**: Defines HTTP routes (e.g., GET, POST, PATCH, DELETE). This layer is purely responsible for handling requests, validating authentication/authorization permissions via dependencies, calling services, and returning formatted responses.
2. **Dependencies (`app/api/dependencies.py`)**: Reusable dependencies injected via FastAPI's `Depends` system, such as DB session management and JWT authentication guards.
3. **Services (`app/services/`)**: The core domain layer where business logic and workflows are orchestrated. It acts as the bridge between API controllers and data access repositories.
4. **Repositories (`app/repositories/`)**: Encapsulates all data access and SQL operations. Inherits from a generic `BaseRepository` for standardized CRUD operations.
5. **Schemas (`app/schemas/`)**: Pydantic V2 schemas for input validation, type safety, and output serialization.
6. **Models (`app/models/`)**: SQLAlchemy 2.0 ORM declarations mapping Python classes to database tables.
7. **Core Config (`app/core/`)**: Core application components such as JWT security configurations (`security.py`), settings management (`config.py`), and database connection engine/session configuration (`database.py`).

---

## Prerequisites

Ensure you have the following installed on your machine:

- **Python**: version `3.10` or higher
- **Virtual Environment Tool**: `venv` (comes bundled with Python 3)
- **Database**: PostgreSQL (or SQLite for local development out-of-the-box)

---

## How to Pull & Run Locally

Follow these steps to set up and run the service locally:

### 1. Clone or Pull the Repository

Clone the project (or fetch the latest updates):

```bash
git clone <repository-url>
cd template-fastapi
```

### 2. Set Up a Virtual Environment

Create a local Python virtual environment to isolate project dependencies:

```bash
python3 -m venv .venv
```

Activate the virtual environment:

- **Linux / macOS**:
  ```bash
  source .venv/bin/activate
  ```
- **Windows (cmd)**:
  ```cmd
  .venv\Scripts\activate.bat
  ```
- **Windows (PowerShell)**:
  ```powershell
  .venv\Scripts\Activate.ps1
  ```

### 3. Install Dependencies

Install all required libraries inside the virtual environment:

```bash
pip install -r requirements.txt
```

_(Note: If `requirements.txt` does not exist, ensure packages like `fastapi`, `uvicorn`, `sqlalchemy`, `aiosqlite`, `pydantic`, `pydantic-settings`, `python-jose`, and `passlib[bcrypt]` are installed.)_

### 4. Configure Environment Variables

Create a `.env` file in the root directory:

```bash
cp .env.example .env
```

Or manually create `.env` and configure the settings:

```env
DATABASE_URL=sqlite+aiosqlite:///./sql_app.db
SECRET_KEY=generate-a-secure-random-key-here-for-production
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 5. Run the Local Development Server

Start the Uvicorn ASGI server with hot-reload enabled:

```bash
uvicorn app.main:app --reload
```

or

```bash
uvicorn app.main:app --host 0.0.0.0 --port 5003 --reload
```

The server will start on `http://127.0.0.1:8000`.

---

## Interactive Documentation

Once the server is running, FastAPI automatically generates interactive API documentation. You can access it via your web browser:

- **Swagger UI**: Visit [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) to visually interact with and execute queries against the API endpoints directly.
- **ReDoc**: Visit [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc) for fully structured, offline-readable API schema specifications.

---

## Environment Variables Schema

The application configures its behavior via the following variables defined in `app/core/config.py`:

| Variable Name                 | Type  | Default Value                      | Description                                                                   |
| :---------------------------- | :---- | :--------------------------------- | :---------------------------------------------------------------------------- |
| `DATABASE_URL`                | `str` | `sqlite+aiosqlite:///./sql_app.db` | SQLAlchemy connection string (e.g. `postgresql+asyncpg://user:pass@host/db`). |
| `SECRET_KEY`                  | `str` | `change_me_in_production_...`      | Cryptographic secret key used to sign JWT access tokens.                      |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `int` | `30`                               | Lifespan duration of generated JWT access tokens.                             |
| `PROJECT_NAME`                | `str` | `FastAPI Template Application`     | The project title displayed in Swagger/ReDoc.                                 |
| `VERSION`                     | `str` | `1.0.0`                            | SemVer versioning for the current build of the API.                           |
