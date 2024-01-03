# templatetags/custom_filters.py
from django import template
from django.db.models.fields.files import FieldFile
import os
import time

register = template.Library()

@register.filter
def filename(value):
    if isinstance(value, FieldFile):
        return os.path.basename(value.name)
    return value

from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent


@register.simple_tag
def file_properties(file_path):
    if not os.path.exists(file_path):
        return f"The file  does not exist."

    file_size = os.path.getsize(file_path)

    # Convert bytes to a human-readable format (optional)
    size_suffixes = ['B', 'KB', 'MB', 'GB', 'TB']
    i = 0
    while file_size >= 1024 and i < len(size_suffixes)-1:
        file_size /= 1024.0
        i += 1

    return f"{file_size:.2f} {size_suffixes[i]}"