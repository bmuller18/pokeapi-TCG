import os
from dotenv import load_dotenv
from supabase import create_client, Client

# Load environment variables
load_dotenv()

def init_supabase():
    """Initialize Supabase connection and setup database"""
    # Get Supabase credentials from environment
    supabase_url = os.getenv('SUPABASE_URL')
    supabase_key = os.getenv('SUPABASE_KEY')

    if not supabase_url or not supabase_key:
        print("Error: SUPABASE_URL and SUPABASE_KEY must be set in .env file")
        return False

    try:
        # Initialize Supabase client
        supabase: Client = create_client(supabase_url, supabase_key)
        print(f"Connected to Supabase at {supabase_url}")

        # Test connection by trying to fetch from a table (if it exists)
        # We'll try to create a table for pokemon data
        print("\nChecking database setup...")

        # Try to insert a test record to see if table exists and we have permissions
        # We'll use a dummy record that we'll delete afterwards
        test_data = {
            "id": 0,
            "name": "test",
            "image": "test",
            "created_at": "2026-09-12T00:00:00Z"
        }

        try:
            # Try to insert into a table called 'pokemon'
            result = supabase.table('pokemon').insert(test_data).execute()
            print("✓ Table 'pokemon' exists and we have insert permissions")

            # Clean up test record
            if result.data:
                test_id = result.data[0].get('id')
                supabase.table('pokemon').delete().eq('id', test_id).execute()
                print("✓ Cleaned up test record")

            return True

        except Exception as e:
            error_msg = str(e)
            print(f"✗ Error accessing 'pokemon' table: {error_msg}")

            # Check if it's a table not found error
            if 'could not find relation' in error_msg or 'does not exist' in error_msg:
                print("\nThe 'pokemon' table does not exist.")
                print("With the anon key provided, we cannot create tables directly.")
                print("You need to:")
                print("1. Go to your Supabase dashboard")
                print("2. Create a new table called 'pokemon'")
                print("3. Add these columns:")
                print("   - id (integer, primary key)")
                print("   - name (text)")
                print("   - image (text)")
                print("   - created_at (timestamp with timezone, default: now())")
                print("\nAlternatively, if you have the service_role key, you could add it to .env")
                print("and use it for table creation.")

                # Show what the table creation SQL would look like
                print("\nSample SQL for creating the table:")
                print("""
                CREATE TABLE public.pokemon (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    image TEXT NOT NULL,
                    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
                );

                -- Enable Row Level Security (optional)
                ALTER TABLE public.pokemon ENABLE ROW LEVEL SECURITY;

                -- Optional: create policies for public access
                -- CREATE POLICY "Allow public read access" ON public.pokemon
                --     FOR SELECT USING (true);

                -- CREATE POLICY "Allow public insert access" ON public.pokemon
                --     FOR INSERT WITH CHECK (true);
                """)

            elif 'permission denied' in error_msg or 'insufficient privilege' in error_msg:
                print("\nYou don't have sufficient privileges to create tables.")
                print("The anon key typically only allows SELECT, INSERT, UPDATE, DELETE")
                print("on existing tables with appropriate RLS policies.")
                print("You would need the service_role key for DDL operations (CREATE TABLE, etc.)")

            return False

    except Exception as e:
        print(f"Failed to connect to Supabase: {e}")
        return False

if __name__ == "__main__":
    init_supabase()