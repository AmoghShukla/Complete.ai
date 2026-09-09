# Complete.AI

Complete.AI is an AI-powered productivity and task management backend built with FastAPI. It provides a structured platform for managing tasks, categories, tags, reminders, authentication, and AI-powered functionality through a modular backend architecture.

The project is designed with scalability and maintainability in mind, separating core infrastructure from individual application features.

## Features

* User authentication and authorization
* JWT-based authentication
* Task management
* Task categorization
* Tag management
* Reminder management
* Background reminder worker
* AI-powered functionality
* PostgreSQL database integration
* Redis integration
* Asynchronous database operations
* Database migrations with Alembic
* WebSocket support
* Pydantic-based validation and configuration
* Modular feature-based architecture
* API documentation through FastAPI

## Tech Stack

| Technology        | Purpose                                      |
| ----------------- | -------------------------------------------- |
| Python 3.11+      | Backend language                             |
| FastAPI           | Web framework                                |
| Uvicorn           | ASGI server                                  |
| PostgreSQL        | Primary database                             |
| SQLAlchemy        | ORM and database abstraction                 |
| AsyncPG           | Asynchronous PostgreSQL driver               |
| Redis             | Caching and asynchronous application support |
| Alembic           | Database migrations                          |
| Pydantic          | Data validation and serialization            |
| Pydantic Settings | Configuration management                     |
| PyJWT             | JWT authentication                           |
| Argon2            | Password hashing                             |
| Boto3             | AWS service integration                      |
| Pydantic AI       | AI application integration                   |
| WebSockets        | Real-time communication                      |

The project dependencies and Python version are defined in `pyproject.toml`.

## Architecture

The backend follows a modular feature-based structure:

```text
Complete.ai/
│
├── alembic/
│   └── Database migration files
│
├── backend/
│   │
│   ├── core/
│   │   ├── base.py
│   │   ├── config.py
│   │   ├── dependencies.py
│   │   └── session.py
│   │
│   ├── features/
│   │   ├── ai/
│   │   ├── auth/
│   │   ├── categories/
│   │   ├── reminders/
│   │   ├── tags/
│   │   └── tasks/
│   │
│   ├── jobs/
│   │   └── reminders.py
│   │
│   ├── models/
│   │
│   ├── utilities/
│   │
│   └── main.py
│
├── .gitignore
├── alembic.ini
├── poetry.lock
├── pyproject.toml
└── run.py
```

The application entry point is `backend.main:app`, with the individual application domains exposed through separate routers.

## Application Modules

### Authentication

The authentication module handles user authentication and authorization using JWT-based security and secure password hashing.

### Tasks

The task module provides the core task-management functionality.

Typical task operations include:

* Creating tasks
* Updating tasks
* Deleting tasks
* Retrieving tasks
* Managing task state
* Associating tasks with categories and tags

### Categories

Categories provide a way to organize tasks into logical groups.

### Tags

Tags allow more flexible classification and filtering of tasks.

### Reminders

The reminder system allows tasks or other application events to be associated with scheduled reminders.

A background worker continuously processes reminders using a configurable polling interval.

### AI

The AI module provides the foundation for integrating AI capabilities into the productivity system using Pydantic AI and OpenAI-compatible models.

This layer is separated from the rest of the application so that AI functionality can evolve independently from the core task-management system.

## Requirements

Before running the project, make sure you have:

* Python 3.11 or higher
* PostgreSQL
* Redis
* Poetry
* Git

## Installation

Clone the repository:

```bash
git clone https://github.com/AmoghShukla/Complete.ai.git
cd Complete.ai
```

Install the dependencies using Poetry:

```bash
poetry install
```

Activate the virtual environment:

```bash
poetry shell
```

## Environment Variables

Create a `.env` file in the project root.

Example:

