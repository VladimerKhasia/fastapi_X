import pytest
from app import schemas
from fastapi.encoders import jsonable_encoder

### ---------------------- post request tests

# @pytest.mark.parametrize("title, content, published", [
#     ("title_1", "content_1", True),
#     ("title_2", "content_2", False),
# ])
# def test_create_one_post(logged_client, test_user, title, content, published):
#     post_data = { "title": title, "content": content, "published": published}
#     re = logged_client.post("/posts/", json=post_data)
#     new_post = schemas.Post(**re.json())

#     assert re.status_code == 201
#     assert new_post.title == title
#     assert new_post.content == content
#     assert new_post.published == published
#     assert new_post.owner_id == test_user['id']

def test_unauthorized_create_post(client):
    post_data = { "title": "unauth_title", "content": "unauth_content", "published": True}
    re = client.post("/posts/", json=post_data)
    assert re.status_code == 401

### ---------------------- get request tests

def test_get_all_posts(logged_client, test_posts):
    re = logged_client.get("/posts/")
    # print(re.json()[0]["Post"])
    # print(f"\n\n------------------\n\n{jsonable_encoder(test_posts)[0]}")
    def response_validator(response_post):
        response_post = schemas.PostResponse(**response_post) 
        return response_post.Post.model_dump() 
    def test_post_validator(test_post):
        test_post = schemas.Post(**jsonable_encoder(test_post))
        return test_post.model_dump() 
    
    re_posts = list(map(response_validator, re.json())) 
    tst_posts = list(map(test_post_validator, test_posts))

    re_posts = sorted(re_posts, key=lambda x: sorted(x.items()))
    tst_posts = sorted(tst_posts, key=lambda x: sorted(x.items()))
    assert re.status_code == 200
    assert re_posts == tst_posts

def test_unauthorized_get_all_posts(client, test_posts):
    re = client.get("/posts/")
    assert re.status_code == 401

def test_get_one_post(logged_client, test_posts):
    re = logged_client.get(f"/posts/{test_posts[0].id}")
    one_post = schemas.PostResponse(**re.json())
    assert re.status_code == 200
    assert one_post.Post.id == test_posts[0].id
    assert one_post.Post.title == test_posts[0].title
    assert one_post.Post.content == test_posts[0].content

def test_unauthorized_get_one_post(client, test_posts):
    re = client.get(f"/posts/{test_posts[0].id}")
    assert re.status_code == 401

def test_get_one_post_absent(logged_client, test_posts):
    re = logged_client.get("/posts/777")
    assert re.status_code == 404

### ---------------------- put/patch request tests

def test_update_one_post(logged_client, test_posts):
    data = {"title": "title_update","content": "content_update","id": test_posts[0].id}
    re = logged_client.put(f"/posts/{test_posts[0].id}", json=data)
    updated_post = schemas.Post(**re.json())
    assert re.status_code == 200
    assert updated_post.id == test_posts[0].id
    assert updated_post.title == data["title"]
    assert updated_post.content == data["content"] 

def test_unauthorized_user_update_one_post(client, test_posts):
    data = {"title": "title_update","content": "content_update","id": test_posts[0].id}
    re = client.put(f"/posts/{test_posts[0].id}", json=data)
    assert re.status_code == 401

def test_update_one_post_absent(logged_client, test_posts):
    data = {"title": "title_update","content": "content_update","id": test_posts[0].id}
    re = logged_client.put("/posts/777", json=data)
    assert re.status_code == 404

def test_update_one_notown_post(logged_client, test_posts):
    data = {"title": "title_update","content": "content_update","id": test_posts[0].id}
    re = logged_client.put(f"/posts/{test_posts[1].id}", json=data)
    assert re.status_code == 403 

### ---------------------- delete request tests

def test_delete_one_post(logged_client, test_posts):
    re = logged_client.delete(f"/posts/{test_posts[0].id}")
    assert re.status_code == 204

def test_unauthorized_user_delete_one_post(client, test_posts):
    re = client.delete(f"/posts/{test_posts[0].id}")
    assert re.status_code == 401

def test_delete_one_post_absent(logged_client, test_posts):
    re = logged_client.delete("/posts/777")
    assert re.status_code == 404

def test_delete_one_notown_post(logged_client, test_posts):
    re = logged_client.delete(f"/posts/{test_posts[1].id}")
    assert re.status_code == 403    


