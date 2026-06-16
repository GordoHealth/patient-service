# Patient Service API
A FastAPI-based microservice for managing patient records, clinical charts, care plans, and medications.

## Setup & Installation

This project relies heavily on `make` commands and Docker for local development and testing. 

### Prerequisites
* Docker and Docker Compose
* pip
* pyenv/pyenv-win
* Python 3.13+ & Pipenv
* `make` utility
* pre-commit

### Local Development
1. **Build and start the containers:**
   ```bash
   make up
```

*This brings up the backend API and the local PostgreSQL database in detached mode.*

2. **Initialize the database and run migrations:**
```bash
make db-setup

```


3. **View Logs:**
```bash
make log-backend
make log-database

```


4. **Access the API:**
* The API runs locally on `http://localhost:3002` (configurable via `APP_PORT`).
* Swagger UI / Docs: `http://localhost:3002/devtools` or `http://localhost:3002/api/latest/docs`



### Testing & Linting

The testing environment uses a dedicated test database profile (`postgres-test`).

* **Run all tests:** `make test`
* **Run unit tests only:** `make test-unit`
* **Run feature tests:** `make test-feature`
* **Check test coverage:** `make coverage`
* **Security & Linting (MyPy, Bandit, Black, Flake8):** `make check-sec`

---


## API Endpoints

The API is versioned and currently accessible under the `/api/v1` or `/api/latest` prefixes.

### System & Health

* `GET /health_check` - Check if the service is alive.
* `GET /status` - Get the database connection status.

### Patients (`/api/v1/patients`)

* `GET /` - Search patients (supports query params: `last_name`, `mrn`, `status`, `date_of_birth`).
* `GET /{patient_id}` - Get a specific patient by their UUID.
* `GET /mrn/{mrn}` - Get a specific patient by their Medical Record Number.
* `POST /` - Create a new patient.
* `PUT /{patient_id}` - Update an existing patient.
* `DELETE /{patient_id}` - Delete a patient.

### Clinical Charts (`/api/v1/clinical-charts`)

* `GET /` - Search clinical charts (supports query param: `patient_id`).
* `GET /{clinical_chart_id}` - Get a clinical chart by its UUID.
* `POST /` - Create a new clinical chart for a patient.
* `PUT /{clinical_chart_id}` - Update a clinical chart.
* `DELETE /{clinical_chart_id}` - Delete a clinical chart.

### Care Plans (`/api/v1/care-plans`)

* `GET /` - Search care plans (supports query params: `patient_id`, `ordering_physician_id`).
* `GET /{care_plan_id}` - Get a care plan by its UUID.
* `POST /` - Create a new care plan.
* `PUT /{care_plan_id}` - Update a care plan.
* `DELETE /{care_plan_id}` - Delete a care plan.

### Medications (`/api/v1/medications`)

* `GET /` - Search the medication catalog (supports query param: `name`).
* `GET /{medication_id}` - Get a medication by its UUID.
* `POST /` - Add a new medication to the catalog.
* `PUT /{medication_id}` - Update medication details.
* `DELETE /{medication_id}` - Delete a medication.

### Patient Medications (`/api/v1/patient-medications`)

* `GET /` - Search patient medications (supports query params: `patient_id`, `medication_id`, `is_discontinued`).
* `GET /{patient_medication_id}` - Get a specific patient medication record.
* `POST /` - Prescribe/assign a medication to a patient.
* `PUT /{patient_medication_id}` - Update a patient's medication record (e.g., mark discontinued).
* `DELETE /{patient_medication_id}` - Remove a patient medication record.

---

## Database Schema (Models)

The service is built around the following core relational models. All entities include common audit fields (`id` (UUID), `created_date`, `last_modified_date`, `created_by`, `last_modified_by`).

| Model | Description | Key Fields |
| --- | --- | --- |
| **Patient** | Core patient demographic data. | `first_name`, `last_name`, `date_of_birth`, `status` (active, discharged, on_hold), `mrn` (Medical Record Number - Unique) |
| **CarePlan** | Prescribed care plans linked to a patient. | `patient_id` (FK), `ordering_physician_id`, `start_date`, `end_date`, `frequency_description` |
| **ClinicalChart** | 1-to-1 chart mapping for a patient. | `patient_id` (FK - Unique), `allergies` (JSONB), `advance_directives`, `dietary_restrictions` |
| **Medication** | Medication catalog/dictionary. | `name`, `dosage`, `frequency`, `route` |
| **PatientMedication** | Many-to-many join mapping patients to active/discontinued meds. | `patient_id` (FK), `medication_id` (FK), `start_date`, `end_date`, `is_discontinued` |

---

## Migrations (Alembic)

Database migrations are managed via Alembic inside the Docker container.

* **Generate a new migration:** `make generate-migration message="your description"`
* **Apply all migrations:** `make migrate`
* **Upgrade N steps:** `make upgrade count=1`
* **Downgrade N steps:** `make downgrade count=1`

```

```