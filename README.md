# QuickPizza API testing lab

This repository contains API integration tests for the QuickPizza demo service. The suite uses Python, `requests`, and pytest to test successful and refused requests, CRUD operations, input partitions, boundary values, ownership, and one known API defect.

## Install

Python 3.10 or newer is required. From the repository root, create a virtual environment and install the dependencies:

```sh
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

On Windows PowerShell, activate the environment with `.venv\Scripts\activate` instead.

## Run

Run the full suite with:

```sh
pytest -v
```

Create the self-contained HTML report with:

```sh
pytest -v --html=report.html --self-contained-html
```

The expected result at the time of this lab is `32 passed, 1 xfailed`. The expected failure keeps the known all-tools-excluded defect visible without making the rest of the suite red.

## Input domain model for `POST /api/ratings`

Base choice uses 3 stars as a whole number, an existing pizza, and the logged-in user's own token. Every other test changes one block while keeping the remaining characteristics at their base blocks.

| Characteristic | Block | Test value | Covering test |
| --- | --- | --- | --- |
| C1 Value of stars | Below 1 | `0` | `test_stars_out_of_range[0]` |
| C1 Value of stars | 1 to 5 (base) | `3` | `test_base_choice_is_saved` |
| C1 Value of stars | Above 5 | `6` | `test_stars_out_of_range[6]` |
| C2 Type of stars | Whole number (base) | `3` | `test_base_choice_is_saved` |
| C2 Type of stars | Decimal | `3.5` | `test_decimal_stars_is_refused` |
| C2 Type of stars | Text | `"3"` | `test_text_stars_is_refused` |
| C2 Type of stars | Missing | No `stars` field | `test_missing_stars_is_refused` |
| C3 Pizza | Exists (base) | A newly recommended pizza | `test_base_choice_is_saved` |
| C3 Pizza | Does not exist | `999999999` | `test_unknown_pizza_is_refused` |
| C4 Token | User's own (base) | Token from the login fixture | `test_base_choice_is_saved` |
| C4 Token | None | No Authorization header | `test_missing_token_is_refused` |
| C4 Token | Wrong length | `token short` | `test_wrong_length_token_is_refused` |

Base choice coverage needs one base test plus one test for every non-base block: `1 + 2 + 3 + 1 + 2 = 9` tests. All-combinations coverage would need `3 × 4 × 2 × 3 = 72` tests.

## Test-data safety

Tests that create or change ratings first create a unique made-up user and operate only on that user's data. The shared `requests.Session` retains the load balancer cookie so creation and login reach the same QuickPizza server. The public and made-up tokens are used only for the read-only or recommendation requests required by the exercise.
