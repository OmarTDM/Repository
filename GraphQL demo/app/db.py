"""Bridge module so `app` package can import the top-level `db` module.
This makes `from app.db import db, client` available while keeping the single
source of truth in the project root `db.py` file.
"""
import importlib

_root_db = importlib.import_module("db")

# expose the same names expected by the app
client = getattr(_root_db, "client", None)
db = getattr(_root_db, "db", None)

# Types used by the configuration UI
bson_types = [
	"String",
	"Integer",
	"Double",
	"Boolean",
	"Date",
	"ObjectId",
	"Array",
	"Checkboxes",
	"Binary Data",
	"Undefined",
	"Null",
]

__all__ = ["client", "db", "bson_types"]
