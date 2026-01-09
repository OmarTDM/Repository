# GraphQL Demo (Flask)

This is a Flask app that reads data from MongoDB and exposes it through a small GraphQL API. The UI pages (especially `/stats`) use that GraphQL API to load fields and build charts.

## What you need

- Python installed.
- A MongoDB connection (local or remote from the dipper database).
- Install dependencies from `requirements.txt`.

## How to run

In PowerShell, from the project folder:

```powershell
pip install -r requirements.txt
python app.py
```

Then open:

- `http://127.0.0.1:5000/`

## Useful pages

- `/projects` shows projects from the database.
- `/stats` lets you build charts from any collection/field.
- `/graphql` is the GraphQL endpoint (POST).

## Notes

- If MongoDB is not reachable, pages that depend on it will be empty.
