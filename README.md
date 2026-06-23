# FastAPI & Pydantic Practice Project

## Overview

This project is a hands-on implementation of **FastAPI** and **Pydantic** concepts. It demonstrates API development, request validation, nested models, custom validators, query parameters, path parameters, and exception handling.

The project uses patient data stored in a JSON file and provides endpoints to view, search, and sort patient records.

---

## Features

* REST API development using FastAPI
* Path Parameters and Query Parameters
* Custom HTTP Exception Handling
* JSON Data Management
* Nested Pydantic Models
* Email and URL Validation
* Field Constraints using `Field()`
* Custom Validation using `field_validator`
* Automatic API Documentation with Swagger UI

---

## API Endpoints

### Home

```http
GET /
```

Returns a welcome message.

### About

```http
GET /about
```

Returns a simple response about the application.

### View All Patients

```http
GET /view
```

Displays all patient records stored in `patients.json`.

### Get Patient by ID

```http
GET /patient/{patient_id}
```

Example:

```http
GET /patient/P001
```

Returns details of the requested patient.

### Sort Patients

```http
GET /sort?sort_by=weight&order=desc
```

Supported fields:

* height
* weight
* bmi

Supported orders:

* asc
* desc

---

## Pydantic Models

### Address Model

```python
class Address(BaseModel):
    city: str
    state: str
    pincode: int
```

### Patient Model

```python
class Patient(BaseModel):
    name: str
    age: int
    address: Address
    email: EmailStr
```

Demonstrates nested model validation using Pydantic.

---

## Field Validation

```python
age: int = Field(gt=0, lt=100)
weight: float = Field(gt=0, strict=True)
```

Validation Rules:

* Age must be between 0 and 100
* Weight must be greater than 0
* Strict type checking enabled

---

## Custom Validators

### Email Domain Validation

```python
@field_validator('email')
@classmethod
def email_validator(cls, value):
```

Allowed domains:

* hdfc.com
* icici.com

Example:

```text
✓ abc@hdfc.com
✗ abc@gmail.com
```

### Name Transformation

```python
@field_validator('name')
@classmethod
def transform_name(cls, value):
    return value.upper()
```

Automatically converts names to uppercase.

### Age Validation

```python
@field_validator('age')
@classmethod
def validate_age(cls, value):
```

Ensures age is within the valid range.

---

## Technologies Used

* Python
* FastAPI
* Pydantic
* Uvicorn
* JSON

---

## Installation

Install required packages:

```bash
pip install fastapi uvicorn pydantic email-validator
```

Run the application:

```bash
uvicorn main:app --reload
```

---

## API Documentation

FastAPI automatically generates interactive API documentation.

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
* Building REST APIs
* Request validation using Pydantic
* Nested Models
* Query & Path Parameters
* Custom Validators
* Exception Handling
* API Documentation Generation
* Working with JSON Data

```
```
