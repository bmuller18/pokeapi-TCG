import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()
url = os.getenv('SUPABASE_URL')
key = os.getenv('SUPABASE_KEY')
if not url or not key:
    print("Missing credentials")
    exit(1)
supabase: Client = create_client(url, key)

# Get a few rows with all columns
resp = supabase.table('pokemon').select('id, name, image, api_response, count, created_at').limit(5).execute()
print(f"Fetched {len(resp.data)} rows")
for i, row in enumerate(resp.data):
    print(f"\nRow {i}:")
    print(f"  id: {row['id']}")
    print(f"  name: {row['name']}")
    print(f"  image: {row['image'][:50]}..." if row['image'] else "  image: None")
    print(f"  count: {row['count']}")
    print(f"  created_at: {row['created_at']}")
    api = row['api_response']
    if api is None:
        print(f"  api_response: None")
    else:
        if isinstance(api, dict):
            print(f"  api_response: dict with keys {list(api.keys())[:5]}...")
            # Show a few sample keys
            for k in ['height', 'weight', 'name', 'id']:
                if k in api:
                    print(f"    {k}: {api[k]}")
        else:
            print(f"  api_response: {type(api)} - {str(api)[:100]}...")