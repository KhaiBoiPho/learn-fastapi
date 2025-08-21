# Learn FastAPI

This repository contains my personal learning notes and practice code for **FastAPI**, a modern, fast (high-performance) web framework for building APIs with Python.

---

## Contents

* Basic examples: creating simple endpoints (`GET`, `POST`)
* Path parameters & query parameters
* Request body & data validation with **Pydantic**
* Response models and error handling
* Middleware and dependency injection
* Small demo

---

## Tech Stack

* Python 3.10+
* FastAPI
* Uvicorn (ASGI server)

---

## How to Run

1. Clone the repository:

   ```bash
   git clone https://github.com/KhaiBoiPho/learn-fastapi.git
   cd learn-fastapi
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Start the server:

   ```bash
   uvicorn main:app --reload
   ```

4. Open your browser at:

   ```
   http://127.0.0.1:8000
   ```

   and check the interactive API docs at:

   ```
   http://127.0.0.1:8000/docs
   ```

---

## Notes

* This repo is for **learning purposes only**.
* Not intended for production use.

---