```env
DATABASE_URL=postgresql+asyncpg://username:password@localhost:5432/complete_ai

REDIS_URL=redis://localhost:6379

SECRET_KEY=your-secret-key
ALGORITHM=HS256

REMINDER_POLL_INTERVAL_SECONDS=60

OPENAI_API_KEY=your-openai-api-key
```

Use values appropriate for your local environment.

Do not commit `.env` files or API keys to the repository.

## Database Setup

Make sure PostgreSQL is running and the database specified in your configuration exists.

Run the Alembic migrations:

```bash
poetry run alembic upgrade head
```

To create a new migration after modifying the database models:

```bash
poetry run alembic revision --autogenerate -m "describe your change"
```

Then apply the migration:

```bash
poetry run alembic upgrade head
```

## Running the Application

Start the development server with:

```bash
poetry run python run.py
```

The application starts on:

```text
http://localhost:8000
```

The project uses Uvicorn with hot reload enabled during development.

You can also start the application directly with Uvicorn:

```bash
poetry run uvicorn backend.main:app --reload --port 8000
```

## API Documentation

Once the application is running, FastAPI automatically provides interactive API documentation.

Swagger UI:

```text
http://localhost:8000/docs
```

ReDoc:

```text
http://localhost:8000/redoc
```

## Health Check

The root endpoint can be used to verify that the application is running:

```http
GET /
```

Example response:

```json
{
  "message": "Congratulations, Your Application is up and running!!"
}
```

The endpoint is registered as the application's health endpoint.

## Database

Complete.AI uses PostgreSQL as its primary relational database.

SQLAlchemy is used as the ORM with asynchronous database support through AsyncPG.

Database schema changes are managed through Alembic migrations.

```text
Application
     |
     v
FastAPI
     |
     v
SQLAlchemy
     |
     v
AsyncPG
     |
     v
PostgreSQL
```

## Redis

Redis is used as an application infrastructure component and is configured independently from the PostgreSQL database.

```text
Complete.AI
     |
     +---- PostgreSQL
     |
     +---- Redis
```

## Background Jobs

The application includes a background reminder worker that starts with the FastAPI application lifecycle.

The worker runs asynchronously and uses a configurable polling interval to process reminders.

The worker is automatically started when the application starts and gracefully stopped when the application shuts down.

## Development

Run the application in development mode:

```bash
poetry run python run.py
```

After making code changes, the development server automatically reloads.

For database changes:

```bash
poetry run alembic revision --autogenerate -m "your migration message"
poetry run alembic upgrade head
```

## Project Design Principles

Complete.AI is structured around several principles:

### Separation of Concerns

Application functionality is separated into independent feature modules rather than placing all endpoints and business logic into a single application file.

### Async First

The backend uses asynchronous database access and asynchronous application components where appropriate.

### Modular Features

Authentication, tasks, categories, tags, reminders, and AI functionality are isolated into their own modules.

### Extensibility

The architecture is intended to make it straightforward to introduce additional features without significantly modifying existing modules.

## Roadmap

Potential future improvements include:

* Frontend application
* More advanced AI task management
* AI-powered task prioritization
* Natural-language task creation
* Smart reminders
* Calendar integrations
* Email and notification integrations
* Real-time task synchronization
* Improved test coverage
* Docker-based development environment
* CI/CD pipeline
* Production deployment configuration
* Observability and application monitoring

## Contributing

Contributions are welcome.

1. Fork the repository.
2. Create a feature branch.

```bash
git checkout -b feature/your-feature
```

3. Make your changes.
4. Run the application and verify your changes.
5. Commit your changes.

```bash
git commit -m "Add your feature"
```

6. Push the branch.

```bash
git push origin feature/your-feature
```

7. Open a Pull Request.

## License

This project currently does not specify a license.

If you intend to distribute or accept external contributions, consider adding an appropriate open-source license.

## Author

**Amogh Shukla**

GitHub: [AmoghShukla](https://github.com/AmoghShukla)

