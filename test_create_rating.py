import pytest

STARS_ERROR = "number of stars must be between 1 and 5 (inclusive)"
DECIMAL_ERROR = (
    "json: cannot unmarshal number 3.5 into Go struct field Rating.stars of type int"
)
TEXT_ERROR = "json: cannot unmarshal string into Go struct field Rating.stars of type int"
AUTH_ERROR = {"error": "authentication failed"}


# Base choice: 3 stars as a whole number, a real pizza, the user's token.
def test_base_choice_is_saved(api, auth, pizza_id):
    new = {"pizza_id": pizza_id, "stars": 3}
    res = api.post("/api/ratings", json=new, headers=auth)
    assert res.status_code == 201
    body = res.json()
    assert body["stars"] == 3
    assert body["pizza_id"] == pizza_id
    api.delete(f"/api/ratings/{body['id']}", headers=auth)


# C1: a number of stars below 1 or above 5 is refused with a message.
@pytest.mark.parametrize("stars", [0, 6])
def test_stars_out_of_range(api, auth, pizza_id, stars):
    new = {"pizza_id": pizza_id, "stars": stars}
    res = api.post("/api/ratings", json=new, headers=auth)
    assert res.status_code == 400
    assert res.json() == {"error": STARS_ERROR}


# C2: decimal stars are refused because stars must be a whole number.
def test_decimal_stars_is_refused(api, auth, pizza_id):
    new = {"pizza_id": pizza_id, "stars": 3.5}
    res = api.post("/api/ratings", json=new, headers=auth)
    assert res.status_code == 400
    assert res.json() == {"error": DECIMAL_ERROR}


# C2: text stars are refused because stars must be a number.
def test_text_stars_is_refused(api, auth, pizza_id):
    new = {"pizza_id": pizza_id, "stars": "3"}
    res = api.post("/api/ratings", json=new, headers=auth)
    assert res.status_code == 400
    assert res.json() == {"error": TEXT_ERROR}


# C2: omitting stars is refused as an out-of-range zero value.
def test_missing_stars_is_refused(api, auth, pizza_id):
    new = {"pizza_id": pizza_id}
    res = api.post("/api/ratings", json=new, headers=auth)
    assert res.status_code == 400
    assert res.json() == {"error": STARS_ERROR}


# C3: a rating for a pizza that does not exist is refused.
def test_unknown_pizza_is_refused(api, auth):
    new = {"pizza_id": 999999999, "stars": 3}
    res = api.post("/api/ratings", json=new, headers=auth)
    assert res.status_code == 400
    assert res.json() == {"error": "pizza ID 999999999 not found"}


# C4: a rating request without an Authorization header is refused.
def test_missing_token_is_refused(api, pizza_id):
    new = {"pizza_id": pizza_id, "stars": 3}
    res = api.post("/api/ratings", json=new)
    assert res.status_code == 401
    assert res.json() == AUTH_ERROR


# C4: a token with the wrong length is refused.
def test_wrong_length_token_is_refused(api, pizza_id):
    new = {"pizza_id": pizza_id, "stars": 3}
    wrong_auth = {"Authorization": "token short"}
    res = api.post("/api/ratings", json=new, headers=wrong_auth)
    assert res.status_code == 401
    assert res.json() == AUTH_ERROR
