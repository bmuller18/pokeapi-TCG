import requests


BASE_URL = "https://pokeapi.co/api/v2/pokemon"


def get_pokemon_by_id(pokemon_id):
    url = f"{BASE_URL}/{pokemon_id}"

    response = requests.get(url, timeout=10)
    response.raise_for_status()

    return response.json()