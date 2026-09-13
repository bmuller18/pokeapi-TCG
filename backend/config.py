import os

from dotenv import load_dotenv
from supabase import create_client, Client


load_dotenv()


SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

FLASK_SECRET_KEY = os.getenv(
    "FLASK_SECRET_KEY",
    "dev-secret-key-change-in-production"
)


def get_supabase_client() -> Client | None:
    """Create and return the Supabase client."""

    if not SUPABASE_URL or not SUPABASE_KEY:
        return None

    try:
        return create_client(
            SUPABASE_URL,
            SUPABASE_KEY
        )
    except Exception as e:
        print(f"Error creating Supabase client: {e}")
        return None