from flask import Blueprint, render_template, request
import requests

from backend.services.pokemon_service import (
    get_pokemon_by_id,
    get_first_150_pokemon,
    get_all_pokemon,
    get_generations,
    get_pokemon_by_generation
)


pokemon_bp = Blueprint("pokemon", __name__)


@pokemon_bp.route("/", methods=["GET", "POST"])
def index():

    pokemon = None
    error = None

    # Get all generations for the navigation menu
    generations = get_generations()

    # Get selected region from query parameters (default to None for all)
    selected_region = request.args.get('region', type=int)

    # Get Pokémon list based on selection
    if selected_region is not None:
        # Validate that the region ID exists in our generations
        valid_region_ids = [g['id'] for g in generations]
        if selected_region in valid_region_ids:
            pokemon_list = get_pokemon_by_generation(selected_region)
        else:
            # Invalid region, fall back to all Pokémon
            pokemon_list = get_all_pokemon()
            selected_region = None
    else:
        # No region selected, show all Pokémon
        pokemon_list = get_all_pokemon()

    # Limit to first 1025 Pokémon (ID ≤ 1025)
    pokemon_list = [pokemon for pokemon in pokemon_list if pokemon['id'] <= 1025]

    # Buscar Pokémon
    if request.method == "POST":

        pokemon_id = request.form.get("pokemon_id", "").strip()

        if not pokemon_id:
            error = "Introduce un ID de Pokémon."

        elif not pokemon_id.isdigit():
            error = "El ID debe ser un número."

        else:
            try:
                pokemon = get_pokemon_by_id(pokemon_id)

            except requests.exceptions.HTTPError:
                error = f"No existe un Pokémon con el ID {pokemon_id}."

            except requests.exceptions.RequestException:
                error = "No se pudo conectar con PokeAPI."

    return render_template(
        "pokemon.html",
        pokemon=pokemon,
        pokemon_list=pokemon_list,
        generations=generations,
        selected_region=selected_region,
        error=error
    )