from flask import Blueprint, render_template, request
import requests

from backend.services.pokemon_service import get_pokemon_by_id


pokemon_bp = Blueprint("pokemon", __name__)


@pokemon_bp.route("/", methods=["GET", "POST"])
def index():

    pokemon = None
    error = None

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

            except requests.exceptions.RequestException as e:
                print(f"Error de conexión: {e}")
                error = "No se pudo conectar con PokeAPI."

    return render_template(
        "pokemon.html",
        pokemon=pokemon,
        error=error
    )