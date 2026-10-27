# 🏥 MediConnect — Healthcare Backend & Management Portal

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg?logo=python&logoColor=white)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-4.2-092E20.svg?logo=django&logoColor=white)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/DRF-3.16-red.svg?logo=django&logoColor=white)](https://www.django-rest-framework.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-17-336791.svg?logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![JWT Auth](https://img.shields.io/badge/JWT-SimpleJWT-black.svg?logo=jsonwebtokens&logoColor=white)](https://django-rest-framework-simplejwt.readthedocs.io/)
[![Swagger / OpenAPI](https://img.shields.io/badge/OpenAPI-3.0-85EA2D.svg?logo=swagger&logoColor=black)](https://swagger.io/)
[![Tests](https://img.shields.io/badge/Tests-28%20Passed-brightgreen.svg)]()
[![License](https://img.shields.io/badge/License-MIT-blue.svg)]()

A robust, production-grade backend system and interactive management portal for healthcare applications built with **Django**, **Django REST Framework (DRF)**, **PostgreSQL**, and **JWT Authentication** (`djangorestframework-simplejwt`).

The system enables secure user registration, token-based login, patient and doctor record management, and doctor-to-patient assignment mappings with granular permissions, comprehensive validation, and an integrated responsive web UI.

---

## 📑 Table of Contents

- [🌟 Features](#-features)
- [🛠 Tech Stack](#-tech-stack)
- [📁 Project Structure](#-project-structure)
- [🚀 Quick Start Guide](#-quick-start-guide)
  - [Prerequisites](#prerequisites)
  - [Installation & Setup](#installation--setup)
  - [PostgreSQL Database Setup](#postgresql-database-setup)
  - [Migrations & Demo Data Seeding](#migrations--demo-data-seeding)
  - [Run the Server](#run-the-server)
- [🖥 Built-in Web Portal (UI)](#-built-in-web-portal-ui)
- [📖 API Documentation & Swagger](#-api-documentation--swagger)
- [📡 Complete API Reference](#-complete-api-reference)
  - [1. Authentication APIs](#1-authentication-apis)
  - [2. Patient Management APIs](#2-patient-management-apis)
  - [3. Doctor Management APIs](#3-doctor-management-apis)
  - [4. Patient-Doctor Mapping APIs](#4-patient-doctor-mapping-apis)
- [🧪 Automated Testing](#-automated-testing)
- [📮 Postman Collection](#-postman-collection)
- [⚙️ Environment Variables Reference](#️-environment-variables-reference)
- [📄 License](#-license)

---

## 🌟 Features

- **🔐 Secure JWT Authentication**:
  - Email-based authentication with encrypted passwords (PBKDF2-SHA256).
  - Access token and refresh token rotation via `djangorestframework-simplejwt`.
- **👥 Patient Management**:
  - Authenticated users can register and manage patient records.
  - Data isolation: users retrieve and manage only the patients they created.
  - Field validations: age constraints ($0-130$), international phone regex, gender choices.
- **🩺 Doctor Management**:
  - Full CRUD operations for clinical practitioners.
  - Profile attributes: name, clinical specialization, experience, verified email, and phone.
- **🔗 Doctor-to-Patient Mapping**:
  - Assign specialists to patients with clinical consultation notes.
  - System-wide mapping retrieval as well as patient-specific doctor queries (`GET /api/mappings/<patient_id>/`).
  - Database-enforced composite unique constraint prevents duplicate assignments.
  - Unassign/remove mappings by ID (`DELETE /api/mappings/<id>/`).
- **🎨 Modern Web UI (MediConnect)**:
  - Responsive Single-Page Application (SPA) served right at root `/`.
  - Built with Tailwind CSS and Lucide icons.
  - 1-click demo login buttons, live search filters, modals, and real-time toast feedback.
- **📚 Interactive API Documentation**:
  - Swagger UI (`/api/docs/`), ReDoc (`/api/redoc/`), and OpenAPI 3 schema (`/api/schema/`).
- **🛡️ Standardized Error Handling**:
  - Consistent JSON error payloads across validation failures, authentication issues, and 404s.

---

## 🛠 Tech Stack

| Component | Technology | Version |
|---|---|---|
| **Backend Framework** | Django | 4.2+ |
| **REST API Engine** | Django REST Framework (DRF) | 3.16+ |
| **Database** | PostgreSQL | 14+ / 17 |
| **Database Driver** | psycopg2-binary | 2.9+ |
| **Authentication** | djangorestframework-simplejwt | 5.5+ |
| **API Documentation** | drf-spectacular (OpenAPI 3) | 0.30+ |
| **Frontend UI** | HTML5, Tailwind CSS, Lucide, ES6+ | — |
| **Configuration** | python-dotenv | 1.2+ |

---

## 📁 Project Structure

```
MediConnect/
├── config/
│   ├── settings.py             # PostgreSQL, JWT, DRF & Swagger settings
│   ├── urls.py                 # Root router (UI, Admin, Swagger, APIs)
│   ├── wsgi.py
│   └── asgi.py
├── apps/
│   ├── authentication/         # Custom User model, Register & Login APIs
│   │   ├── models.py, serializers.py, views.py, urls.py, admin.py
│   ├── patients/               # Patient model, creator-scoped CRUD & permissions
│   │   ├── models.py, serializers.py, views.py, urls.py, permissions.py, admin.py
│   ├── doctors/                # Doctor model, CRUD views & validations
│   │   ├── models.py, serializers.py, views.py, urls.py, admin.py
│   ├── mappings/               # PatientDoctorMapping model & assignment views
│   │   ├── models.py, serializers.py, views.py, urls.py, admin.py
│   └── common/                 # Custom error handler & seed_data command
│       ├── exceptions.py, management/commands/seed_data.py
├── templates/
│   └── index.html              # Modern MediConnect web dashboard SPA
├── tests/                      # Automated test suite (28 tests, 100% pass)
│   ├── test_auth.py
│   ├── test_patients.py
│   ├── test_doctors.py
│   └── test_mappings.py
├── postman_collection.json     # Ready-to-import Postman 2.1 collection
├── requirements.txt            # Pinned dependencies
├── .env.example                # Environment variables template
├── .env                        # Active environment configuration
└── manage.py
```

---

## 🚀 Quick Start Guide

### Prerequisites
- **Python 3.9+**
- **PostgreSQL 14+**
- **Git**

### Installation & Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/<your-username>/MediConnect.git
   cd MediConnect
   ```

2. **Create and activate a virtual environment**:
   ```bash
   # On macOS/Linux:
   python3 -m venv venv
   source venv/bin/activate

   # On Windows:
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

### PostgreSQL Database Setup

1. Ensure your PostgreSQL server is running. On macOS with Homebrew:
   ```bash
   brew services start postgresql@17
   ```

2. Create the project database:
   ```bash
   psql -U <your_postgres_user> -c "CREATE DATABASE healthcare_db;"
   ```

3. Configure your environment file:
   ```bash
   cp .env.example .env
   ```
   Open `.env` and verify database credentials:
   ```ini
   DB_NAME=healthcare_db
   DB_USER=your_postgres_user
   DB_PASSWORD=your_postgres_password
   DB_HOST=127.0.0.1
   DB_PORT=5432
   ```

### Migrations & Demo Data Seeding

1. **Apply database migrations**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

2. **Seed sample healthcare data** (creates admin, demo doctors, patients, and assignments):
   ```bash
   python manage.py seed_data
   ```

### Run the Server

```bash
python manage.py runserver
```

The application is now running at **`http://127.0.0.1:8000/`**.

---

## 🖥 Built-in Web Portal (UI)

Open **`http://127.0.0.1:8000/`** in your browser. The portal provides:

- **Instant 1-Click Demo Logins**:
  - 👩‍⚕️ **Dr. Sarah**: `dr.sarah@healthcare.com` / `DoctorPass123!`
  - 👨‍⚕️ **Nurse John**: `nurse.john@healthcare.com` / `NursePass123!`
  - ⚡ **Administrator**: `admin@healthcare.com` / `AdminPassword123!`
- **Dashboard Overview**: Metrics, PostgreSQL status, recent activity.
- **Patients Management**: Search, add, edit, and delete patients; inspect assigned doctors per patient.
- **Doctors Management**: Doctor cards with specialization, experience, and contact details.
- **Assignments**: Assign doctors with clinical notes, filter by patient or doctor, and unassign with one click.
- **Django Admin GUI**: Visual database browser available at [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/).

---

## 📖 API Documentation & Swagger

Interactive OpenAPI documentation is generated automatically:

- **Swagger UI**: [http://127.0.0.1:8000/api/docs/](http://127.0.0.1:8000/api/docs/)
- **ReDoc**: [http://127.0.0.1:8000/api/redoc/](http://127.0.0.1:8000/api/redoc/)
- **OpenAPI 3 JSON Schema**: [http://127.0.0.1:8000/api/schema/](http://127.0.0.1:8000/api/schema/)

---

## 📡 Complete API Reference

All protected endpoints require the HTTP Authorization header:
```http
Authorization: Bearer <your_jwt_access_token>
```

### 1. Authentication APIs

| Method | Endpoint | Description | Auth Required |
|---|---|---|:---:|
| `POST` | `/api/auth/register/` | Register new user with `name`, `email`, `password` | No |
| `POST` | `/api/auth/login/` | Log in user and receive JWT tokens | No |
| `POST` | `/api/auth/token/refresh/` | Obtain a new access token using refresh token | No |

#### `POST /api/auth/register/`
```json
// Request Body
{
  "name": "Dr. Alice Smith",
  "email": "alice@healthcare.com",
  "password": "SecurePassword123!"
}

// Response (201 Created)
{
  "success": true,
  "message": "User registered successfully.",
  "user": {
    "id": 1,
    "name": "Dr. Alice Smith",
    "email": "alice@healthcare.com"
  },
  "tokens": {
    "refresh": "<jwt_refresh_token>",
    "access": "<jwt_access_token>"
  }
}
```

#### `POST /api/auth/login/`
```json
// Request Body
{
  "email": "alice@healthcare.com",
  "password": "SecurePassword123!"
}

// Response (200 OK)
{
  "success": true,
  "message": "Login successful.",
  "user": {
    "id": 1,
    "name": "Dr. Alice Smith",
    "email": "alice@healthcare.com"
  },
  "tokens": {
    "refresh": "<jwt_refresh_token>",
    "access": "<jwt_access_token>"
  }
}
```

---

### 2. Patient Management APIs

| Method | Endpoint | Description | Auth Required |
|---|---|---|:---:|
| `POST` | `/api/patients/` | Add a new patient record | Yes |
| `GET` | `/api/patients/` | Retrieve all patients created by the authenticated user | Yes |
| `GET` | `/api/patients/<id>/` | Get details of a specific patient | Yes (Creator/Admin) |
| `PUT` | `/api/patients/<id>/` | Update patient details | Yes (Creator/Admin) |
| `DELETE` | `/api/patients/<id>/` | Delete a patient record | Yes (Creator/Admin) |

#### `POST /api/patients/`
```json
// Request Body
{
  "name": "Arthur Dent",
  "age": 42,
  "gender": "Male",
  "contact_number": "+1-555-4242",
  "email": "arthur.dent@example.com",
  "address": "42 Galactica Way, Cityville",
  "medical_history": "Stress-induced migraines."
}

// Response (201 Created)
{
  "success": true,
  "message": "Patient created successfully.",
  "data": {
    "id": 1,
    "name": "Arthur Dent",
    "age": 42,
    "gender": "Male",
    "contact_number": "+1-555-4242",
    "created_by": 1,
    "created_by_email": "alice@healthcare.com"
  }
}
```

---

### 3. Doctor Management APIs

| Method | Endpoint | Description | Auth Required |
|---|---|---|:---:|
| `POST` | `/api/doctors/` | Add a new doctor record | Yes |
| `GET` | `/api/doctors/` | Retrieve all doctors | Yes |
| `GET` | `/api/doctors/<id>/` | Get details of a specific doctor | Yes |
| `PUT` | `/api/doctors/<id>/` | Update doctor details | Yes |
| `DELETE` | `/api/doctors/<id>/` | Delete a doctor record | Yes |

#### `POST /api/doctors/`
```json
// Request Body
{
  "name": "Gregory House",
  "specialization": "Diagnostic Medicine",
  "phone": "+1-555-0101",
  "email": "house@diagnostics.org",
  "years_of_experience": 22
}

// Response (201 Created)
{
  "success": true,
  "message": "Doctor added successfully.",
  "data": {
    "id": 1,
    "name": "Gregory House",
    "specialization": "Diagnostic Medicine",
    "phone": "+1-555-0101",
    "email": "house@diagnostics.org",
    "years_of_experience": 22
  }
}
```

---

### 4. Patient-Doctor Mapping APIs

| Method | Endpoint | Description | Auth Required |
|---|---|---|:---:|
| `POST` | `/api/mappings/` | Assign a doctor to a patient | Yes |
| `GET` | `/api/mappings/` | Retrieve all patient-doctor mappings *(supports `?patient_id=` & `?doctor_id=`)* | Yes |
| `GET` | `/api/mappings/<patient_id>/` | Get all doctors assigned to a specific patient | Yes |
| `DELETE` | `/api/mappings/<id>/` | Remove a doctor from a patient *(by mapping ID)* | Yes |

#### `POST /api/mappings/`
```json
// Request Body
{
  "patient": 1,
  "doctor": 2,
  "notes": "Cardiology consult referral."
}

// Response (201 Created)
{
  "success": true,
  "message": "Doctor 'Dr. James Wilson' assigned to patient 'Arthur Dent' successfully.",
  "data": {
    "id": 1,
    "patient": { "id": 1, "name": "Arthur Dent", "age": 42 },
    "doctor": { "id": 2, "name": "James Wilson", "specialization": "Oncology" },
    "notes": "Cardiology consult referral.",
    "assigned_at": "2026-10-27T10:00:00Z"
  }
}
```

#### `GET /api/mappings/<patient_id>/`
```json
// Response (200 OK)
{
  "patient_id": 1,
  "patient_name": "Arthur Dent",
  "patient_gender": "Male",
  "patient_age": 42,
  "total_assigned_doctors": 1,
  "assigned_doctors": [
    {
      "mapping_id": 1,
      "doctor_id": 2,
      "name": "James Wilson",
      "specialization": "Oncology",
      "phone": "+1-555-0102",
      "email": "wilson@oncology.org",
      "years_of_experience": 19,
      "notes": "Cardiology consult referral.",
      "assigned_at": "2026-10-27T10:00:00Z"
    }
  ]
}
```

---

## 🧪 Automated Testing

The project includes **28 comprehensive automated unit and integration tests** covering:
- User registration, password validation rules, and duplicate user rejections.
- User authentication, JWT issuance, and token refresh.
- Scoped patient listings (ensuring users only see patients they created).
- Object-level permissions preventing unauthorized edits or deletions.
- Doctor CRUD operations and email uniqueness.
- Patient-Doctor assignments, duplicate mapping rejection, and unassignments.

Run the test suite:
```bash
python manage.py test
```

Expected output:
```text
Found 28 test(s).
Creating test database for alias 'default'...
............................
----------------------------------------------------------------------
Ran 28 tests in 5.254s

OK
Destroying test database for alias 'default'...
```

---

## 📮 Postman Collection

A pre-configured Postman 2.1 Collection is included in the project root: [`postman_collection.json`](./postman_collection.json).

### How to use:
1. Open Postman, click **Import**, and select `postman_collection.json`.
2. The collection is configured with variable `baseUrl = http://127.0.0.1:8000`.
3. Execute **1. Authentication -> Login User** or **Register User**.
4. The Postman test script **automatically extracts and sets the JWT access token** in the collection variable `jwt_token`.
5. All subsequent requests in Patient, Doctor, and Mapping folders will automatically use this Bearer token!

---

## ⚙️ Environment Variables Reference

| Variable | Default Value | Description |
|---|---|---|
| `SECRET_KEY` | *(django secret key)* | Django cryptographic signing key |
| `DEBUG` | `True` | Debug mode (`True` for local development, `False` for production) |
| `ALLOWED_HOSTS` | `localhost,127.0.0.1` | Comma-separated list of valid hostnames |
| `DB_NAME` | `healthcare_db` | PostgreSQL database name |
| `DB_USER` | `avnishsingh` | PostgreSQL database username |
| `DB_PASSWORD` | `""` | PostgreSQL database password |
| `DB_HOST` | `127.0.0.1` | Database host |
| `DB_PORT` | `5432` | Database port |
| `ACCESS_TOKEN_LIFETIME_MINUTES` | `60` | JWT Access Token validity duration in minutes |
| `REFRESH_TOKEN_LIFETIME_DAYS` | `7` | JWT Refresh Token validity duration in days |

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).
