from backend.config import get_supabase_client


def add_pokemon_to_collection(user_id, pokemon_id):
    """Add a Pokémon to the user's collection."""

    supabase = get_supabase_client()

    if not supabase:
        return False, "Supabase no está configurado."

    try:
        response = (
            supabase
            .table("user_pokemon")
            .insert({
                "user_id": user_id,
                "pokemon_id": pokemon_id
            })
            .execute()
        )

        return True, "Pokémon agregado a tu colección."

    except Exception as e:

        error_message = str(e)

        # PostgreSQL unique constraint
        if "23505" in error_message:
            return False, "Este Pokémon ya está en tu colección."

        print(f"Error adding Pokémon to collection: {e}")

        return False, "No se pudo agregar el Pokémon."