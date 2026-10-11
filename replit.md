# Running the imported Django project

The original Django 6 application remains in `Project/`, with its templates,
static assets, and existing SQLite database unchanged.

## Start

Use the **Start application** workflow (or the Run button). Its command is:

```sh
cd Project && python manage.py runserver 0.0.0.0:5000
```

Python 3.12 and the dependencies declared in `Project/requirements.txt` are
installed through the root `pyproject.toml` and `uv.lock`.

The root URL displays the CV page. Routes include `/cv`, `/contact`, `/about`,
and `/admin/`. The unused Home and Accueil pages and their routes have been
removed.

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
