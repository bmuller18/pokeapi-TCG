import requests


BASE_URL = "https://pokeapi.co/api/v2/pokemon"


def get_pokemon_by_id(pokemon_id):
    url = f"{BASE_URL}/{pokemon_id}"

    response = requests.get(url, timeout=10)
    response.raise_for_status()

    return response.json()


def get_first_150_pokemon():
    url = f"{BASE_URL}?limit=150&offset=0"

    response = requests.get(url, timeout=10)
    response.raise_for_status()

    data = response.json()

    pokemon_list = []

    for pokemon in data["results"]:
        pokemon_id = pokemon["url"].rstrip("/").split("/")[-1]

        pokemon_list.append({
            "id": int(pokemon_id),
            "name": pokemon["name"],
            "image": (
                "https://raw.githubusercontent.com/PokeAPI/"
                "sprites/master/sprites/pokemon/other/"
                f"official-artwork/{pokemon_id}.png"
            )
        })

    return pokemon_list


def get_all_pokemon():
    # First, get the total count of Pokémon
    count_url = f"{BASE_URL}?limit=0"
    count_response = requests.get(count_url, timeout=10)
    count_response.raise_for_status()
    total_count = count_response.json()["count"]

    # Then, get all Pokémon using the total count as limit
    url = f"{BASE_URL}?limit={total_count}&offset=0"
    response = requests.get(url, timeout=15)  # Slightly longer timeout for larger request
    response.raise_for_status()

    data = response.json()

    pokemon_list = []

    for pokemon in data["results"]:
        pokemon_id = pokemon["url"].rstrip("/").split("/")[-1]

        pokemon_list.append({
            "id": int(pokemon_id),
            "name": pokemon["name"],
            "image": (
                "https://raw.githubusercontent.com/PokeAPI/"
                "sprites/master/sprites/pokemon/other/"
                f"official-artwork/{pokemon_id}.png"
            )
        })

    return pokemon_list


def get_generations():
    """Get list of all generations with their main region names"""
    url = f"https://pokeapi.co/api/v2/generation?limit=20"

    response = requests.get(url, timeout=10)
    response.raise_for_status()

    data = response.json()

    generations = []
    # Map generation IDs to region names for display
    region_names = {
        1: "Kanto",
        2: "Johto",
        3: "Hoenn",
        4: "Sinnoh",
        5: "Unova",
        6: "Kalos",
        7: "Alola",
        8: "Galar",
        9: "Paldea"
    }

    for gen in data["results"]:
        # Extract generation ID from URL (e.g., "/api/v2/generation/1/" -> 1)
        gen_id = int(gen["url"].split("/")[-2])
        generations.append({
            "id": gen_id,
            "name": gen["name"],
            "region": region_names.get(gen_id, f"Region {gen_id}")
        })

    return generations


def get_pokemon_by_generation(generation_id):
    """Get all Pokémon for a specific generation"""
    # First, get the generation details to get the Pokémon species
    gen_url = f"https://pokeapi.co/api/v2/generation/{generation_id}"

    gen_response = requests.get(gen_url, timeout=10)
    gen_response.raise_for_status()
    gen_data = gen_response.json()

    pokemon_list = []

    # For each Pokémon species in this generation, get the basic Pokémon data
    for pokemon_species in gen_data["pokemon_species"]:
        # Extract Pokémon ID from the species URL
        # Example: "https://pokeapi.co/api/v2/pokemon-species/1/" -> 1
        pokemon_id = int(pokemon_species["url"].split("/")[-2])

        # Get the basic Pokémon data (for sprites, etc.)
        pokemon_url = f"{BASE_URL}/{pokemon_id}"
        pokemon_response = requests.get(pokemon_url, timeout=10)
        pokemon_response.raise_for_status()
        pokemon_data = pokemon_response.json()

        pokemon_list.append({
            "id": pokemon_data["id"],
            "name": pokemon_data["name"],
            "image": (
                "https://raw.githubusercontent.com/PokeAPI/"
                "sprites/master/sprites/pokemon/other/"
                f"official-artwork/{pokemon_id}.png"
            )
        })

    # Sort by ID to maintain consistent order
    pokemon_list.sort(key=lambda x: x["id"])
    return pokemon_list