# python-clean-architecture

## Difference with buckpal 

### 1. test_account_persistence_adapter
In buckpal, its test case for persistence adapter directly call the sql database. But in python we rarely run the unit test with real database. So that I mock the repository function output.


## Reference
- https://github.com/thombergs/buckpal
- https://github.com/zhanymkanov/fastapi-best-practices
- https://python-dependency-injector.ets-labs.org/examples/fastapi-sqlalchemy.html#fastapi-sqlalchemy-example
- https://github.com/faraday-academy/fast-api-lms