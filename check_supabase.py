import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()
supabase_url = os.getenv('SUPABASE_URL')
supabase_key = os.getenv('SUPABASE_KEY')
if not supabase_url or not supabase_key:
    print("Missing Supabase credentials in .env")
    exit(1)

supabase: Client = create_client(supabase_url, supabase_key)

# Try to get one row from pokemon table to see columns
try:
    resp = supabase.table('pokemon').select('*').limit(1).execute()
    if resp.data:
        print("Columns in the row:", list(resp.data[0].keys()))
        print("First row:")
        for k, v in resp.data[0].items():
            if k == 'api_response':
                print(f"  {k}: <JSONB, length {len(str(v))} chars>")
            else:
                print(f"  {k}: {v}")
    else:
        print("No rows found in table 'pokemon'.")
except Exception as e:
    print(f"Error selecting from pokemon: {e}")

# Also try to get count
try:
    resp = supabase.table('pokemon').select('id', count='exact').execute()
    print(f"Total rows in pokemon: {resp.count}")
except Exception as e:
    print(f"Error counting rows: {e}")