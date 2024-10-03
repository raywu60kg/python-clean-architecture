# Python Clean Architecture
![image](static/hexagonal_architecture.png)
This repository is a Python implementation of the [buckpal](https://github.com/thombergs/buckpal) project, which was originally written in Java. The goal is to demonstrate how to achieve Hexagonal Architecture using modern Python packages and practices.

## About Buckpal
Buckpal is a simple web application that adheres to the principles of Hexagonal Architecture, as outlined in the book "Get Your Hands Dirty on Clean Architecture" by Tom Hombergs. This architecture is an elegant and efficient solution for building complex applications with maintainability, testability, and flexibility.

For a deep dive into Hexagonal Architecture, refer to ["Get Your Hands Dirty on Clean Architecture"](https://thombergs.gumroad.com/l/gyhdoca). The book provides invaluable insights and has greatly inspired me.

## Technical Stack
- API Server: FastAPI (with async/await)
- Containerization: Docker / Docker Compose
- Testing Framework: Pytest
- Database: PostgreSQL (with asyncpg)
- Database Migrations: Alembic
- Dependency Injection: python-dependency-injector
- Static Analysis and Linting: Mypy / Ruff

## Run Server
Run 
```bash
docker compose up 
```
Then the server will be running at `localhost:80`. Check the swagger document at `localhost:80/docs`

## Tricky thing for Hexagonal Architecture in python
### 1. Async Function Annotation
In Hexagonal Architecture, each layer should be decoupled and unaware of the details from other layers. However, the `async` function annotation can break this principle. When you are forced to mark a function as `async` because it calls another asynchronous function, it inadvertently leaks information about implementation details across layers, compromising the desired separation of concerns.

### 2. Typing 
When working with object-oriented programming and multilevel inheritance in Python, it's important to use type annotations for function/class inputs and outputs, along with Mypy for static analysis. However, I believe the Python typing ecosystem is still evolving, and you may encounter various unexpected challenges when using type hints.


### 3. Dependency Injector
In multilevel inheritance, avoiding dependency injection tools can make development quite challenging. In Python, however, we don't have many options aside from `python-dependency-injector`. While it's a powerful tool with excellent documentation, it hasn't gained widespread discussion or adoption in the community, at least from my perspective.

## Difference with buckpal 
### 1. Test Account persistence adapter
In buckpal, test case for persistence adapter directly call the sql database. But in python we rarely run the unit test with real database. So that I mock the repository function output.

### 2. Dependency Rule Tests
I do not think there is a way for testing dependency rule in python so I did not implement the dependency rule tests. If you know how to do it, please let me know. 

## Development Environment Setup
Please see [here](https://github.com/raywu60kg/python-clean-architecture//blob/main/docs/dev_env_setup.md).

## Reference
- https://github.com/thombergs/buckpal
- https://github.com/zhanymkanov/fastapi-best-practices
- https://python-dependency-injector.ets-labs.org/examples/fastapi-sqlalchemy.html#fastapi-sqlalchemy-example
- https://github.com/faraday-academy/fast-api-lms
