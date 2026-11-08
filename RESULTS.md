# API lab results

Tests were run against `https://quickpizza.grafana.com` on 8 November 2026 with Python 3.12.14, pytest 9.2.0, requests 2.34.2, and pytest-html 4.2.0. Results from this shared public service can change between runs.

## Part 0

- **Step 0.1, number of pizza names:** 18.
- **Step 0.3, request without a token:** 401 Unauthorized with `{"error": "authentication failed"}`.
- **Step 0.4, vegetarian pizza name:** `A Narrow Pugliese`.
- **Step 0.12, three runs without a session:** pass, pass, fail. The third run created the user with status 201 but login reached a different server and returned 401.
- **Step 0.16, blocks of “how many of the three tools are excluded”:** 0 excluded (`[]`), 1 excluded (`["Knife"]` and `["Scissors"]`), 2 excluded (`["Knife", "Scissors"]`), and all 3 excluded (`["Knife", "Pizza cutter", "Scissors"]`). The final block reveals the defect.

## Defect report

- **Title:** Excluding all available tools returns 500 with an empty response.
- **Request:** `POST /api/pizza` with a logged-in user's Authorization header and body `{"excludedTools": ["Knife", "Pizza cutter", "Scissors"]}`.
- **Expected result:** Status 400 Bad Request and a JSON body whose `error` field explains that no pizza can satisfy the request.
- **Actual result:** Status 500 Internal Server Error with an empty body.
- **Severity:** Medium. The defect does not lose data or bypass authorization, but a validly formed unsatisfiable request triggers a server failure and gives the client no message it can display or handle usefully.

## Part A

- **Step A4, another user's access:** read returned 404, update returned 400, and delete returned 400. All three attempts were refused and the owner's rating remained unchanged.

## Part B

1. These integration tests can find deployment or routing problems such as the load balancer sending related requests to different servers, and integration problems among authentication, the API code, and stored database records. Unit tests with stubs cannot exercise those real connections. Unit tests are still useful because they are fast, deterministic, and can isolate many edge cases without depending on a remote service.

2. Every test creates a unique user so its ratings belong to that test and cannot collide with or modify another student's data. The public token represents shared data and is unsuitable for mutations. In Project 2, each test should create uniquely named records for the group's own account, operate only on those records, and clean them up where the API allows it.

3. One session preserves the `AWSALB`/`AWSALBCORS` load-balancer cookies, so user creation, login, and later requests keep reaching the server that knows that user. Without a session, two of the three optional runs passed, while one failed at login with 401 after user creation had returned 201. That changing result with unchanged code is a flaky test.

4. The block that excludes all three available tools revealed the defect. A 500 with an empty body looks like an unexpected server failure and gives an app no structured explanation to show the user; a 400 with a JSON message clearly says the input cannot be satisfied. The test remains as a strict xfail so the defect stays documented and automatically becomes an unexpected pass when the API is fixed, prompting removal of the marker.

5. Base choice needs `1 + (3−1) + (4−1) + (2−1) + (3−1) = 9` tests: one base test and one for each non-base block. All combinations needs `3 × 4 × 2 × 3 = 72` tests.

6. The other user received 404 for read, 400 for update, and 400 for delete. I would expect 404 for all three because a rating owned by another user should appear not to exist, which also avoids revealing it. The security requirement itself passes because every operation is refused and the rating is unchanged. The different codes are an API consistency issue, and become a contract defect if the specified response for an inaccessible rating is uniformly 404.

7. The made-up 16-character token returned status 200 and a JSON list of ratings. This is an authorization defect because the server appears to accept token shape without proving that the token was issued by login. On a real system, a stranger could read or enumerate another user's data; if mutation endpoints made the same mistake, the stranger might also alter or delete it. This lab used the token only for the required read.

8. An API test checks protocol details such as exact status codes, headers, error schemas, and fields more directly and precisely than a web-page test. A web-page test is needed to check what users actually see and can interact with, including layout, rendering, accessibility, and browser behaviour.
