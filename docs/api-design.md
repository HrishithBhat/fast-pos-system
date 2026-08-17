# API Design (FastAPI)

Base path: `/api`
Auth: Bearer JWT. Header: `Authorization: Bearer <token>`
All endpoints are scoped by authenticated user's `tenant_id`.

## Auth
- POST `/api/auth/register` (admin only)
  - body: { email, password, role }
  - resp: { id }
- POST `/api/auth/login`
  - body: { email, password }
  - resp: { access_token, token_type }

## Tenants & Settings
- GET `/api/settings`
  - resp: JSON settings for current tenant
- PUT `/api/settings` (admin)
  - body: JSON settings

## Catalog
- GET `/api/categories`
- POST `/api/categories` (manager/admin)
- GET `/api/products`
- POST `/api/products` (manager/admin)

## POS Flow
- POST `/api/cart/price`
  - body: { items: [{ product_id, quantity, modifiers?, discounts? }] }
  - resp: pricing summary (subtotal, taxes, discounts, grand_total)
- POST `/api/orders`
  - body: { items, source, payment_method }
  - resp: { order_id, status }
- GET `/api/orders/:id`
- PUT `/api/orders/:id/status` (kitchen flow)
  - body: { status }

## Payments
- POST `/api/payments/pay`
  - body: { order_id, method, amount }
  - resp: { status, gateway_ref? }
- POST `/api/payments/refund`
  - body: { order_id, amount }

## Receipts
- GET `/api/receipts/:order_id`
  - resp: { content_html }

## Inventory
- GET `/api/inventory/:product_id`
- POST `/api/inventory/adjust` (manager/admin)

## Reports
- GET `/api/reports/daily-sales?date=YYYY-MM-DD`
- GET `/api/reports/product-sales?from=&to=`
- GET `/api/reports/tax?from=&to=`
- GET `/api/reports/export.csv?type=orders|products&from=&to=`

## KDS Realtime
- WS `/ws/kds/{tenant_id}`
  - Receives broadcasted `{ order_id, status, items, created_at }` on updates.
