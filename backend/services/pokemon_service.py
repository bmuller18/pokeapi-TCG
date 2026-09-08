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