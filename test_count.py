from app import fetch_pokemon

pokemon_list = fetch_pokemon()
if pokemon_list:
    print(f"First pokemon: {pokemon_list[0]['name']} with count: {pokemon_list[0].get('count', 'NOT FOUND')}")
else:
    print("No pokemon found")