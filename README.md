Simplified backend for X

`fastapi` `pydantic` `sqlalchemy 2` `alembic` `postgresql` `pytest` `docker` `github actions` etc.

Quick overview of current version:
![Capture](https://github.com/VladimerKhasia/fastapi_X/assets/56228503/f9c0d160-f737-4d26-8185-6fd88737c43d)


You need to add .env file in root directory. Example .env file looks like this:
```
DB_USERNAME = postgres
DB_PASSWORD = your_password
DB_HOST = localhost     
DB_PORT = 5432
DB_NAME = postgres 
SECRET_KEY = "09d26myi889fmd0k49d8r0mm66b7a9563b93f7099f6njf78c9fmd88wnq88w9"  
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

#### f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
#### DB_NAME = #postgres #fastapi_X 
#### DB_HOST = #postgres #localhost #postgres instead of localhost - docker directly references to postgres
```
