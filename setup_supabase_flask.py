import os
from flask import Flask
from dotenv import load_dotenv
from supabase import create_client, Client

# Load environment variables
load_dotenv()

def create_app():
    """Create and configure a minimal Flask app for Supabase setup"""
    app = Flask(__name__)

    # Configure Supabase
    supabase_url = os.getenv('SUPABASE_URL')
    supabase_key = os.getenv('SUPABASE_KEY')

    if not supabase_url or not supabase_key:
        raise ValueError("SUPABASE_URL and SUPABASE_KEY must be set in .env file")

    # Initialize Supabase client
    supabase: Client = create_client(supabase_url, supabase_key)
    app.supabase = supabase

    return app

def setup_database():
    """Setup the Supabase database for Pokemon data"""
    app = create_app()
    supabase = app.supabase

    print(f"Connected to Supabase at {os.getenv('SUPABASE_URL')}")

    # Try to test the connection and setup table
    try:
        # Test connection by attempting to query (will fail if table doesn't exist, but that's ok)
        # We use limit=0 to just test connectivity without fetching data
        result = supabase.table('pokemon').select('id').limit(0).execute()
        print("✓ Successfully connected to 'pokemon' table")

        # Check if count column exists by trying to select it
        try:
            supabase.table('pokemon').select('count').limit(0).execute()
            print("✓ 'count' column exists")
        except Exception as e:
            if 'could not find column' in str(e) or 'does not exist' in str(e):
                print("⚠ 'count' column does not exist - needed for duplicate counting")
                print("  Please add it manually:")
                print("  ALTER TABLE public.pokemon ADD COLUMN count INTEGER DEFAULT 1;")
                print("  OR recreate the table with the count column:")
            else:
                print(f"? Unexpected error checking count column: {e}")

    except Exception as e:
        error_msg = str(e).lower()
        print(f"Connection test failed: {e}")

        # Check if it's a table not found error
        if 'could not find relation' in error_msg or 'does not exist' in error_msg or 'not found' in error_msg:
            print("\nThe 'pokemon' table does not exist in your Supabase database.")
            print("Please create it manually using the Supabase dashboard or SQL editor.")
            print("\nRequired table structure (with count column for tracking duplicates):")
            print("Table name: pokemon")
            print("Columns:")
            print("  - id (integer, primary key)")
            print("  - name (text)")
            print("  - image (text)")
            print("  - count (integer, default: 1)  <-- Tracks how many times each pokemon appeared")
            print("  - created_at (timestamp with timezone, default: now())")
            print("\nYou can run this SQL in the Supabase SQL editor:")
            print("""
            CREATE TABLE IF NOT EXISTS public.pokemon (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                image TEXT NOT NULL,
                count INTEGER DEFAULT 1,
                created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
            );

            -- Optional: Enable RLS if needed
            -- ALTER TABLE public.pokemon ENABLE ROW LEVEL SECURITY;

            -- Optional: Allow public access (if using anon key)
            -- CREATE POLICY "Allow public read" ON public.pokemon FOR SELECT USING (true);
            -- CREATE POLICY "Allow public insert" ON public.pokemon FOR INSERT WITH CHECK (true);
            """)
            return False
        else:
            print(f"Unexpected error: {e}")
            return False

    # If we got here, the table exists and we can access it
    print("✓ Database setup verification complete")
    return True

if __name__ == "__main__":
    print("Setting up Supabase database for Pokemon data...")
    print("=" * 50)

    success = setup_database()

    print("=" * 50)
    if success:
        print("✓ Setup completed successfully!")
        print("You can now use buscar_carta.py to fetch and store Pokemon data.")
        print("Each time a pokemon appears, its count will increment in the database.")
    else:
        print("✗ Setup incomplete. Please create the table manually as shown above.")
        exit(1)