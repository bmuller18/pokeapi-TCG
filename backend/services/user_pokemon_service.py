from backend.config import get_authenticated_supabase_client

def add_pokemon_to_collection(
    user_id,
    pokemon_id,
    access_token):
    """Add a Pokémon to the user's collection."""

    supabase = get_authenticated_supabase_client(
        access_token
    )

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

        if "23505" in error_message:
            return False, "Este Pokémon ya está en tu colección."

        print(
            f"Error adding Pokémon to collection: {e}"
        )

        return False, "No se pudo agregar el Pokémon."

def get_user_collection(
    user_id,
    access_token):
    """Get all Pokémon in the user's collection."""

    supabase = get_authenticated_supabase_client(
        access_token
    )

    if not supabase:
        return []

    try:
        response = (
            supabase
            .table("user_pokemon")
            .select(
                """
                pokemon_id,
                pokemon (
                    id,
                    name,
                    image,
                    api_response,
                    count
                )
                """
            )
            .eq("user_id", user_id)
            .order("pokemon_id")
            .execute()
        )

        collection = []

        for item in response.data or []:

            pokemon = item.get("pokemon")

            if pokemon:
                collection.append(pokemon)

        return collection

    except Exception as e:

        print(
            f"Error getting user collection: {e}"
        )

        return []
    """Get all Pokémon in the user's collection."""

    supabase = get_supabase_client()

    if not supabase:
        return []

    try:
        response = (
            supabase
            .table("user_pokemon")
            .select(
                """
                pokemon_id,
                pokemon (
                    id,
                    name,
                    image,
                    api_response,
                    count
                )
                """
            )
            .eq("user_id", user_id)
            .order("pokemon_id")
            .execute()
        )

        collection = []

        for item in response.data or []:
            pokemon = item.get("pokemon")

            if pokemon:
                collection.append(pokemon)

        return collection

    except Exception as e:
        print(f"Error getting user collection: {e}")
        return []
    supabase = get_supabase_client()

    if not supabase:
        return []

    try:
        response = (
            supabase
            .table('user_pokemon')
            .select('*')
            .eq('user_id', user_id)
            .order('pokemon_id')
            .execute()
        )

        return response.data or []

    except Exception as e:
        print(f"Error getting user collection: {e}")
        return []