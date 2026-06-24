# Patient Management API using FastAPI

## Overview

A RESTful Patient Management API built using **FastAPI** and **Pydantic**. This project demonstrates CRUD operations, request validation, computed fields, query parameters, path parameters, and JSON-based data persistence.

Patient records are stored in a local `patients.json` file and can be created, viewed, updated, deleted, and sorted through API endpoints.

---

## Features

* Create, Read, Update, and Delete (CRUD) patient records
* Data validation using Pydantic models
* Partial updates using a dedicated update schema
* Automatic BMI calculation using computed fields
* BMI health classification (Underweight, Normal, Overweight, Obese)
* Sorting patients by height, weight, or BMI
* Custom error handling using FastAPI HTTP exceptions
* Interactive API documentation with Swagger UI and ReDoc
* JSON-based storage without requiring a database

---

## Project Structure

```text
.
├── main.py
├── patients.json
└── README.md
```

---

## Patient Schema

```python
class Patient(BaseModel):
    id: str
    name: str
    city: str
    age: int
    gender: Literal["male", "female", "others"]
    height: float
    weight: float
```

### Computed Fields

The API automatically calculates:

```python
bmi
bmi_verdict
```

BMI Categories:

| BMI Range   | Verdict     |
| ----------- | ----------- |
| < 18.5      | Underweight |
| 18.5 - 24.9 | Normal      |
| 25 - 29.9   | Overweight  |
| >= 30       | Obese       |

---

## API Endpoints

### Home

```http
GET /
```

Returns a welcome message.

---

### View All Patients

```http
GET /view
```

Returns all patient records.

---

### Get Patient by ID

```http
GET /patient/{patient_id}
```

Example:

```http
GET /patient/P001
```

Returns details of the specified patient.

---

### Create Patient

```http
POST /create
```

Example Request Body:

```json
{
  "id": "P001",
  "name": "Rahul",
  "city": "Bangalore",
  "age": 22,
  "gender": "male",
  "height": 1.75,
  "weight": 72
}
```

---

### Update Patient

```http
PUT /update?patient_id=P001
```

Supports partial updates.

Example Request Body:

```json
{
  "weight": 78
}
```

Only the provided fields are updated.

---

### Delete Patient

```http
DELETE /delete/P001
```

Deletes the specified patient record.

---

### Sort Patients

```http
GET /sort?sort_by=bmi&order=desc
```

Supported Sorting Fields:

* height
* weight
* bmi

Supported Order:

* asc
* desc

Examples:

```http
GET /sort?sort_by=height&order=asc
```

```http
GET /sort?sort_by=weight&order=desc
```

---

## Validation Rules

### Patient Model

| Field  | Validation                |
| ------ | ------------------------- |
| age    | Must be between 1 and 119 |
| height | Must be greater than 0    |
| weight | Must be greater than 0    |
| gender | male, female, or others   |

---

## Technologies Used

* Python
* FastAPI
* Pydantic
* Uvicorn
* JSON

---

## Installation

Clone the repository:

```bash
git clone https://github.com/Dheekshithgr/FastAPI.git
cd FastAPI
```

Install dependencies:

```bash
pip install fastapi uvicorn pydantic
```

Run the application:

```bash
uvicorn main:app --reload
```

Server:

```text
http://127.0.0.1:8000
```

---

## API Documentation

FastAPI automatically generates API documentation.

Swagger UI:

```text
http://127.0.0.1:8000/docs
```

ReDoc:

```text
http://127.0.0.1:8000/redoc
```

---

## Learning Outcomes

Through this project, I learned:

* FastAPI fundamentals
* REST API development
* Pydantic data validation
* Computed fields
* CRUD operations
* Path and Query parameters
* Exception handling
* JSON data persistence
* API documentation generation
* Partial updates using update schemas

```
```
