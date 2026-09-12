import os
from dotenv import load_dotenv
from supabase import create_client, Client

# Load environment variables
load_dotenv()

def main():
    try:
        print("Probando si la columna 'count' existe en la tabla 'pokemon'...")
        print("=" * 60)

        # Initialize Supabase client
        supabase_url = os.getenv('SUPABASE_URL')
        supabase_key = os.getenv('SUPABASE_KEY')

        if not supabase_url or not supabase_key:
            print("Error: SUPABASE_URL y SUPABASE_KEY deben estar configurados en .env")
            return

        supabase = create_client(supabase_url, supabase_key)
        print(f"✓ Conectado a Supabase: {supabase_url}")

        # Try to insert a test record with count field
        test_data = {
            "id": 999999,  # Use a high ID unlikely to conflict
            "name": "test",
            "image": "test.jpg",
            "count": 5
        }

        print("\nIntentando insertar registro de prueba con campo 'count'...")
        try:
            result = supabase.table('pokemon').insert(test_data).execute()
            print("✓ Inserción exitosa - la columna 'count' EXISTE")
            print(f"  Resultado: {result.data}")

            # Clean up test record
            print("\nLimpiando registro de prueba...")
            supabase.table('pokemon').delete().eq('id', 999999).execute()
            print("✓ Registro de prueba eliminado")

        except Exception as e:
            error_msg = str(e)
            print(f"✗ Inserción falló: {error_msg}")

            if "could not find column" in error_msg or "does not exist" in error_msg:
                print("  Esto confirma que la columna 'count' NO existe en la tabla")
            elif "duplicate key" in error_msg:
                print("  Error de llave duplicada - la columna 'count' podría existir pero el ID ya está en uso")
                # Try with a different approach - maybe the ID 999999 already exists
                test_data["id"] = 999998
                try:
                    result = supabase.table('pokemon').insert(test_data).execute()
                    print("✓ Inserción exitosa con ID alternativo - la columna 'count' EXISTE")
                    supabase.table('pokemon').delete().eq('id', 999998).execute()
                except Exception as e2:
                    print(f"✗ También falló con ID alternativo: {e2}")
            else:
                print("  Error inesperado al intentar insertar con campo 'count'")

        # Also try inserting without count field to see what happens
        print("\nProbando inserción SIN campo 'count'...")
        test_data_no_count = {
            "id": 999997,
            "name": "test2",
            "image": "test2.jpg"
            # No count field
        }

        try:
            result = supabase.table('pokemon').insert(test_data_no_count).execute()
            print("✓ Inserción sin 'count' exitosa")
            supabase.table('pokemon').delete().eq('id', 999997).execute()
        except Exception as e:
            print(f"✗ Inserción sin 'count' falló: {e}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()