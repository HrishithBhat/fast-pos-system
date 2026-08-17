# fast-pos-system

A robust, real-time Point of Sale (POS) backend and frontend architecture built with FastAPI, Next.js, and WebSockets.

## Table of Contents
- [Architecture](#architecture)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Setup & Running](#setup--running)
- [API Reference](#api-reference)
- [Analysis & Validation Checks](#analysis--validation-checks)
- [Trade-offs & Decisions](#trade-offs--decisions)
- [Deployment Notes](#deployment-notes)
- [Assumptions](#assumptions)

## Architecture

### System Flow Diagram

```text
┌─────────┐      POST /api/orders/              ┌──────────────┐
│  Client  │ ────────────────────────────────▸│  FastAPI     │
│(Next.js) │ ◂──── 201 { order, status }──────│   Server     │
└────┬────┘                                   └──────┬───────┘
     │                                               │
     │            ┌──────────────────────────────────┤
     │            │  1. Validate stock availability  │
     │            │  2. Compute order totals         │
     │            │  3. Insert DB row (pending)      │
     │            │  4. Broadcast to KDS via WS      │
     │            └──────────────────────────────────┘
     │                                               │
┌────▼────┐                                   ┌──────▼───────┐
│ Kitchen │ ◂─── WebSocket (Order Details) ───│  SQLite /    │
│ Display │                                   │  PostgreSQL  │
│ System  │ ────────────────────────────────▸ │              │
└─────────┘      PUT /api/orders/{id}/status    └──────────────┘
```

### Processing Flow
1. **Order Placement**: Client sends order data via `POST /api/orders/`.
2. **Validation**: FastAPI validates product IDs, verifies availability, and calculates the total price including taxes.
3. **Persistence**: Order is saved to the local SQLite database (or Postgres) through SQLAlchemy.
4. **Real-Time Notification**: The server instantly pushes the new order payload over a WebSocket channel to the Kitchen Display System (KDS).
5. **Fulfillment**: Kitchen staff update the order status (`PUT /api/orders/{id}/status`) which broadcasts changes back to the POS client.

## Features

### Core
- ✅ **Product Management**: Endpoints for creating and tracking product catalogs.
- ✅ **Order Pipeline**: Full lifecycle control from creation to fulfillment.
- ✅ **Real-Time KDS**: Live kitchen display updates via WebSockets (no polling).
- ✅ **Mock Payments**: Simulation of payment processing.
- ✅ **JWT Authentication**: Secure user login and role-based access control.

### Bonus
- ✅ **Responsive UI**: Built with Next.js and Tailwind CSS.
- ✅ **Database Migrations**: Alembic integrated for safe schema iterations.
- ✅ **Automated Testing**: Pytest-ready testing suite setup for backend APIs.
- ✅ **Containerization**: Included Dockerfiles for predictable deployment.

## Tech Stack

| Component | Technology | Justification |
|-----------|------------|---------------|
| **Frontend** | Node.js + Next.js (React) | Seamless client-side routing and component structure. |
| **Styling** | Tailwind CSS | Fast, utility-first UI styling. |
| **Backend** | Python + FastAPI | Blazing fast REST APIs with native Pydantic validation. |
| **Database** | SQLite + SQLAlchemy | Zero-config local db, type-safe ORM, seamless Postgres switch later. |
| **Migrations** | Alembic | Track database schema changes effortlessly. |
| **Real-time** | WebSockets (FastAPI built-in) | Perfect for KDS, better than REST polling. |
| **Security** | python-jose / passlib | Industry-standard JWT handling and password hashing. |

## Project Structure

```text
fast-pos-system/
├── backend/
│   ├── alembic.ini                # DB Migrations config
│   ├── app/
│   │   ├── api/                   # Core endpoint routers (orders, auth, products)
│   │   ├── core/                  # Security, configs, dependencies
│   │   ├── models/                # SQLAlchemy database models
│   │   ├── schemas/               # Pydantic schemas (Types/Validation)
│   │   ├── services/              # Business logic decoupling
│   │   └── main.py                # FastAPI entry point
│   ├── tests/                     # Pytest test suite
│   ├── requirements.txt           # Python dependencies
│   └── Dockerfile                 # Backend container
├── frontend/
│   ├── src/
│   │   ├── pages/                 # Next.js UI routing (POS, Admin, KDS)
│   │   └── styles/                # Tailwind global styles
│   ├── package.json               # Node dependencies
│   ├── tailwind.config.js         # UI config
│   └── Dockerfile                 # Frontend container
├── infra/                         # Docker Compose setups
└── README.md                      # This file
```

## Setup & Running

### Prerequisites
- Node.js 18+
- Python 3.9+
- Docker (optional)

### Option 1: Docker Compose

```bash
# Start the full stack
cd infra
docker-compose up --build

# API will be at http://localhost:8000
# Frontend will be at http://localhost:3000
```

### Option 2: Local Development

```bash
# 1. Setup Backend
cd backend
python -m venv .venv
# Activate: `.\.venv\Scripts\activate` (Windows) or `source .venv/bin/activate` (Mac/Linux)
pip install -r requirements.txt
uvicorn app.main:app --reload

# API: http://localhost:8000
# Swagger UI: http://localhost:8000/docs

# 2. Setup Frontend (New Terminal)
cd frontend
npm install
npm run dev

# Frontend UI: http://localhost:3000
```

## API Reference

### Create Order
```bash
curl -X POST http://localhost:8000/api/orders/ \
  -H "Content-Type: application/json" \
  -d '{"items": [{"product_id": 1, "quantity": 2}]}'
```
**Response (201 Created):**
```json
{
  "id": 12,
  "status": "pending",
  "total": 45.50,
  "created_at": "2024-01-15T10:30:00.000Z"
}
```

### Update Order Status
```bash
curl -X PUT http://localhost:8000/api/orders/12/status \
  -H "Content-Type: application/json" \
  -d '{"status": "completed"}'
```

### KDS WebSocket Connection
```javascript
const ws = new WebSocket('ws://localhost:8000/api/kds_ws/');
ws.onmessage = (event) => {
  console.log("New order for Kitchen:", JSON.parse(event.data));
};
```

## Analysis & Validation Checks

The system runs several business logic conditions autonomously before accepting an order:

1. **Inventory Availability**: Cross-references local stock before adding to cart.
2. **Price Consistency**: Re-calculates total order sums strictly on the backend to prevent client-side cart tampering.
3. **Data Integrity**: Uses Pydantic validation ensuring strict typed data is parsed from JSON before it touches the ORM layer.
4. **WebSocket Connectivity**: Verifies active KDS sessions before attempting to broadcast order payloads.

## Trade-offs & Decisions

| Area | Decision | Rationale |
|------|-----------|-----------|
| **Framework** | FastAPI over Django | Provides asynchronous features natively (needed for KDS WebSockets) and built-in type validation via Pydantic. |
| **Separation** | Distinct API/Frontend | Did not use Next.js API Routes for the POS business logic to ensure the backend could scale independently (e.g., if we develop a native mobile app). |
| **Real-Time** | WebSockets over Polling | A KDS strictly requires sub-second freshness. Standard REST polling would unnecessarily load the DB. |
| **Storage** | SQLite | Easy to run locally out-of-the-box. SQLAlchemy ensures upgrading to PostgreSQL just requires swapping the connection string. |

## Deployment Notes

### Architecture for Scale
- **Backend (Render / Railway / AWS ECS)**: Deploy the FastAPI app via a Dockerfile. Set scaling concurrency behind a Load Balancer.
- **Frontend (Vercel / Netlify)**: The frontend should be deployed as a static or edge-rendered application.
- **Database (AWS RDS / Supabase)**: Host the PostgreSQL database. Swap the `DATABASE_URL` `.env` variable inside the backend to migrate off SQLite effortlessly.

## Assumptions
- **Local environment mapping**: WebSockets are hardcoded to test over `.localhost` protocols. These need `wss://` conversion for production.
- **Mock Payments**: Real payment gateways (like Stripe/Square) are abstracted temporarily; transactions simulate a success scenario.
- **Authentication Bypass**: Local development endpoints currently ignore strict multi-tenant constraints for easier UI testing.
