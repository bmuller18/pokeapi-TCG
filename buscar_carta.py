import os
from dotenv import load_dotenv
from supabase import create_client, Client
from backend.services.pokemon_service import get_random_pokemon_ids, get_pokemon_by_ids

# Load environment variables
load_dotenv()

def init_supabase():
    """Initialize Supabase client"""
    supabase_url = os.getenv('SUPABASE_URL')
    supabase_key = os.getenv('SUPABASE_KEY')

    if not supabase_url or not supabase_key:
        raise ValueError("SUPABASE_URL and SUPABASE_KEY must be set in .env file")

    return create_client(supabase_url, supabase_key)

def store_pokemon(supabase: Client, pokemon_data):
    """Store Pokémon data in Supabase table 'pokemon' with counter for duplicates"""
    try:
        pokemon_id = pokemon_data["id"]

        # First, try to get the existing record to see current count
        try:
            existing = supabase.table('pokemon').select('count').eq('id', pokemon_id).execute()

            if existing.data and len(existing.data) > 0:
                # Record exists, increment count
                current_count = existing.data[0].get('count', 0)
                new_count = current_count + 1

                # Update the record with incremented count
                # We also update name and image in case they changed (though they shouldn't for same id)
                supabase.table('pokemon').update({
                    "name": pokemon_data["name"],
                    "image": pokemon_data["image"],
                    "count": new_count
                }).eq('id', pokemon_id).execute()
            else:
                # Record doesn't exist, insert with count = 1
                supabase.table('pokemon').insert({
                    "id": pokemon_id,
                    "name": pokemon_data["name"],
                    "image": pokemon_data["image"],
                    "count": 1
                }).execute()

        except Exception as select_error:
            # If select fails (e.g., table doesn't have count column yet),
            # fall back to simple insert and hope the table has been altered
            # OR if it's a duplicate key error on insert, we'll try to update
            try:
                supabase.table('pokemon').insert({
                    "id": pokemon_id,
                    "name": pokemon_data["name"],
                    "image": pokemon_data["image"],
                    "count": 1
                }).execute()
            except Exception as insert_error:
                # If insert fails due to duplicate key, try to update
                if "duplicate key" in str(insert_error).lower() or "unique constraint" in str(insert_error).lower():
                    # Try to get current count and increment
                    try:
                        existing = supabase.table('pokemon').select('count').eq('id', pokemon_id).execute()
                        if existing.data and len(existing.data) > 0:
                            current_count = existing.data[0].get('count', 0)
                            new_count = current_count + 1
                            supabase.table('pokemon').update({
                                "name": pokemon_data["name"],
                                "image": pokemon_data["image"],
                                "count": new_count
                            }).eq('id', pokemon_id).execute()
                    except Exception:
                        # If we can't get current count, just update with count=1 (best effort)
                        supabase.table('pokemon').update({
                            "name": pokemon_data["name"],
                            "image": pokemon_data["image"],
                            "count": 1
                        }).eq('id', pokemon_id).execute()
                else:
                    # Some other error, ignore silently as storage is secondary
                    pass

    except Exception:
        # Silently ignore storage errors - primary function is to show name
        pass

def main():
    try:
        # Initialize Supabase - if this fails, we show error as it's critical for setup
        supabase = init_supabase()

        # Obtener 1 ID aleatorio
        random_ids = get_random_pokemon_ids(1)
        # Obtener los datos del pokemon
        pokemons = get_pokemon_by_ids(random_ids)
        if pokemons:
            pokemon = pokemons[0]

            # Store in Supabase with counter (non-critical operation - errors ignored)
            store_pokemon(supabase, pokemon)

            # Imprimir solo el nombre del primer (y único) pokemon
            print(pokemon["name"])
        else:
            print("No se pudo obtener el pokemon")
    except Exception as e:
        # Only show critical errors (like missing Supabase config)
        print(f"Error: {e}")

if __name__ == "__main__":
    main()