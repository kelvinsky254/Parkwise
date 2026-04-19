# Parkwise

A unified parking payment shortcut for Nairobi.

Nairobi has several parking operators — KAPS, EvoPay, Nairobi County, and others — each managing their own lots with their own USSD codes, payment flows, and menu structures. The friction isn't M-Pesa (that works fine), it's everything before the PIN: figuring out which company runs this lot, finding their code, navigating their menu, and typing your plate and phone number on a small screen in a parking lot.

Parkwise removes all of that. Open the app, tap your lot, tap dial. The M-Pesa prompt arrives. Enter your PIN and drive away.

---

## How it works

When a car enters a parking lot, the operator's cameras log the plate number and entry time. Their system already knows the car's location, duration, and amount owed. Parkwise does not replicate any of that.

What Parkwise does is construct the correct USSD payment string for that operator — pre-filled with your plate number and phone number — and open your phone's dialer with it ready to send. The operator's system handles the rest.

---

## Running locally

```bash
# 1. Clone and configure environment
git clone https://github.com/kelvinsky254/Parkwise.git
cd Parkwise
cp .env.example .env

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

---

## Running tests

```bash
pytest
```

Coverage is enforced at 70% minimum. Key test coverage includes:
- `haversine_km` distance calculation
- Adapter USSD string construction and `tel:` URI encoding
- `initiate_payment_session` service — happy path and no-vendor error case

---

## Project structure

```
parkwise/
├── .github/workflows/ci.yml      ← GitHub Actions (test + lint + coverage)
├── parkwise/
│   ├── settings/
│   │   ├── base.py               ← shared config (DRF, JWT, Celery, DB)
│   │   ├── dev.py                ← DEBUG=True, console email
│   │   └── prod.py               ← security hardening, SMTP
│   ├── urls.py
│   ├── api_router.py
│   └── celery.py
├── apps/
│   ├── accounts/                 ← User, Vehicle models + JWT auth
│   ├── locations/                ← ParkingLot, LotVendorMapping, nearby search
│   ├── vendors/                  ← Vendor model + adapter pattern
│   ├── payments/                 ← PaymentSession, orchestration service
│   └── core/                     ← shared utilities
├── requirements/
│   ├── base.txt
│   ├── dev.txt
│   └── prod.txt
├── Dockerfile
├── docker-compose.yml            ← web + db (port 5433) + redis + celery
├── pytest.ini
├── .env.example
└── .gitignore
```

---

## Vendor adapter pattern

Adding a new parking operator requires:
1. Create `apps/vendors/adapters/newvendor.py` extending `BaseVendorAdapter`
2. Implement `build_ussd_payload()`
3. Add a `Vendor` row in the database pointing to the adapter class
4. Map parking lots to the vendor via `LotVendorMapping`

No changes needed to existing code.

---

## Vendor sandbox mode

All vendors default to `sandbox_mode=True`. In sandbox mode, adapters return a fake USSD string so the full flow can be tested without dialling a real shortcode. Set `VENDOR_SANDBOX_MODE=False` in `.env` and update each vendor's `ussd_chain_template` with the confirmed live shortcode when going live.

USSD chain templates must be confirmed by manually testing each operator's flow.

---

## Project status

| Area | Status |
|------|--------|
| Django project scaffold | ✅ Done |
| Settings split (base/dev/prod) | ✅ Done |
| Data models — all 5 apps | ✅ Done |
| Migrations | ✅ Done |
| USSD vendor adapter pattern | ✅ Done |
| Location nearest-lot service (Haversine) | ✅ Done |
| Payment session orchestration | ✅ Done |
| Docker + docker-compose | ✅ Done (PostgreSQL on port 5433) |
| GitHub Actions CI | ✅ Done |
| DRF serializers + API endpoints | ⬜ Not started |
| Tests (target 70% coverage) | ⬜ Not started |
| Initial vendor fixtures | ⬜ Not started |
| Frontend (3-screen mobile UI) | ⬜ Not started |
| Live USSD template verification | ⏳ Pending (requires manual testing) |
| Nairobi lot database | ⏳ Pending (manual curation) |