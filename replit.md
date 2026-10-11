# Running the imported Django project

The original Django 6 application remains in `Project/`, with its existing
SQLite database and public CV styling retained.

## Start

Use the **Start application** workflow (or the Run button). Its command is:

```sh
cd Project && python manage.py runserver 0.0.0.0:5000
```

Python 3.12 and the dependencies declared in `Project/requirements.txt` are
installed through the root `pyproject.toml` and `uv.lock`.

The root URL displays the public CV. Visitors do not need to sign in. The CV is
managed at `/dashboard/`, which is limited to Django superusers; sign in at
`/dashboard/login/`. The older Home and Accueil pages and routes were removed.
Public navigation contains only CV and Contact: visitors do not have accounts
or a login link. The dashboard login accepts only active superusers. The legacy
`/about` URL redirects to the public CV rather than displaying another page.

The CV profile, sections, and entries are stored in the existing SQLite
database. The initial data migration carries the current CV content into these
tables. Changes made through the dashboard appear on the public CV immediately.

If you do not have access to the existing owner account, create another owner
from the Replit Shell:

```sh
cd Project && python manage.py createsuperuser
```

## Configuration

- `SESSION_SECRET` must be present in workspace Secrets. Django uses it as its
  secret key; do not put its value in code or documentation.
- Data remains in `Project/db.sqlite3`; do not replace or reset this database.
- Static assets are served by Django's development server from the existing
  `Project/Project/static/` directory.
- This is a development setup, not a production deployment: DEBUG is enabled
  and all hosts are allowed for the preview. Production publishing requires
  a separate security and hosting review.

## Checks

```sh
cd Project
python manage.py check
python manage.py showmigrations
python manage.py test
```

Apply future database migrations with `python manage.py migrate` after reviewing
them and backing up any important data.
