
def test_unauthorized_voting(client, test_votes):
    data = { "post_id": test_votes[1].post_id, "direction": 1}
    re = client.post("/votes/", json=data)
    assert re.status_code == 401

def test_up_vote(logged_client, test_votes):
    data = { "post_id": test_votes[1].post_id, "direction": 1}
    re = logged_client.post("/votes/", json=data)
    assert re.status_code == 201

def test_up_vote_twice(logged_client, test_votes):
    data = { "post_id": test_votes[0].post_id, "direction": 1}
    re = logged_client.post("/votes/", json=data)
    assert re.status_code == 403 

def test_upvote_absent_post(logged_client, test_votes):
    data = { "post_id": 777, "direction": 1}
    re = logged_client.post("/votes/", json=data)
    assert re.status_code == 404

def test_down_vote(logged_client, test_votes):
    data = { "post_id": test_votes[0].post_id, "direction": 0}
    re = logged_client.post("/votes/", json=data)
    assert re.status_code == 201