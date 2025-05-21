# 🧪 Flask API Test Setup

This project contains a lightweight Flask API along with automated tests using `pytest`. Follow the steps below to set up your environment, run the server, and execute the tests.

---

## ✅ Prerequisites

- Python 3.7 or higher
- `virtualenv` (recommended for isolated environments)

---

## 🚀 Setup & Run Instructions

### Step 1: Create and Activate Virtual Environment

```bash
python3 -m venv venv
```
### Step 2: Install Dependencies

```bash 
pip install -r requirements.txt
```

### Step 3: Run the Flask Server

```bash 
python3 api/test_api.py
```
Once the server starts, you should see:

```bash 
 * Running on http://127.0.0.1:5000/
```

### Step 4:  Run Tests with Pytest

```bash 
pytest tests/test_example.py
```

