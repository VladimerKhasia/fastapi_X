import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from app import models, database, oauth2
from app.config import settings
from app.main import app
from alembic import command


SQLALCHEMY_TEST_DATABASE_URL = f"postgresql://{settings.DB_USERNAME}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}_test"

test_engine = create_engine(SQLALCHEMY_TEST_DATABASE_URL)

TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

###------------------ for test database
@pytest.fixture
def session():
    # models.Base.metadata.drop_all(bind=test_engine)   # command.downgrade('base')
    # models.Base.metadata.create_all(bind=test_engine) # command.upgrade('head')
    command.downgrade('base')
    command.upgrade('head')
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()
    

@pytest.fixture
def client(session):
    def override_session_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[database.get_db] = override_session_db 
    yield TestClient(app) 

###------------------ for testing users
@pytest.fixture
def test_user(client):
    user_data = {"email": "user@example.com","password": "something"}
    re = client.post("/users/", json=user_data)
    made_user = re.json()
    made_user["password"] = "something"
    assert re.status_code == 201
    return made_user     

@pytest.fixture
def access_token_of_test_user(test_user):
    """Create access token of test_user""" 
    return oauth2.create_access_token(data={"id": test_user["id"]})

@pytest.fixture
def logged_client(client, access_token_of_test_user):
    """Turn the client into logged in client
       by equipping the client with test_user's access token"""
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {access_token_of_test_user}"
    }
    return client

@pytest.fixture
def test_users(client):
    """Creates additional fake users for testing."""
    users_data = [
        {"email": "user1@example.com","password": "1something"},
        {"email": "user2@example.com","password": "2something"},
        {"email": "user3@example.com","password": "3something"}
    ]
    def create_user(one_user_data):
        re = client.post("/users/", json=one_user_data)
        return re.json()
    return list(map(create_user, users_data))


###------------------ for testing posts
@pytest.fixture
def test_posts(test_user, test_users, session):
    """Creates fake posts for testing."""
    posts_data = [
        {
        "title": "one",
        "content": "stringone",
        "owner_id": test_user["id"]
        },
        {
        "title": "two",
        "content": "stringtwo",
        "owner_id": test_users[2]["id"]
        },
        {
        "title": "three",
        "content": "stringthree",
        "owner_id": test_users[2]["id"]
        },
        {
        "title": "three",
        "content": "stringthree",
        "owner_id": test_users[1]["id"]
        }
    ]
    def validate(individual_post):
        return models.Post(**individual_post)
    pre_posts = list(map(validate, posts_data))
    session.add_all(pre_posts)
    session.commit()
    posts = session.query(models.Post).all()
    return posts

###------------------ for testing votes
@pytest.fixture
def test_votes(test_posts, test_user, test_users, session):
    """Creates votes for testing"""
    votes_data = [
        {"user_id": test_user["id"], "post_id": test_posts[0].id},
        {"user_id": test_users[2]["id"], "post_id": test_posts[1].id}
    ]
    def validate(individual_vote):
        return models.Vote(**individual_vote)
    pre_votes = list(map(validate, votes_data))
    session.add_all(pre_votes)
    session.commit()
    votes = session.query(models.Vote).all()
    return votes    

