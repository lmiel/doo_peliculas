#!/usr/bin/env python
import os
import sys

TMDB_API_KEY= 'c2dc323ab66e5495c27791ea6469e55e'


if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "netflixuax.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and available on your PYTHONPATH environment variable?"
        ) from exc
    execute_from_command_line(sys.argv)

