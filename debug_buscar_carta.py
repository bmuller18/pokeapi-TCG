import os
from dotenv import load_dotenv
from supabase import create_client, Client
from backend.services.pokemon_service import get_random_pokemon_ids, get_pokemon_by_ids

# Load environment variables
load_dotenv()

def main():
    try:
        print("Step 1: Initializing Supabase...")
        supabase_url = os.getenv('SUPABASE_URL')
        supabase_key = os.getenv('SUPABASE_KEY')
        print(f"  URL: {supabase_url}")
        print(f"  Key present: {bool(supabase_key)}")

        if not supabase_url or not supabase_key:
            raise ValueError("SUPABASE_URL and SUPABASE_KEY must be set in .env file")

        supabase = create_client(supabase_url, supabase_key)
        print("  ✓ Supabase client initialized")

        print("Step 2: Getting random Pokemon ID...")
        random_ids = get_random_pokemon_ids(1)
        print(f"  Got IDs: {random_ids}")

        if not random_ids:
            print("  ✗ No IDs returned")
            return

        print("Step 3: Getting Pokemon data...")
        pokemons = get_pokemon_by_ids(random_ids)
        print(f"  Got pokemon data: {pokemons}")

        if not pokemons:
            print("  ✗ No pokemon data returned")
            return

        pokemon = pokemons[0]
        print(f"  Selected pokemon: {pokemon['name']} (ID: {pokemon['id']})")

        print("Step 4: Storing in Supabase...")
        try:
            # Prepare data for insertion/upsert
            data = {
                "id": pokemon["id"],
                "name": pokemon["name"],
                "image": pokemon["image"]
            }
            print(f"  Data to store: {data}")

            # Try upsert
            result = supabase.table('pokemon').upsert(data, on_conflict='id').execute()
            print(f"  ✓ Upsert successful: {result}")
        except Exception as e:
            print(f"  ✗ Upsert failed: {e}")
            print("  Trying regular insert...")
            try:
                result = supabase.table('pokemon').insert(data).execute()
                print(f"  ✓ Insert successful: {result}")
            except Exception as e2:
                print(f"  ✗ Insert also failed: {e2}")

        print("Step 5: Printing pokemon name...")
        print(pokemon["name"])
        print("✓ Done!")

    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()