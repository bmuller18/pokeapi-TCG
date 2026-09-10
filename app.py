from flask import Flask

from backend.routes.pokemon_routes import pokemon_bp


app = Flask(__name__)

app.register_blueprint(pokemon_bp)


if __name__ == "__main__":
    app.run(debug=True, port=5001)