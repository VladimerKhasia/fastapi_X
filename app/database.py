from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .config import settings

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.DB_USERNAME}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# import psycopg2.extras
# import psycopg2

# while True:
#     try:
#         conn = psycopg2.connect(host='localhost', database='fastapi', 
#                                 user='postgres', password='something',
#                                 cursor_factory=psycopg2.extras.RealDictCursor)
#         cursor = conn.cursor()
#         print('we connected to database')
#         break
#         # conn.commit()
#         # cursor.close()
#         # conn.close()
#     except Exception as error:
#         print(f'error was {error}')        