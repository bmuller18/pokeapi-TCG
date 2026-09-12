import json
import time
import os
from dotenv import load_dotenv
from supabase import create_client, Client
from backend.services.pokemon_service import get_pokemon_by_id

# Load environment variables
load_dotenv()

def init_supabase():
    """Initialize Supabase client if credentials are present."""
    supabase_url = os.getenv('SUPABASE_URL')
    supabase_key = os.getenv('SUPABASE_KEY')
    if not supabase_url or not supabase_key:
        return None
    try:
        return create_client(supabase_url, supabase_key)
    except Exception as e:
        print(f"⚠️  Failed to initialize Supabase client: {e}")
        return None

def store_pokemon_data(supabase: Client, pokemon_data):
    """Store or update the complete Pokemon data in Supabase, incrementing count on duplicate."""
    try:
        pokemon_id = pokemon_data["id"]
        # Construct the official artwork URL as used elsewhere
        image_url = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/{pokemon_id}.png"

        # First, try to get the current record to see if it exists
        existing = supabase.table('pokemon').select('count').eq('id', pokemon_id).execute()

        if existing.data and len(existing.data) > 0:
            # Record exists, increment count
            current_count = existing.data[0].get('count', 0)
            new_count = current_count + 1
            # Update the count and other fields (in case they changed?)
            record = {
                "name": pokemon_data["name"],
                "image": image_url,
                "api_response": pokemon_data,
                "count": new_count
            }
            supabase.table('pokemon').update(record).eq('id', pokemon_id).execute()
            print(f"\n✅  Updated Pokémon id={pokemon_id} ({pokemon_data['name']}) count to {new_count} in Supabase.")
        else:
            # New record, set count to 1
            record = {
                "id": pokemon_id,
                "name": pokemon_data["name"],
                "image": image_url,
                "api_response": pokemon_data,
                "count": 1
            }
            supabase.table('pokemon').insert(record).execute()
            print(f"\n✅  Inserted new Pokémon id={pokemon_id} ({pokemon_data['name']}) with count=1 in Supabase.")
    except Exception as e:
        # Print the error for debugging
        print(f"\n⚠️  Error al almacenar en Supabase: {e}")
        # Also print the record we attempted to store (truncated for readability)
        try:
            print(f"   Record attempted: id={pokemon_id}, name={pokemon_data['name']}, image={image_url}, api_response keys: {list(pokemon_data.keys()) if isinstance(pokemon_data, dict) else 'not dict'}")
        except Exception:
            pass

def extract_required_fields(pokemon_data):
    """Extract only the fields requested: id, name, weight, height, types, HP, Attack, Speed."""
    try:
        pid = pokemon_data["id"]
        pname = pokemon_data["name"]
        pweight = pokemon_data["weight"]  # hectograms
        pheight = pokemon_data["height"]  # decimetres
        # Types: list of objects with type.name
        types = [t["type"]["name"] for t in pokemon_data.get("types", [])]
        # Stats: find by stat.name
        stats_map = {s["stat"]["name"]: s["base_stat"] for s in pokemon_data.get("stats", [])}
        php = stats_map.get("hp")
        patk = stats_map.get("attack")
        pspeed = stats_map.get("speed")
        result = {
            "id": pid,
            "name": pname,
            "weight": pweight,
            "height": pheight,
            "types": types,
            "hp": php,
            "attack": patk,
            "speed": pspeed
        }
        return result
    except Exception as e:
        # If something goes wrong, return minimal info
        return {
            "id": pokemon_data.get("id"),
            "name": pokemon_data.get("name"),
            "error": str(e)
        }

def main():
    try:
        # Initialize Supabase (may be None if not configured)
        supabase = init_supabase()

        # Try to get a valid pokemon (with retries in case of invalid IDs)
        max_attempts = 5
        pokemon_data = None

        for attempt in range(max_attempts):
            # Obtener 1 ID aleatorio
            random_ids = get_random_pokemon_ids(1)
            if not random_ids:
                if attempt < max_attempts - 1:
                    time.sleep(0.5)
                continue
            pokemon_id = random_ids[0]
            # Obtener los datos completos del pokemon
            try:
                pokemon_data = get_pokemon_by_id(pokemon_id)
                if pokemon_data:
                    break
            except Exception:
                pokemon_data = None
            if attempt < max_attempts - 1:
                time.sleep(0.5)

        if pokemon_data:
            # Extract required fields and print as JSON
            required = extract_required_fields(pokemon_data)
            print(json.dumps(required, ensure_ascii=False, indent=2))

            # Intentar almacenar en Supabase (si está configurado)
            if supabase:
                store_pokemon_data(supabase, pokemon_data)
            else:
                # Supabase not configured; inform user but continue
                print("\nℹ️  Supabase no configurado (falta SUPABASE_URL o SUPABASE_KEY en .env).")
                print("   Los datos se muestran arriba pero no se almacenan.")
                print("   Para almacenar, configure .env y asegúrese de que la columna 'api_response' y 'count' existan.\n")
        else:
            print("No se pudo obtener el pokemon despues de varios intentos")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()