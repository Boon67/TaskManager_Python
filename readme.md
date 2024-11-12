# Task Management REST API
This is a task management REST API built using Python, FastAPI, and SQLAlchemy. It follows the clean architecture and repository pattern principles to ensure separation of concerns, maintainability, and testability.

## Features
- Create, read, update, and delete tasks
- Mark tasks as complete
- Get a list of all tasks
- Get details of a specific task

## Architecture

The application is structured into the following layers:

1. **Domain Layer**:
   - Contains the core business entities (`Task`) and repository interfaces
   - Defines the business rules and behaviors

2. **Infrastructure Layer**:
   - Implements the repository interface using SQLAlchemy
   - Handles database operations and data persistence

3. **Application Layer**:
   - Contains use cases that orchestrate the flow of data
   - Implements business logic using domain entities
   - Uses DTOs for data transfer

4. **Presentation Layer**:
   - FastAPI controllers handling HTTP requests
   - Routes for CRUD operations and task completion

## Getting Started

### Prerequisites

- Python 3.9 or higher
- SQLite (or any other SQL database supported by SQLAlchemy)

### Installation

1. Clone the repository:


Install dependencies from requirements.txt
Run uvicorn app.main:app --reload
Access the API docs at http://localhost:8000/docs