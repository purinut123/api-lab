import uuid

PASSWORD = "Pizza-2026"


def new_user():
    return {"username": "lab-" + uuid.uuid4().hex[:12], "password": PASSWORD}


# Creating a second user with an existing username is refused.
def test_duplicate_username_is_refused(api):
    user = new_user()
    first = api.post("/api/users", json=user)
    assert first.status_code == 201
    res = api.post("/api/users", json=user)
    assert res.status_code == 400
    assert res.json() == {"error": "username already taken"}


# Logging in with a wrong password is refused.
def test_wrong_password_is_refused(api):
    user = new_user()
    made = api.post("/api/users", json=user)
    assert made.status_code == 201
    wrong = {"username": user["username"], "password": "Wrong-Pizza-2026"}
    res = api.post("/api/users/token/login", json=wrong)
    assert res.status_code == 401
    assert res.json() == {"error": "authentication failed"}


# Creating a user with an empty username is refused.
def test_empty_username_is_refused(api):
    user = {"username": "", "password": PASSWORD}
    res = api.post("/api/users", json=user)
    assert res.status_code == 400
    assert res.json() == {"error": "username field is empty"}
