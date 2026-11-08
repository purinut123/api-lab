import pytest

STARS_ERROR = {"error": "number of stars must be between 1 and 5 (inclusive)"}


# Updating stars checks both sides of the valid 1-to-5 boundary.
@pytest.mark.parametrize(
    "stars, expected_status",
    [(0, 400), (1, 200), (5, 200), (6, 400)],
)
def test_update_rating_boundary(api, auth, rating, stars, expected_status):
    path = f"/api/ratings/{rating['id']}"
    res = api.put(path, json={"stars": stars}, headers=auth)
    assert res.status_code == expected_status

    if expected_status == 200:
        assert res.json()["stars"] == stars
        expected_saved_stars = stars
    else:
        assert res.json() == STARS_ERROR
        expected_saved_stars = rating["stars"]

    saved = api.get(path, headers=auth)
    assert saved.status_code == 200
    assert saved.json()["stars"] == expected_saved_stars
