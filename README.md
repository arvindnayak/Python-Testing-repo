# Complete Web UI and API Test Automation Framework

This repository contains a comprehensive test automation framework built with Python and Pytest. It is designed to test both the Web UI of a sample e-commerce application and a custom backend REST API built with Flask and PostgreSQL.

The project incorporates industry best practices like the Page Object Model (POM) for UI testing, direct database validation for API testing, and Continuous Integration (CI) via GitHub Actions.

---

## 🚀 Automation Scope & Features

### 1. Web UI Automation (Selenium WebDriver)
The UI tests are built using Selenium WebDriver and validate the frontend of `https://tutorialsninja.com/demo/`. The framework leverages the **Page Object Model (POM)** design pattern for maintainability and uses `conftest.py` for centralized browser setup (running Headless Chrome).

**Covered UI Scenarios:**
*   **Search Functionality:**
    *   Searching for a valid product (e.g., 'HP') and verifying product display.
    *   Searching for an invalid product and verifying the "no product matches" message.
    *   Empty search input validation.
*   **User Registration:**
    *   Attempting to register with an already existing email.
    *   Validating the warning message for duplicate email registrations.
*   **User Login:**
    *   Successful login with valid credentials.
    *   Failed login attempts with invalid email, invalid password, and empty credentials (using Pytest parametrization for data-driven testing).

### 2. API Automation (Requests & PostgreSQL)
The backend automation tests a custom Flask REST API (`/api/items`) backed by a PostgreSQL database. It validates HTTP responses and performs **direct database assertions** using `psycopg2` to guarantee data integrity.

**Covered API Scenarios (CRUD Operations):**
*   **GET /api/items:**
    *   Fetch all items (Validates 200 OK and response list structure).
    *   Fetch item by specific ID (Validates 200 OK).
    *   Invalid formats and non-existent IDs (Validates 404 Not Found).
*   **POST /api/items:**
    *   Successfully create an item (Validates 201 Created and response payload).
    *   **DB Verification:** Queries PostgreSQL directly to ensure the item was genuinely inserted.
    *   Missing required fields and empty payloads (Validates 400 Bad Request).
*   **PUT /api/items/<id>:**
    *   Complete replacement of an item.
    *   **DB Verification:** Asserts that all columns in the DB reflect the updated payload.
    *   Missing name or non-existent items (Validates 400/404).
*   **PATCH /api/items/<id>:**
    *   Partial update (e.g., updating only the price).
    *   **DB Verification:** Ensures targeted fields are updated while keeping others untouched.
*   **DELETE /api/items/<id>:**
    *   Successful deletion of an item.
    *   **DB Verification:** Confirms the record is completely purged from the PostgreSQL table.
    *   Verification that a subsequent GET request returns 404.
*   **Edge Cases:**
    *   Validating disallowed HTTP methods (e.g., POST to a specific item ID returns 405 Method Not Allowed).

### 3. CI/CD Integration (GitHub Actions)
The project includes a GitHub Actions workflow (`api_tests.yml`) to automatically execute the API test suite on any `push` or `pull_request` to the `main` branch. 
*   Configures a Python 3.10 environment on `ubuntu-latest`.
*   Installs dependencies dynamically.
*   Injects database and API credentials securely via GitHub Secrets.

---

## 🛠️ Tech Stack & Libraries

*   **Language:** Python 3.10
*   **Test Runner:** Pytest
*   **UI Automation:** Selenium WebDriver
*   **API Automation:** Requests
*   **Database Interaction:** Psycopg2 (PostgreSQL)
*   **Backend Application:** Flask (included in the repository for testing)
*   **CI/CD:** GitHub Actions

---

## ⚙️ Setup and Execution

### Prerequisites
Ensure you have Python installed and run the following to install requirements:
```bash
pip install pytest selenium requests psycopg2-binary flask
```

### Running UI Tests
The UI tests execute against the public TutorialsNinja demo site.
```bash
pytest Web_tester_pkg/Test/test_search.py Web_tester_pkg/Test/test_login.py Web_tester_pkg/Test/test_register.py -v
```

### Running API Tests
Ensure your local PostgreSQL server is running and the schema is created using `database_schema.sql`. Start the Flask API server (`flask_api.py`), then run:
```bash
pytest Web_tester_pkg/Test/test_api.py -v
```
