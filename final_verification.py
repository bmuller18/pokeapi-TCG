import os
from dotenv import load_dotenv
from supabase import create_client, Client

# Load environment variables
load_dotenv()

def main():
    try:
        print("✅ VERIFICACIÓN FINAL: Pokemon cargados en Supabase")
        print("=" * 60)

        # Initialize Supabase client
        supabase_url = os.getenv('SUPABASE_URL')
        supabase_key = os.getenv('SUPABASE_KEY')

        if not supabase_url or not supabase_key:
            print("❌ Error: SUPABASE_URL y SUPABASE_KEY deben estar configurados en .env")
            return

        supabase = create_client(supabase_url, supabase_key)
        print(f"🔗 Conectado a Supabase: {supabase_url}")

        # Get all records from the pokemon table
        try:
            result = supabase.table('pokemon').select('id, name, image, created_at').execute()

            if result.data:
                print(f"\n📊 SE ENCONTRARON {len(result.data)} REGISTROS EN LA TABLA 'pokemon':")
                print("-" * 60)
                print(f"{'#':<3} {'ID':<6} {'Nombre':<15} {'Fecha de creación'}")
                print("-" * 60)

                for i, pokemon in enumerate(result.data, 1):
                    # Format created_at for display
                    created_at = pokemon['created_at'][:19].replace('T', ' ') if pokemon['created_at'] else 'N/A'
                    print(f"{i:<3} {pokemon['id']:<6} {pokemon['name']:<15} {created_at}")

                print("-" * 60)

                # Show summary
                print(f"\n📈 RESUMEN:")
                print(f"   • Total de especies diferentes de Pokémon almacenadas: {len(result.data)}")

                # Check if we have any actual duplicates by looking for same ID
                ids = [p['id'] for p in result.data]
                unique_ids = set(ids)
                if len(ids) == len(unique_ids):
                    print(f"   • Todas las entradas tienen IDs únicos (no hay duplicados en la tabla)")
                else:
                    from collections import Counter
                    id_counts = Counter(ids)
                    duplicates = [id for id, count in id_counts.items() if count > 1]
                    print(f"   • IDs duplicados encontrados: {duplicates}")

            else:
                print("\n⚠ No se encontraron registros en la tabla 'pokemon'")
                print("  Ejecuta 'buscar_carta.py' varias veces para almacenar algunos Pokémon")

        except Exception as e:
            print(f"\n❌ Error al consultar la tabla 'pokemon': {e}")

        # Test the main functionality
        print("\n" + "=" * 60)
        print("🧪 PROBANDO FUNCIÓN PRINCIPAL DE buscar_carta.py:")
        print("-" * 60)

        try:
            from backend.services.pokemon_service import get_random_pokemon_ids, get_pokemon_by_ids
            random_ids = get_random_pokemon_ids(1)
            pokemons = get_pokemon_by_ids(random_ids)
            if pokemons:
                pokemon_name = pokemons[0]["name"]
                print(f"   Próximo Pokémon que se mostraría: {pokemon_name}")
                print("   (Este sería el salida en bash al ejecutar buscar_carta.py)")
            else:
                print("   ❌ No se pudo obtener datos de Pokémon")
        except Exception as e:
            print(f"   ❌ Error al obtener Pokémon: {e}")

    except Exception as e:
        print(f"❌ Error inesperado: {e}")

if __name__ == "__main__":
    main()