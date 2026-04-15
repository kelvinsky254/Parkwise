# Parkwise

A unified parking payment shortcut for Nairobi.

Nairobi has several parking operators — KAPS, EvoPay, Nairobi County, and
others — each managing multiple buildings, malls, and street lots. Each
operator has their own USSD code, their own payment flow, and their own
quirks. The friction isn't M-Pesa itself (that works fine), it's everything
before the PIN: figuring out which company runs this lot, finding their code,
navigating their menu, typing your plate and phone number on a small screen
in a parking lot.

Parkwise removes all of that. Open the app, tap your lot, tap dial. The
M-Pesa prompt arrives. Enter your PIN and drive away.

---

## How it works

When a car enters a parking lot, the operator's cameras log the plate number
and entry time. Their system already knows the car's location, duration, and
amount owed. Parkwise does not need to replicate any of that.

What Parkwise does is construct the correct USSD payment string for that
operator — pre-filled with your plate number and phone number — and open your
phone's dialer with it ready to dial. The operator's system handles everything
else.

```
User opens app
  → GPS finds the nearest known lot
  → App looks up which operator runs that lot
  → App constructs: *483*1*{plate}*{phone}#
  → User taps "Open Dialer"
  → Operator's system finds the plate, calculates amount owed
  → M-Pesa STK push arrives with the correct amount
  → User enters PIN
  → Done
```

Parkwise never handles money, never integrates with M-Pesa directly, and
never needs to know how long you have been parked. The operator already knows.

---

## Architecture

**Backend**: Django 5.1 + Django REST Framework  
**Auth**: JWT via SimpleJWT  
**Database**: PostgreSQL 16  
**Cache / broker**: Redis 7 + Celery  
**Containerisation**: Docker + docker-compose  
**CI**: GitHub Actions  

### Apps

| App | Responsibility |
|-----|----------------|
| `core` | Shared base models, pagination, middleware, exception handling |
| `accounts` | User registration, JWT auth, RBAC roles, vehicle management |
| `locations` | Curated parking lot database, GPS nearest-lot lookup |
| `vendors` | Operator config, pluggable USSD adapter per operator |
| `payments` | Payment session orchestration, audit trail |

### Vendor adapter pattern

Each parking operator has an adapter class that knows how to construct their
specific USSD chain string. The adapter class is stored as a dotted Python
path in the database (`Vendor.adapter_class`), loaded dynamically at runtime.

Adding a new operator requires:
1. One new adapter file in `vendors/adapters/`
2. One new `Vendor` row in the database

No changes to existing code.

### USSD chain templates

Each vendor record stores a `ussd_chain_template`, for example:

```
*483*1*{plate}*{phone}#
```

At runtime, `{plate}` and `{phone}` are substituted with the user's vehicle
plate and phone number. The resulting string is handed to the frontend as both
a plain string (for display and copying) and a `tel:` URI deeplink that opens
the phone dialer directly.

### Location matching

GPS coordinates from the user's device are compared against the curated lot
database using the Haversine formula. The nearest active lots within a
configurable radius (default 0.5 km) are returned, ordered by distance.
The user confirms their lot — a one-tap step that eliminates wrong-lot
payments in dense areas like mall complexes.

Lot-to-operator data is maintained manually. Operator websites publish their
locations, and the database is updated when operators change.

---

## Data models

### accounts
- `User` — custom user model (email-based auth), phone number, name
- `Role` — `driver`, `vendor_admin`, `parking_officer`, `super_admin`
- `UserRole` — through table linking users to roles with assignment timestamp
- `Vehicle` — plate number, make, model, color, default flag per user

### locations
- `ParkingLot` — name, address, GPS coordinates, active flag
- `LotVendorMapping` — links a lot to its operator with effective dates,
  so operator changes are tracked historically without data loss

### vendors
- `Vendor` — operator name, USSD shortcode, chain template, adapter class,
  config JSON, sandbox mode flag

### payments
- `PaymentSession` — audit record of every payment initiation: lot, vendor,
  plate, phone, USSD string generated, status (`initiated` / `dialed` /
  `cancelled`). Plate and phone are denormalised at session creation time so
  historical records are accurate even if the user later changes their details.

---

## API endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/auth/register/` | Create account |
| POST | `/api/v1/auth/token/` | Obtain JWT access + refresh tokens |
| POST | `/api/v1/auth/token/refresh/` | Refresh access token |
| GET PATCH | `/api/v1/users/profile/` | Get / update profile |
| GET POST | `/api/v1/users/vehicles/` | List vehicles / add vehicle |
| GET PATCH DELETE | `/api/v1/users/vehicles/<id>/` | Manage a vehicle |
| GET | `/api/v1/locations/nearby/?lat=&lng=` | Nearest lots to GPS coordinates |
| POST | `/api/v1/payments/initiate/` | Build USSD string for a lot + vehicle |
| GET | `/api/v1/payments/sessions/` | User's payment session history |
| PATCH | `/api/v1/payments/sessions/<id>/status/` | Mark session as dialed |

---

## Running locally

```bash
# 1. Clone and set up environment
cp .env.example .env
# Edit .env with your local values

# 2. Start backing services
docker-compose up -d db redis

# 3. Install dependencies
pip install -r requirements/dev.txt

# 4. Run migrations
python manage.py migrate

# 5. Load initial vendor data
python manage.py loaddata fixtures/initial_vendors.json

# 6. Create a superuser
python manage.py createsuperuser

# 7. Start the server
python manage.py runserver
```

Or run everything via Docker:

```bash
docker-compose up --build
```

---

## Running tests

```bash
pytest
```

Coverage is enforced at 70% minimum. The most meaningful tests cover:
- `haversine_km` distance calculation
- Adapter USSD string construction and `tel:` URI encoding
- `initiate_payment_session` service — happy path and no-vendor error case

---

## Vendor sandbox mode

All vendors default to `sandbox_mode=True`. In sandbox mode, adapters return
a fake USSD string so the full flow can be tested without dialling a real
shortcode. Set `VENDOR_SANDBOX_MODE=False` in `.env` and update each vendor's
`ussd_chain_template` with the confirmed live shortcode when going live.

USSD chain templates must be confirmed by manually testing each operator's
flow. Operator APIs are not publicly available.

---

## Project status

| Area | Status |
|------|--------|
| Backend scaffold | ✅ Done |
| Settings split (base / dev / prod) | ✅ Done |
| Docker + docker-compose | ✅ Done |
| GitHub Actions CI | ✅ Done |
| Data models + migrations | 🔄 In progress |
| DRF serializers + API endpoints | 🔄 In progress |
| USSD adapter pattern | 🔄 In progress |
| Location nearest-lot service | ⬜ Not started |
| Payment session orchestration | ⬜ Not started |
| Initial vendor fixtures | ⬜ Not started |
| Frontend | ⬜ Not started |
| Live USSD template verification | ⏳ Pending (requires manual testing) |
| Lot database (Nairobi) | ⏳ Pending (manual curation) |