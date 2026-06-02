# Spec: Registration

## Overview
Implement the user registration flow so new visitors can create a Spendly account. The existing `GET /register` route already renders the form; this step wires up the `POST /register` handler to validate input, hash the password, insert the new user into the `users` table, and redirect to the login page on success. On error (duplicate email, blank fields, short password) the form re-renders with a descriptive inline message. Step 01 already delivered the schema and `get_db()` helper, so no schema changes are needed here.

## Depends on
- **Step 01 — Database Setup**: requires `users` table, `get_db()`, and `werkzeug` hashing to already be in place.

## Routes
- `POST /register` — accepts form fields `name`, `email`, `password`; creates a new user; redirects to `/login` on success — **public**

## Database changes
No database changes. The `users` table (id, name, email, password_hash, created_at) was created in Step 01.

## Templates
- **Modify:** `templates/register.html`
  - Keep the existing form layout unchanged
  - Ensure `action="{{ url_for('register') }}"` stays on the `<form>` tag (already present as `/register` — switch to `url_for`)
  - The `{% if error %}` block is already in place; no further changes needed

## Files to change
- `app.py` — convert the `register` route from `GET`-only to `GET, POST`; add POST logic inline
- `database/db.py` — add a `create_user(name, email, password_hash)` helper function

## Files to create
None.

## New dependencies
No new dependencies.

## Rules for implementation
- No SQLAlchemy or ORMs — use raw `sqlite3` via `get_db()`
- Parameterised queries only — never use f-strings or `%` formatting in SQL
- Passwords hashed with `werkzeug.security.generate_password_hash` before INSERT
- Use CSS variables — never hardcode hex values (template already follows this)
- All templates extend `base.html`
- The route must handle duplicate email via `sqlite3.IntegrityError` and re-render the form with `error="An account with that email already exists."`
- Validate server-side: name not blank, email not blank, password ≥ 8 characters — re-render form with a clear `error` message on failure
- On success redirect to `url_for('login')` using `redirect()`; do **not** auto-login (session management is Step 3)
- `create_user()` in `db.py` must return the new user's `id`
- Do not touch stub routes or any other feature

## Definition of done
- [ ] Submitting the registration form with valid data creates a new row in `users` with a hashed password and redirects to `/login`
- [ ] Re-submitting with the same email shows the form again with the error "An account with that email already exists."
- [ ] Submitting with an empty name, empty email, or password shorter than 8 characters shows the form again with a descriptive error message
- [ ] The password stored in the database is never plaintext — `check_password_hash` can verify it
- [ ] `GET /register` still renders the blank form without errors
- [ ] No new routes are broken; all existing stub routes still return their placeholder strings
- [ ] `pytest` passes (existing tests continue to pass)
