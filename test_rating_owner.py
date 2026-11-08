# A second user cannot read another user's rating.
def test_other_user_cannot_read_rating(api, auth, other_auth, rating):
    path = f"/api/ratings/{rating['id']}"
    res = api.get(path, headers=other_auth)
    assert 400 <= res.status_code <= 499

    saved = api.get(path, headers=auth)
    assert saved.status_code == 200
    assert saved.json() == rating


# A second user cannot change another user's rating.
def test_other_user_cannot_update_rating(api, auth, other_auth, rating):
    path = f"/api/ratings/{rating['id']}"
    res = api.put(path, json={"stars": 5}, headers=other_auth)
    assert 400 <= res.status_code <= 499

    saved = api.get(path, headers=auth)
    assert saved.status_code == 200
    assert saved.json()["stars"] == rating["stars"]


# A second user cannot delete another user's rating.
def test_other_user_cannot_delete_rating(api, auth, other_auth, rating):
    path = f"/api/ratings/{rating['id']}"
    res = api.delete(path, headers=other_auth)
    assert 400 <= res.status_code <= 499

    saved = api.get(path, headers=auth)
    assert saved.status_code == 200
    assert saved.json() == rating
