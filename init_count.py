import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

url = os.getenv('SUPABASE_URL')
key = os.getenv('SUPABASE_KEY')
if not url or not key:
    print("Missing Supabase credentials in .env")
    exit(1)

supabase: Client = create_client(url, key)

try:
    # Get all rows where count is null or 0, or we don't know? Let's get all rows and update if count is less than 1.
    # We'll do: update pokemon set count = 1 where count is null or count < 1;
    # But note: we don't want to overwrite a count that is already >=1.

    # First, let's see how many rows we have.
    resp = supabase.table('pokemon').select('id, count').execute()
    rows = resp.data
    print(f"Found {len(rows)} rows in pokemon table.")

    updated = 0
    for row in rows:
        current_count = row.get('count')
        if current_count is None or current_count < 1:
            # Update this row to set count to 1
            supabase.table('pokemon').update({"count": 1}).eq('id', row['id']).execute()
            updated += 1

    print(f"Updated {updated} rows to set count to 1 (where count was null or less than 1).")

except Exception as e:
    print(f"Error: {e}")