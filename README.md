# QuickPizza API testing lab

API integration-testing exercises for QuickPizza using Python, requests, and pytest.

## Install

```sh
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Step 0.5 verified the names, tools, and vegetarian-pizza requests with the
Python `requests` library before converting them into pytest tests.

## Input domain model for `POST /api/ratings`

| Characteristic | Blocks | Values |
| --- | --- | --- |
| C1 Value of stars | Below 1; 1–5 (base); above 5 | `0`, `3`, `6` |
| C2 Type of stars | Whole number (base); decimal; text; missing | `3`, `3.5`, `"3"`, no field |
| C3 Pizza | Exists (base); does not exist | New pizza, `999999999` |
| C4 Token | User's own (base); none; wrong length | Login token, no header, `token short` |
