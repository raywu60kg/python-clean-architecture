# Development Environment Setup
## Requirement
- poetry
- docker 
- make 

## 1. Install Dependencies by Poetry
```bash
poetry install 
```

## 2. Run the Postgresql Database
```bash
make postgresql-up
```

## 3. (Optional) Run Pytest
```bash
pytest
```

## 4. Apply alembic 
```bash
alembic upgrade head
```

## 5. Run local Server
```bash
make server-dev
```
Then check the `localhost:8000/docs` for swagger UI.