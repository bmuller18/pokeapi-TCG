from flask import Blueprint, render_template, request, session
import requests

from backend.services.pokemon_service import (
    get_pokemon_by_id,
    get_random_pokemon_ids,
    get_pokemon_by_ids,
    get_pokemon_species
)


pokemon_bp = Blueprint("pokemon", __name__)


@pokemon_bp.route("/", methods=["GET", "POST"])
def index():

    pokemon = None
    error = None
    random_pokemons = None
    show_random = False

    # Initialize discovered regions in session if not present
    if 'discovered_regions' not in session:
        session['discovered_regions'] = []

    # Handle form submission
    if request.method == "POST":
        action = request.form.get("action")

        if action == "random":
            # Show 3 random Pokémon with their region information
            try:
                random_ids = get_random_pokemon_ids(3)
                random_pokemons_data = get_pokemon_by_ids(random_ids)

                # Enhance each Pokémon with region information and add to discovered regions
                random_pokemons = []
                newly_discovered_regions = set()  # Use set to avoid duplicates within the same batch
                for pokemon_data in random_pokemons_data:
                    try:
                        # Get species data to find generation/region
                        species_data = get_pokemon_species(pokemon_data["id"])
                        generation_name = species_data["generation"]["name"]  # e.g., "generation-i"

                        # Map generation to region name
                        generation_to_region = {
                            "generation-i": "Kanto",
                            "generation-ii": "Johto",
                            "generation-iii": "Hoenn",
                            "generation-iv": "Sinnoh",
                            "generation-v": "Unova",
                            "generation-vi": "Kalos",
                            "generation-vii": "Alola",
                            "generation-viii": "Galar",
                            "generation-ix": "Paldea"
                        }
                        region = generation_to_region.get(generation_name, "Desconocida")

                        # Add region information to pokemon data
                        pokemon_data["region"] = region
                        random_pokemons.append(pokemon_data)

                        # Add region to discovered regions if not already there and not unknown
                        if region != "Desconocida" and region not in session['discovered_regions']:
                            newly_discovered_regions.add(region)
                    except Exception:
                        # If we can't get species data, still include the pokemon without region
                        pokemon_data["region"] = "Desconocida"
                        random_pokemons.append(pokemon_data)

                # Update discovered regions in session
                session['discovered_regions'].extend(list(newly_discovered_regions))
                # Mark session as modified to ensure it's saved
                session.modified = True

                show_random = True
            except requests.exceptions.RequestException:
                error = "No se pudo conectar con PokeAPI."
        else:
            # Regular search by ID
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

    # Get discovered regions from session for template
    discovered_regions = session.get('discovered_regions', [])

    return render_template(
        "pokemon.html",
        pokemon=pokemon,
        random_pokemons=random_pokemons,
        show_random=show_random,
        discovered_regions=discovered_regions,
        error=error
    )