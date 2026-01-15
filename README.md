# Spy Cat Agency - Full Stack Project

## Overview
This is the **Spy Cat Agency (SCA)** project, a full-stack application to manage spy cats, missions, and targets.  
It includes:  

- **Backend**: FastAPI REST API with SQLite database  
- **Frontend**: Next.js dashboard to manage spy cats  
- **Postman Collection** to test all API endpoints  

---

## Backend

### Overview
The backend API allows:  
- CRUD operations for Spy Cats  
- CRUD operations for Missions and Targets  
- Assigning Cats to Missions  
- Updating target notes with validation  
- Cat breed validation using [TheCatAPI](https://thecatapi.com)  

### Requirements
- Python 3.10+  
- Dependencies listed in `requirements.txt`  

## Install dependencies:

```bash
pip install -r requirements.txt
```
# Running the Backend

1. Go to the backend folder:

```bash
cd backend
```
## Start the FastAPI server:

```bash
uvicorn main:app --reload
```
## Access the API at:

http://127.0.0.1:8000

## Interactive API docs:

http://127.0.0.1:8000/docs

# API Endpoints
## Cats

    GET /cats → list all cats

    POST /cats → create a new cat

    GET /cats/{id} → get cat by ID

    PATCH /cats/{id} → update cat salary

    DELETE /cats/{id} → delete cat

## Missions & Targets

    POST /missions → create mission with targets

    POST /missions/{id}/assign/{cat_id} → assign a cat

    PATCH /targets/{id} → update target notes / complete state

    DELETE /missions/{id} → delete mission (if not assigned)

## Postman Collection

A ready-to-use Postman collection is included:

SpyCatAgency.postman_collection.json

You can import it into Postman or Postman Web to test all endpoints.
Frontend
Overview

A simple Next.js dashboard for Spy Cat Agency to manage spy cats.
Supports:

    List all spy cats

    Add new spy cat

    Edit salary of existing cats

    Delete cats

    Breed dropdown to prevent invalid breed names

# Running the Frontend


## Navigate to the frontend folder:
```bash
cd spy-cat-frontend
```
## Install dependencies:

```bash
npm install
```
## Start the development server:

```bash
npm run dev
```
## Open the dashboard in your browser:

http://localhost:3000

## Notes

    The frontend fetches data from the backend at http://127.0.0.1:8000

    The breed dropdown is fetched from TheCatAPI

    All form inputs have validation:

        Name cannot be empty or only numbers

        Experience and Salary must be positive

        Breed must be selected

## Project Structure
```bash
spy-cat/
├─ backend/
│  ├─ main.py
│  ├─ models.py
│  ├─ schemas.py
│  ├─ database.py
│  ├─ requirements.txt
│  └─ SpyCatAgency.postman_collection.json
├─ spy-cat-frontend/
│  ├─ pages/
│  │  └─ index.js
│  ├─ package.json
│  └─ ...
└─ README.md
```