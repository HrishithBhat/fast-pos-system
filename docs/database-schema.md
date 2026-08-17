# Database Schema (PostgreSQL)

Note: All tables include `tenant_id` to enforce data isolation. Use UUIDs for primary keys where appropriate.

## Tables

### tenants
- id: UUID (PK)
- name: text
- code: text (unique)
- created_at: timestamptz
- updated_at: timestamptz

### tenant_settings
- id: UUID (PK)
- tenant_id: UUID (FK tenants)
- settings: JSONB
  - taxes: [{ name, rate, inclusive }]
  - discounts: [{ name, type (percent|amount), value, conditions }]
  - receipts: { header, footer, layout }
  - payments: { enabled: [cash, stripe, razorpay], stripe_key?, razorpay_key? }
  - roles: { customPermissions: { roleName: [perm keys] } }
- updated_at: timestamptz

### users
- id: UUID (PK)
- tenant_id: UUID (FK tenants)
- email: text (unique within tenant)
- password_hash: text
- role: text (enum: admin|manager|cashier|kitchen)
- is_active: bool
- created_at: timestamptz

### categories
- id: UUID (PK)
- tenant_id: UUID (FK tenants)
- name: text
- sort_order: int

### products
- id: UUID (PK)
- tenant_id: UUID (FK tenants)
- category_id: UUID (FK categories)
- name: text
- sku: text
- price: numeric(12,2)
- tax_rate: numeric(5,2) (default from tenant settings)
- modifiers: JSONB (e.g., size, addons)
- barcode: text
- is_active: bool
- stock_tracking: bool
- created_at: timestamptz

### orders
- id: UUID (PK)
- tenant_id: UUID (FK tenants)
- order_number: text (unique within tenant)
- status: text (enum: pending|preparing|ready|completed|cancelled)
- source: text (pos|online)
- subtotal: numeric(12,2)
- tax_total: numeric(12,2)
- discount_total: numeric(12,2)
- grand_total: numeric(12,2)
- payment_status: text (unpaid|paid|refund_pending|refunded)
- created_at: timestamptz
- completed_at: timestamptz nullable
- cashier_id: UUID (FK users)

### order_items
- id: UUID (PK)
- tenant_id: UUID (FK tenants)
- order_id: UUID (FK orders)
- product_id: UUID (FK products)
- name_snapshot: text (copy of product name)
- unit_price: numeric(12,2)
- quantity: int
- line_tax: numeric(12,2)
- line_discount: numeric(12,2)
- modifiers: JSONB

### payments
- id: UUID (PK)
- tenant_id: UUID (FK tenants)
- order_id: UUID (FK orders)
- method: text (cash|stripe|razorpay)
- amount: numeric(12,2)
- status: text (pending|succeeded|failed|refunded)
- gateway_ref: text (charge id, payment intent, etc.)
- created_at: timestamptz

### receipts
- id: UUID (PK)
- tenant_id: UUID (FK tenants)
- order_id: UUID (FK orders)
- content_html: text
- printed_at: timestamptz nullable

### inventory_movements
- id: UUID (PK)
- tenant_id: UUID (FK tenants)
- product_id: UUID (FK products)
- change: int (negative for sale)
- reason: text (sale|refund|adjustment|restock)
- order_id: UUID nullable
- created_at: timestamptz

## Indexes & Constraints
- Unique: (tenant_id, order_number) on `orders`
- Unique: (tenant_id, email) on `users`
- Foreign keys cascade where appropriate.
- Indexes: `tenant_id`, `created_at` on major tables for reporting.
