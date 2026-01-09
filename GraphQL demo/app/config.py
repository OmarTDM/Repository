import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, "../.env"))

BASEDIR = basedir

DB_HOST = os.environ.get("DB_HOST") or "localhost"
DB_PORT = os.environ.get("DB_PORT") or 27017
DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
SEEDLIST_CONNECTION_FORMAT = os.environ.get("USE_SEEDLIST_CONNECTION_FORMAT") or False

if SEEDLIST_CONNECTION_FORMAT and SEEDLIST_CONNECTION_FORMAT.lower() != "false":
    MONGODB_URI = f"mongodb+srv://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/"
else:
    MONGODB_URI = f"mongodb://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/"

GITHUB_ORG = os.environ.get("GH_ORG")
GITHUB_TOKEN = os.environ.get("GH_TOKEN2")
SECRET_KEY = os.environ.get("SECRET_KEY") or "changeme-p85JuZYpkYbgET8i"

if not GITHUB_TOKEN or not GITHUB_ORG:
    raise RuntimeError("GITHUB_ORG and GITHUB_TOKEN must be configured")
