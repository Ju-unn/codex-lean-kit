# Security checklist (web app: HTTP API + DB + browser UI)

## Finding rule
For every candidate finding, name:
- the lower-trust principal
- the accepted input or action
- the intended control
- the crossed boundary
- the affected principal or resource
- the concrete result

A missing best practice, a guessed deployment behaviour, or a self-impact is not a security finding.

Severity anchors:
- **critical**: an unauthenticated actor gains code execution, full data access, or takeover of other accounts.
- **high**: an explicit control is fully defeated with real consequences. Examples: auth bypass, reading or writing another user's or store's data, stored script execution affecting other users.
- **medium**: a real boundary violation with a limited blast radius or uncommon preconditions.
- **low**: disclosure of non-secret internals, or an effect that needs sustained effort for minimal gain.

Does the result fully defeat an explicit control, or only weaken it? If you cannot state the concrete damage, the severity is lower than it feels.

## Injection
Trace untrusted input from its entry point to a dangerous sink: SQL queries, HTML output, shell commands, file paths, HTTP redirects.
- Look for indirect injection too: data stored safely, then used in a dangerous context by different code.
- Look for injection through field names, keys, and headers, not just values.
- SQL: parameterized statements only, including ORDER BY and LIMIT values and dynamic column names (allow-list them).
- HTML: user text rendered with textContent or React escaping. Never innerHTML or dangerouslySetInnerHTML with user data.

## Access control
Verify that a caller cannot act outside its authority, and that the check is the right permission for the right resource through the right mechanism.
- Is there another path to the same state change that checks a weaker permission?
- Can a field in the request body override what the permission system restricts, such as userId, role, storeId, or status?
- Are there endpoints that check authentication but forget authorization (IDOR: /items/:id of another user)?
- Does the same resource have several access paths with inconsistent checks (list vs detail vs update)?
- Do bulk, export, and import operations enforce per-item permissions?

## Business logic
- State machine violations:
  - Can a step be skipped, gone back to, or replayed after completion?
  - Can the flow reach an invalid state?
- Races with business impact: concurrent requests that double-approve, double-book, or lose updates. Enforce these in SQL with UNIQUE, CHECK, or a conditional UPDATE whose changed-row count is checked.
- Numbers: negative, zero, huge, non-integer, string-number coercion.
- Implicit trust: data from the DB or another component assumed safe because "we validated it on the way in".
- Time: expiry checks at the exact boundary moment, time zones, clock source.
- Defaults: what an empty or missing field or config turns into. Fail closed.

## Data leakage
- Do error messages or status codes differ between "does not exist" and "no access" (enumeration)?
- Can search, filter, or sort parameters reveal records the user cannot open?
- Do responses include fields the UI does not need, such as password hashes, other users' data, or internal IDs?

## Secrets and crypto
- No hardcoded passwords, keys, or tokens in source, logs, error messages, URLs, or responses. Config comes from env, and .env is git-ignored.
- Security-critical random values come from node:crypto, never Math.random.
- Passwords are hashed with scrypt or bcrypt and never logged. Secrets are compared in constant time (crypto.timingSafeEqual).
- If a crypto operation fails, the error path must not fall back to no-crypto.

## Obvious things (check every item literally)
- grep for password, secret, apikey, token, Bearer, -----BEGIN
- TODO, FIXME, or HACK comments about auth or validation
- unprotected /debug, /admin, /test, /env, /config routes; test or seed credentials that work outside tests
- eval, Function, child_process, or vm with dynamic input
- CORS set to `*` together with credentials
- cookies without HttpOnly or SameSite when they carry a session
- open redirects (redirect, next, url, return parameters)
- stack traces, internal paths, or SQL errors in responses

## Not findings
- Defence-in-depth advice with no reachable boundary violation.
- A checklist deviation presented as a vulnerability.
- .env.example values, obviously fake test credentials, checksums.
- Hardening the requirements do not ask for, such as rate limiting, RBAC, or CSRF on a cookie-less API.

Sources: cloudflare/security-audit-skill (finding rule, severity anchors, attack classes: injection, access control, business logic, feature abuse, obvious things); affaan-m/ECC security-reviewer.
