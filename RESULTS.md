# API lab results

## Part 0

- **Step 0.1:** The `/api/names` response contained 18 pizza names.
- **Step 0.2:** The response used status 200 and content type `application/json`.
- **Step 0.3:** The tools request without a token returned 401 Unauthorized.
- **Step 0.4:** The vegetarian request returned `A Narrow Pugliese`.
- **Step 0.9:** A unique made-up user logged in and started with no ratings.
- **Step 0.12:** Three runs without a session produced pass, pass, and fail (401), confirming the test is flaky without the load-balancer cookie.
- **Step 0.16:** The excluded-tool count blocks are 0, 1, 2, and 3 of the three available tools.

## Defect report

- **Title:** Excluding all available tools returns 500 with an empty response.
- **Request:** `POST /api/pizza` with all three tools in `excludedTools`.
- **Expected result:** Status 400 with a useful JSON error message.
- **Actual result:** Status 500 with an empty body.
- **Severity:** Medium.
