import pytest


# The pizza never needs a tool that the customer excluded.
@pytest.mark.parametrize(
    "excluded",
    [[], ["Knife"], ["Scissors"], ["Knife", "Scissors"]],
)
def test_excluded_tool_is_not_used(api, auth, excluded):
    body = {"excludedTools": excluded}
    res = api.post("/api/pizza", json=body, headers=auth)
    assert res.status_code == 200
    assert res.json()["pizza"]["tool"] not in excluded


# Excluding every tool is a bad request and should return a useful JSON error.
@pytest.mark.xfail(
    reason="Defect 1: excluding all tools returns 500 with an empty body",
    strict=True,
)
def test_excluding_all_tools_returns_a_client_error(api, auth):
    body = {"excludedTools": ["Knife", "Pizza cutter", "Scissors"]}
    res = api.post("/api/pizza", json=body, headers=auth)
    assert res.status_code == 400
    assert res.headers["Content-Type"].startswith("application/json")
    assert res.json()["error"] != ""
