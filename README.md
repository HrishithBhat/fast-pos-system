# NexusPOS

A modern, full-stack Point of Sale (POS) application featuring a Next.js frontend and a high-performance Python/FastAPI backend.

## Architecture
This project follows a decoupled client-server architecture:
- **Client**: A robust Next.js application that handles the user interface. It communicates with the backend via REST API for standard operations (CRUD) and WebSockets for real-time features.
- **Server**: A high-performance Python backend built with FastAPI. It uses SQLAlchemy as the ORM to interact with the database (SQLite for local development).
- **Communication**: Axios and SWR are used on the frontend for data fetching and caching, ensuring a fast, responsive user experience. 

## Features
- **Order Management**: Create, update, and track customer orders.
- **Product Catalog**: Manage inventory and pricing.
- **Payment Processing**: Secure mock processing for completing transactions.
- **Real-Time KDS (Kitchen Display System)**: WebSockets provide real-time updates to kitchen staff as new orders are placed.
- **Authentication**: JWT-based secure user authentication.

## Tech Stack
- **Frontend**: Next.js 14, React 18, Tailwind CSS, SWR, Axios, TypeScript.
- **Backend**: Python 3.9+, FastAPI, SQLAlchemy, Uvicorn, Pydantic, Alembic.
- **Database**: SQLite (local) / PostgreSQL (production).

## Setup & Running

### Prerequisites
- Node.js (v18+)
- Python (3.9+)

### Backend Setup
1. Navigate to the `backend` folder:
   ```bash
   cd backend
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   # Windows
   .venv\Scripts\activate
   # Mac/Linux
   source .venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the server:
   ```bash
   uvicorn app.main:app --reload
   ```
   *The backend will be available at http://localhost:8000.*

### Frontend Setup
1. Navigate to the `frontend` folder:
   ```bash
   cd frontend
   ```
2. Install Node dependencies:
   ```bash
   npm install
   ```
3. Run the development server:
   ```bash
   npm run dev
   ```
   *The frontend will be available at http://localhost:3000.*

## API Reference
FastAPI auto-generates interactive API documentation. Once the backend is running, you can explore the API endpoints here:
- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

Key core routers include:
- `/auth/`
- `/products/`
- `/orders/`
- `/payments/`
- `/kds_ws/` (WebSocket connection for Kitchen Display System)

## Analysis Checks
The backend uses `pytest` and `pytest-asyncio` for unit and integration testing. 
To run the tests:
```bash
cd backend
pytest -v
```

## Trade-offs & Decisions
- **FastAPI over Django/Flask**: Chosen for its native asynchronous capabilities, automatic Pydantic validation, and excellent built-in WebSocket support needed for the KDS.
- **Decoupled Architecture**: Next.js API routes were deliberately skipped in favor of a standalone Python backend to ensure backend scalability and decoupling for potential future mobile applications.
- **SQLite for Local Dev**: Used SQLite via standard library for frictionless onboarding, utilizing SQLAlchemy to make a seamless transition to PostgreSQL in production. 
- **WebSockets vs Polling**: Opted for real-time WebSockets for the Kitchen Display System to minimize network overhead and ensure instantaneous updates compared to standard HTTP polling.

## Deployment Notes
- **Docker**: Both the frontend and backend include `Dockerfile`s in their respective directories allowing for containerized deployments on platforms like AWS run, Railway, or Google Cloud Run.
- **Database Migrations**: Alembic is configured in the backend. When deploying to production with PostgreSQL, run `alembic upgrade head` inside the container or CI/CD pipeline to properly structure the production DB.
- **Environment Variables**: Use the `.env.example` in the backend as a baseline for deploying real secrets (Database URIs, JWT keys) in production.

## Assumptions
- It is assumed that the local development environment is running on the default ports (8000 for FastAPI, 3000 for Next.js) and that CORS has been configured accordingly.
- Authentication endpoints mock user interactions or rely on predefined user roles within the local testing phase.
