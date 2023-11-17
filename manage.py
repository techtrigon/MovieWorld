#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import joblib


def main():
    # import recommender_logic
    # mymodel = joblib.load("./model")
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "movie_recommendation.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHON environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


# if __name__ == "__main__":
# PYTHON 3.11.6 IMPORTANT
# !!!!!!!!           BELOW LINES ARE IMPORTANT FOR JOBLIB TO WORK


# from recommender_logic import model, genre_counts, get_genre_movies
# import recommender_logic

main()
