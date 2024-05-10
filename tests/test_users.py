import pytest
from jose import jwt
from app import schemas
from app.config import settings 

    
def test_user_login(client, test_user):
    form_data = {"username": test_user["email"],"password": test_user["password"]}
    re = client.post("/login", data=form_data) 
    login_response = schemas.Token(**re.json())
    payload = jwt.decode(login_response.access_token, key=settings.SECRET_KEY, algorithms=[settings.ALGORITHM]) 
    assert re.status_code == 200
    assert login_response.token_type == "bearer"
    assert payload.get("id") == test_user["id"] 

@pytest.mark.parametrize("email, password, status_code", [
    ("user@example.com","something", 403),
    ("user@example.com","something", 500),
    ("user@example.com","wrongpassword", 200),
    ("wrongmail@example.com","something", 200),
    ("user@example.com","wrongpassword", 500),
    ("wrongmail@example.com","something", 500),   
    ("wrongmail@example.com","wrongpassword", 200),
    ("wrongmail@example.com","wrongpassword", 200),   
    ("wrongmail@example.com","wrongpassword", 500),
    ("wrongmail@example.com","wrongpassword", 500),       
])
def test_failed_login(client, test_user, email, password, status_code):
    form_data = {"username": email,"password": password}
    re = client.post("/login", data=form_data) 
    assert re.status_code != status_code
    #assert re.json().get("detail") == "Invalid credentials." 

def test_create_user(client):
    user_data = {"email": "user@example.com","password": "something"}
    re = client.post("/users/", json=user_data)
    user_response = schemas.UserResponse(**re.json())
    assert re.status_code == 201
    assert user_response.email == "user@example.com" 


def test_get_user(logged_client, test_user, test_users):
    def validate_single_user(single_user):
        re = logged_client.get(f"/users/{single_user['id']}")
        assert re.status_code == 200
        assert schemas.UserResponse(**re.json())
    assert list(map(validate_single_user, list([test_user, *test_users])))


def test_unauthorized_get_user(client, test_users):
    import random
    re = client.get(f"/users/{random.choice(test_users)['id']}")
    assert re.status_code == 401
    

# def test_root(client):
#     re = client.get("/")
#     assert re.status_code == 200
#     assert re.json() == {"Hello": "My World"}