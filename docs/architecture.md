# POS System Architecture (Multi-tenant)

This design targets restaurants, online kitchens, and retail with per-tenant customization. It uses Next.js for the frontend, FastAPI for the backend, PostgreSQL for data, WebSockets for realtime, and pluggable payments (Stripe/Razorpay). Security is JWT-based with role RBAC.

## High-level overview

```mermaid
flowchart LR
    subgraph Client[Browser/Devices]
      POS[POS UI]
      Admin[Admin Dashboard]
      KDS[Kitchen Display]
    end

    POS -->|REST| API[FastAPI]
    Admin -->|REST| API
    KDS -->|WebSocket| WS[(WS Gateway)]

    API --> DB[(PostgreSQL)]
    API --> Cache[(Optional Redis)]
    API --> Pay[Payments (Stripe/Razorpay)]

    WS --> API

    subgraph DBLayer[Postgres]
      Tenants[(tenants)]
      Users[(users)]
      Products[(products)]
      Orders[(orders)]
      OrderItems[(order_items)]
      Payments[(payments)]
      Settings[(tenant_settings JSONB)]
      Inventory[(inventory_movements)]
    end

    API <--> DBLayer
```

### Multi-tenancy
- All business entities include `tenant_id`.
- Per-tenant JSON settings (`tenant_settings.settings`) drive taxes, discounts, receipt layout, payment options, business rules.
- Row-level filtering by `tenant_id` enforced in repository layer and auth context. Optional PostgreSQL RLS can be added later.

### Security
- JWT access tokens; refresh token optional.
- Role-based access control: Admin, Manager, Cashier, Kitchen.
- Endpoint guards (dependencies) enforce role + tenant ownership.

### Realtime (KDS)
- WebSocket channel per tenant: `/ws/kds/{tenant_id}`.
- Order status events broadcast to subscribed KDS clients.

### Payments (pluggable)
- Strategy interface: `CashPayment`, `StripePayment`, `RazorpayPayment`.
- Selected via tenant settings JSON; can be per terminal.

### Hardware support
- Printer: generate HTML/ESC/POS-ready receipt payloads; front-end prints or service sends to local agent.
- Barcode scanner: handled as keyboard input in POS or via WebUSB.
- Cash drawer: via printer pulse or local agent API.

### Deployment
- Docker Compose with services: `db`, `backend`, `frontend`.
- Environment-driven configuration; secrets via env vars.
