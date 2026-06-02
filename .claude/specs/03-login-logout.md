# Spec: Login and Logout

## Overview
Implement the login and logout flows so registered users can authenticate and end their session. The existing `GET /login` route renders the form stub; this step wires up `POST /login` to verify credentials against the database, create a Flask session on success, and redirect to a dashboard placeholder. `GET /logout` clears the session and redirects to the landing page. Together these two routes complete the auth loop started in Step 02 (registration), making session state available to all future protected routes.

## Depends on
- **Step 01 — Database Setup**: requires `users` table, `get_db()`, and `werkzeug` hashing to be in place.
- **Step 02 — Registration**: requires `create_user()` and a working user record to log in against.

## Routes
- `POST /login` — accepts form fields `email` and `password`; verifies credentials; sets session on success; redirects to `/dashboard` placeholder on success — **public**
- `GET /logout` — clears the Flask session; redirects to `/` — **logged-in** (but safe to call when already logged out)

## Database changes
No database changes. The `users` table from Step 01 already stores `email` and `password_hash`.

A new helper `get_user_by_email(email)` must be added to `database/db.py` to look up a user by email. No schema changes are required.

## Templates
- **Modify:** `templates/login.html`
  - Ensure `<form>` uses `method="POST"` and `action="{{ url_for('login') }}"`
  - Add `{% if error %}<p class="error">{{ error }}</p>{% endif %}` block if not already present
  - Keep existing layout and styles unchanged
- **Modify:** `templates/base.html`
  - Add a logout link (e.g. in the nav) that is only visible when the user is logged in: `{% if session.user_id %}`

## Files to change
- `app.py` — convert `login` from GET-only to `GET, POST`; add POST logic; implement `logout`; add `secret_key` to app config; import `session`, `check_password_hash`
- `database/db.py` — add `get_user_by_email(email)` helper that returns a `sqlite3.Row` or `None`
- `templates/login.html` — wire up the form as described above
- `templates/base.html` — add conditional logout nav link

## Files to create
None.

## New dependencies
No new dependencies. `flask.session` and `werkzeug.security.check_password_hash` are already available.

## Rules for implementation
- No SQLAlchemy or ORMs — use raw `sqlite3` via `get_db()`
- Parameterised queries only — never use f-strings or `%` formatting in SQL
- Passwords verified with `werkzeug.security.check_password_hash` — never compare plaintext
- `app.secret_key` must be set before any session usage; use a hard-coded dev string (`"spendly-dev-secret"`) — do not read from env (no `.env` support yet)
- Store only `session["user_id"]` and `session["user_name"]` — nothing else
- Use CSS variables — never hardcode hex values
- All templates extend `base.html`
- On bad credentials re-render `login.html` with `error="Invalid email or password."` — do not reveal which field was wrong
- On successful login redirect to `url_for('dashboard')` — add a minimal stub route `GET /dashboard` that returns `"Dashboard — coming soon"` if it does not already exist
- `logout` must call `session.clear()` then `redirect(url_for('landing'))`
- Do not touch any other stub routes

## Definition of done
- [ ] Submitting the login form with the demo user credentials (`demo@spendly.com` / `demo123`) sets `session["user_id"]` and redirects to `/dashboard`
- [ ] Submitting with a wrong password re-renders the login form with `"Invalid email or password."`
- [ ] Submitting with an email that does not exist re-renders the login form with `"Invalid email or password."`
- [ ] Visiting `/logout` clears the session and redirects to `/`
- [ ] After logout, visiting `/logout` again redirects to `/` without error
- [ ] The logout nav link is visible in `base.html` only when `session.user_id` is set
- [ ] `GET /login` still renders the blank form without errors
- [ ] No existing routes are broken; all other stub routes still return their placeholder strings
- [ ] `pytest` passes (existing tests continue to pass)
