# TodoApp Repository Architecture

A layered Python backend project built with:
- FastAPI
- Repository Pattern
- SQLite
- Service Layer
- Domain Logic
- Pytest

## Features
- Create todo items
- Toggle done state
- Set priority
- Delete items
- Search items
- REST API with FastAPI
- Repository-based persistence layer

## Architecture
```text
API
 ↓
Service
 ↓
Repository
 ↓
SQLite
```
## Tech Stack
- Python
- FastAPI
- Uvicorn
- SQLite
- Pytest
## Live API

https://todoapp-repository-architecture-1.onrender.com/docs

## Run locally
```bash
pip install -r requirements.txt
uvicorn todo.api:app --reload
```

## Learning Goals
This project was created to practice:

- backend architecture
- repository pattern
- FastAPI
- layered application design
- testing
- deployment workflow
