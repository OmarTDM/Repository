import io
import re
from email_validator import validate_email, EmailNotValidError
from PIL import Image
from pymongo import ReturnDocument

from app.db import db


def is_valid_email(email):
    try:
        # Validate the email address
        validate_email(email)
        return True
    except EmailNotValidError as e:
        # Email is not valid, return False
        return False


def convert_image_to_webp(image_stream):
    img = Image.open(image_stream)
    webp_io = io.BytesIO()
    img.save(webp_io, format="webp", quality=60)
    webp_io.seek(0)
    return webp_io.read()


def get_next_project_code():
    counter = db.counters.find_one_and_update(
        {"_id": "project_id"},
        {"$inc": {"sequence_value": 1}},
        upsert=True,
        return_document=ReturnDocument.AFTER,
    )
    return counter["sequence_value"]


def get_next_research_project_code():
    counter = db.counters.find_one_and_update(
        # Idealy, this should be "research_project_id", but it's a mistake in the database so we have to use "overproject_id" instead to avoid breaking the application
        {"_id": "overproject_id"}, 
        {"$inc": {"sequence_value": 1}},
        upsert=True,
        return_document=ReturnDocument.AFTER,
    )
    return counter["sequence_value"]


def format_studentproject_number(number):
    if not (0 <= number < 10000):
        raise ValueError("Number must be between 0 and 9999")
    formatted_number = f"S-{number:04d}"
    return formatted_number


def format_research_project_number(number):
    if not (0 <= number < 10000):
        raise ValueError("Number must be between 0 and 9999")
    formatted_number = f"R-{number:04d}"
    return formatted_number

def github_slugify(name: str) -> str:
    """
    Converts a repository name into a GitHub-compatible slug.
    
    Args:
        name (str): The repository name.
        
    Returns:
        str: The slugified string, conforming to GitHub's naming rules.
    """
    # Replace invalid characters with hyphens
    name = re.sub(r'[^a-z0-9._-]', '-', name)
    # Remove leading and trailing hyphens
    name = name.strip('-')
    # Collapse consecutive hyphens
    name = re.sub(r'-+', '-', name)
    return name
