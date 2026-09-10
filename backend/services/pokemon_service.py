import requests
import random


BASE_URL = "https://pokeapi.co/api/v2/pokemon"


def get_pokemon_by_id(pokemon_id):
    """Get a specific Pokémon by ID"""
    url = f"{BASE_URL}/{pokemon_id}"

    response = requests.get(url, timeout=10)
    response.raise_for_status()

    return response.json()


def get_random_pokemon_ids(count=3):
    """Get random Pokémon IDs by first getting the total count"""
    # Get total count of Pokémon
    count_url = f"{BASE_URL}?limit=0"
    count_response = requests.get(count_url, timeout=10)
    count_response.raise_for_status()
    total_count = count_response.json()["count"]

    # Generate random IDs (making sure they're within valid range)
    random_ids = []
    for _ in range(count):
        # Pokémon IDs start at 1, so we use randint(1, total_count)
        random_ids.append(random.randint(1, total_count))

    return random_ids


def get_pokemon_by_ids(pokemon_ids):
    """Get multiple Pokémon by their IDs"""
    pokemon_list = []
    for pokemon_id in pokemon_ids:
        try:
            pokemon_data = get_pokemon_by_id(pokemon_id)
            pokemon_list.append({
                "id": pokemon_data["id"],
                "name": pokemon_data["name"],
                "image": (
                    "https://raw.githubusercontent.com/PokeAPI/"
                    "sprites/master/sprites/pokemon/other/"
                    f"official-artwork/{pokemon_id}.png"
                )
            })
        except Exception:
            # Skip invalid IDs and continue
            continue
    return pokemon_list


def get_pokemon_species(pokemon_id):
    """Get Pokemon species data which includes generation information"""
    url = f"https://pokeapi.co/api/v2/pokemon-species/{pokemon_id}"

    response = requests.get(url, timeout=10)
    response.raise_for_status()

    return response.json()