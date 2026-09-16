import os
import dj_database_url
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Determine environment (default to 'development')
ENVIRONMENT = os.getenv('ENVIRONMENT', 'development').lower()

def get_database_config():
    """
    Returns the appropriate database configuration based on the environment.
    Just like in FastAPI, this keeps database connection logic modular.
    """
    if ENVIRONMENT == 'production':
        # In production, we use PostgreSQL.
        # Option 1 (preferred): provide a full connection string in DATABASE_URL.
        #   e.g. postgres://user:pass@host:5432/dbname
        # Option 2: provide individual credentials via DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT.
        # DATABASE_URL takes priority if both are present.
        db_url = os.getenv('DATABASE_URL')
        if db_url:
            return {
                'default': dj_database_url.parse(db_url, conn_max_age=600)
            }

        # Fall back to explicit individual credentials
        db_name = os.getenv('DB_NAME')
        db_user = os.getenv('DB_USER')
        db_password = os.getenv('DB_PASSWORD')
        db_host = os.getenv('DB_HOST', 'localhost')
        db_port = os.getenv('DB_PORT', '5432')

        if not all([db_name, db_user, db_password]):
            raise ValueError(
                "Production database is not configured. "
                "Set either DATABASE_URL or all of DB_NAME, DB_USER, DB_PASSWORD (and optionally DB_HOST, DB_PORT) in .env."
            )

        return {
            'default': {
                'ENGINE': 'django.db.backends.postgresql',
                'NAME': db_name,
                'USER': db_user,
                'PASSWORD': db_password,
                'HOST': db_host,
                'PORT': db_port,
                'CONN_MAX_AGE': 600,
            }
        }
    else:
        # In local/development, fallback to SQLite
        return {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': BASE_DIR / 'db.sqlite3',
            }
        }

DATABASES = get_database_config()
