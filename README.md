# Trekking Management Web Application

A role-based web application for managing a trekking organization — built as a course project for the IIT Madras BS Degree program (Modern Application Development II).

The app supports three distinct user roles — **Admin**, **Trek Staff**, and **Trekker** — each with a dedicated dashboard and permission set, backed by a Flask REST API and a Vue 3 single-page frontend.

---

## Features

**Trekker**
- Register and log in
- Browse open treks with difficulty filtering
- Book a trek via an in-page modal (no page navigation)
- View active bookings and past booking history
- Edit profile details and change password

**Trek Staff** *(created by admin only — no self-registration)*
- Dashboard with KPIs: assigned treks, total participants, ongoing treks
- View treks assigned to them
- View participant details (name, age, language, phone) per trek via modal
- Close an assigned trek
- Edit profile details and change password

**Admin**
- Dashboard with organization-wide KPIs
- Full trek management: create, edit, close, reopen
- Staff management: create staff accounts, deactivate
- Trekker management: activate/deactivate
- Booking management: view all bookings, cancel a booking
- Cross-entity search (treks, staff, trekkers, bookings)
- Visual reports (Chart.js — trek status, booking status, user counts)
- Edit own profile and change password

**System-wide**
- JWT-based authentication with role-based access control (RBAC)
- Soft-delete design throughout — no data is ever hard-deleted; status fields track lifecycle state instead, preserving a full audit trail
- Cascading status logic — deactivating a trekker invalidates their active bookings; deactivating a staff member unassigns them from their treks; closing a trek invalidates its bookings
- Server-side response caching (Flask-Caching + Redis) demonstrated on one endpoint

---

## Tech Stack

**Backend**
- Flask
- Flask-SQLAlchemy (ORM) — SQLite database
- Flask-JWT-Extended — token-based authentication
- Flask-CORS
- Flask-Caching + Redis — response caching

**Frontend**
- Vue 3 (Vite)
- Vue Router — nested, role-based routing with navigation guards
- Axios — HTTP client
- Bootstrap 5 + Bootstrap Icons
- Chart.js — admin reports visualizations

---

## Project Structure

```
Trekking-Management-App/
├── backend/
│   ├── app.py            # Flask app entry point — all API routes
│   ├── models.py         # SQLAlchemy models: User, Trek, Booking
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── views/
│   │   │   ├── trekker/
│   │   │   ├── staff/
│   │   │   └── admin/
│   │   ├── components/
│   │   │   ├── layout/       # TrekkerLayout, StaffLayout, AdminLayout
│   │   │   ├── BookTrekModal.vue
│   │   │   └── ParticipantsModal.vue
│   │   ├── router/
│   │   │   └── index.js
│   │   ├── App.vue
│   │   └── main.js
│   └── package.json
└── README.md
```

---

## Database Schema

- **User** — `id, username, password_hash, role, is_active, fname, lname, age, language, phone, email`
- **Trek** — `id, assigned_staff_id, name, location, description, start_date, end_date, duration, length, difficulty, status, min_age, max_age, total_slots, available_slots, price`
- **Booking** — `id, user_id, trek_id, booking_date, payment_status, booking_status`

**Relationships**
- User (staff) → Trek: one-to-many, via `assigned_staff_id`
- User (trekker) → Booking: one-to-many
- Trek → Booking: one-to-many

`Trek.status`: `open`, `sold_out`, `completed`, `closed` 

`Booking.booking_status`: `booked`, `cancelled`, `completed`, `invalidated`

---

## Setup & Installation

### Prerequisites
- Python 3.10+
- Node.js 18+
- Redis (for caching)

### Backend

```bash
cd backend
pip install -r requirements.txt
python3 app.py
```

The Flask server runs on `http://127.0.0.1:5000`. On first run, it creates the database and a default admin account (`admin` / `admin`).

### Frontend

```bash
cd frontend
npm install
npm run dev
```

The Vite dev server runs on `http://localhost:5173`.

### Redis (for caching)

```bash
sudo service redis-server start
```

Verify it's running with `redis-cli ping` (should return `PONG`).

---

## Authentication & Authorization

- **Authentication**: JWT tokens issued at login (`Flask-JWT-Extended`), stored in `localStorage` on the frontend, sent as `Authorization: Bearer <token>` on protected requests.
- **Authorization (RBAC)**: enforced at two layers —
  - **Frontend** — Vue Router navigation guards check role metadata before rendering a route (UX layer only)
  - **Backend** — every protected route re-verifies the user's role from the database via `@admin_required` / `@staff_required` decorators, plus object-level checks where relevant (e.g., a staff member can only view participants for treks assigned specifically to them)

The frontend guard is not a security boundary by itself — the backend is the authoritative enforcement layer.

---

## Design Notes

- **No hard deletes.** Every "delete" action in the UI is a soft-delete: closing a trek, deactivating a user. This preserves historical/audit data rather than discarding it.
- **Modals over navigation.** Booking a trek and viewing participant details happen via Bootstrap modals in place, rather than routing to a new page.
- **Per-file API base URL.** Each Vue file defines its own `API_BASE_URL` constant rather than a shared API client module, favoring simplicity and self-contained files for this project's scope.

---

## Author

Vaishnavi Saxena
IIT Madras BS Degree Program
