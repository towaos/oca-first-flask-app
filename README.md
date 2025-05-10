# Flask App with Docker and Virtual Environment

This project provides a minimal Flask application setup using a Python virtual environment and Docker Compose.

## Getting Started

### 1. Set Up Virtual Environment

Create and activate the virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. Install Dependencies

Install Flask & mysql-connector-python:

```bash
pip install flask
pip install mysql-connector-python
```

### 3. Build and Run with Docker Compose

Start the application with Docker Compose:

```bash
docker compose up --build
```
### 4. Shut Down the Application

Stop and remove the containers:

```bash
docker compose down
```

### 5. Exit the Virtual Environment

Deactivate the virtual environment:

```bash
deactivate
```