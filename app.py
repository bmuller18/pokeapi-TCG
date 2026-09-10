from flask import Flask

from backend.routes.pokemon_routes import pokemon_bp


app = Flask(__name__)
app.secret_key = 'pokeapi-explorer-secret-key-change-in-production'  # In production, use a proper secret key

app.register_blueprint(pokemon_bp)


if __name__ == "__main__":
    app.run(debug=True, port=5000)