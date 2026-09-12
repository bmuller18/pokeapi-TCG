import os
from dotenv import load_dotenv
from supabase import create_client, Client

# Load environment variables
load_dotenv()

def main():
    try:
        print("Verificando conexión a Supabase y datos almacenados...")
        print("=" * 60)

        # Initialize Supabase client
        supabase_url = os.getenv('SUPABASE_URL')
        supabase_key = os.getenv('SUPABASE_KEY')

        if not supabase_url or not supabase_key:
            print("Error: SUPABASE_URL y SUPABASE_KEY deben estar configurados en .env")
            return

        supabase = create_client(supabase_url, supabase_key)
        print(f"✓ Conectado a Supabase: {supabase_url}")

        # Try to get records with id, name, and count
        try:
            print("\nObteniendo registros con contador...")
            result = supabase.table('pokemon').select('id, name, count').execute()

            if result.data:
                # Sort by count descending in Python
                sorted_data = sorted(result.data, key=lambda x: x['count'], reverse=True)

                print(f"✓ Se obtuvieron {len(sorted_data)} registros con contador:")
                print("-" * 40)
                print(f"{'ID':<5} {'Nombre':<15} {'Count':<6}")
                print("-" * 40)

                for pokemon in sorted_data:
                    print(f"{pokemon['id']:<5} {pokemon['name']:<15} {pokemon['count']:<6}")

                print("-" * 40)
                total_appearances = sum(p['count'] for p in sorted_data)
                print(f"Total de apariciones registradas: {total_appearances}")

                # Show which Pokemon has appeared most
                if sorted_data:
                    top = sorted_data[0]
                    if top['count'] > 1:
                        print(f"\n🏆 Pokémon más frecuente: {top['name']} (ID {top['id']}) - {top['count']} apariciones")
                    else:
                        print(f"\nℹ️  Todos los Pokémon han aparecido solo una vez hasta ahora")
            else:
                print("  No se encontraron registros")

        except Exception as e:
            print(f"✗ Error al obtener registros con contador: {e}")
            print("  Esto podría indicar que la columna 'count' no existe o tiene un nombre diferente")

            # Try to get column information by getting one record and seeing what's available
            try:
                print("\nIntentando determinar estructura de la tabla...")
                result = supabase.table('pokemon').select('*').limit(1).execute()
                if result.data:
                    columns = list(result.data[0].keys())
                    print(f"  Columnas detectadas: {columns}")

                    # Check if we have a count-like column
                    count_columns = [col for col in columns if 'count' in col.lower()]
                    if count_columns:
                        print(f"  Posibles columnas de contador: {count_columns}")
                    else:
                        print("  ⚠ No se encontró columna obvia de contador")
                else:
                    print("  No hay datos para determinar estructura")
            except Exception as e2:
                print(f"  También falló intento de determinar estructura: {e2}")

        # Show all columns for one record to confirm structure
        try:
            print("\nMostrando datos completos de un registro...")
            result = supabase.table('pokemon').select('*').limit(1).execute()
            if result.data:
                print("  Estructura de un registro:")
                for key, value in result.data[0].items():
                    print(f"    {key}: {value} ({type(value).__name__})")
            else:
                print("  No hay registros para mostrar")
        except Exception as e:
            print(f"✗ Error al mostrar estructura: {e}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()