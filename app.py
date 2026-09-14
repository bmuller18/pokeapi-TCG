from flask import (
    Flask,
    render_template,
    request,
    url_for,
    redirect,
    flash,
    Blueprint,
    session
)
from backend.services.pokemon_service import get_pokemon_by_id, get_random_pokemon_ids
import json
from backend.config import get_supabase_client, FLASK_SECRET_KEY
from backend.services.user_pokemon_service import (
    add_pokemon_to_collection,
    get_user_collection
)
from functools import wraps





def fetch_pokemon(filters=None):
    """Fetch pokemon from Supabase with optional filters.
    filters: dict with keys 'gte_id', 'lte_id' (both int). If None, fetch all.
    Returns list of pokemon dicts ready for template.
    """
    supabase = get_supabase_client()
    if not supabase:
        return []
    try:
        query = supabase.table('pokemon').select('id, name, image, api_response, count').order('id')
        if filters:
            if 'gte_id' in filters and filters['gte_id'] is not None:
                query = query.gte('id', filters['gte_id'])
            if 'lte_id' in filters and filters['lte_id'] is not None:
                query = query.lte('id', filters['lte_id'])
        resp = query.execute()
        pokemon_list = []
        for row in resp.data or []:
            pid = row['id']
            pname = row['name']
            image_url = row['image'] or f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/{pid}.png"
            api_row = row.get('api_response')
            # Initialize defaults
            height = 0
            weight = 0
            types = []
            hp = 0
            attack = 0
            speed = 0
            pcount = row.get('count', 0) or 0
            if isinstance(api_row, dict):
                height = api_row.get('height', 0) or 0
                weight = api_row.get('weight', 0) or 0
                types = [t['type']['name'] for t in api_row.get('types', []) if t.get('type')]
                stats_map = {s['stat']['name']: s['base_stat'] for s in api_row.get('stats', []) if s.get('stat')}
                hp = stats_map.get('hp', 0) or 0
                attack = stats_map.get('attack', 0) or 0
                speed = stats_map.get('speed', 0) or 0
            pokemon_list.append({
                'id': pid,
                'name': pname,
                'height': height,  # decimetres
                'weight': weight,  # hectograms
                'types': types,
                'hp': hp,
                'attack': attack,
                'speed': speed,
                'image': image_url,
                'count': pcount
            })
        return pokemon_list
    except Exception as e:
        print(f"Error fetching from Supabase: {e}")
        return []

def get_pokemon_count():
    """Return total number of pokemon rows in Supabase."""
    supabase = get_supabase_client()
    if not supabase:
        return 0
    try:
        resp = supabase.table('pokemon').select('id', count='exact').execute()
        # resp.count holds the total count
        return resp.count if hasattr(resp, 'count') else 0
    except Exception as e:
        print(f"Error counting pokemon: {e}")
        return 0

def get_pokemon_from_supabase(pokemon_id):
    """Get a single pokemon from Supabase by id, including stored count and api_response."""
    supabase = get_supabase_client()
    if not supabase:
        return None
    try:
        resp = supabase.table('pokemon').select('id, name, image, api_response, count').eq('id', pokemon_id).single().execute()
        return resp.data
    except Exception as e:
        print(f"Error fetching pokemon {pokemon_id} from Supabase: {e}")
        return None

# Pokemon detail blueprint
pokemon_bp = Blueprint('pokemon', __name__)

@pokemon_bp.route('/pokemon/<int:pokemon_id>')
def pokemon_detail(pokemon_id):
    pokemon = get_pokemon_from_supabase(pokemon_id)
    if not pokemon:
        # Fallback to fetching from PokeAPI if not in Supabase
        try:
            pokemon_data = get_pokemon_by_id(pokemon_id)
            if not pokemon_data:
                from flask import abort
                abort(404)
            # Construct image URL
            image_url = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/{pokemon_id}.png"
            pokemon = {
                'id': pokemon_data['id'],
                'name': pokemon_data['name'],
                'image': image_url,
                'api_response': pokemon_data,
                'count': 0  # Not stored yet
            }
        except Exception:
            from flask import abort
            abort(404)
    return render_template('pokemon_detail.html', pokemon=pokemon, regions=REGIONS, active_region=None)

app = Flask(__name__)
app.secret_key = FLASK_SECRET_KEY

@app.context_processor
def inject_user():
    return {
        'current_user_email': session.get('email'),
        'current_user_id': session.get('user_id')
    }

def login_required(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if 'user_id' not in session:
            flash(
                'Debes iniciar sesión para acceder a esta página.',
                'error'
            )
            return redirect(url_for('login'))

        return view(*args, **kwargs)

    return wrapped_view

# Register blueprints
app.register_blueprint(pokemon_bp)

REGIONS = {
    "hisui": {"name": "Own Deck", "start": None, "end": None},
    "kanto": {"name": "Kanto", "start": 1, "end": 151},
    "johto": {"name": "Johto", "start": 152, "end": 251},
    "hoenn": {"name": "Hoenn", "start": 252, "end": 386},
    "sinnoh": {"name": "Sinnoh", "start": 387, "end": 493},
    "unova": {"name": "Unova", "start": 494, "end": 649},
    "kalos": {"name": "Kalos", "start": 650, "end": 721},
    "alola": {"name": "Alola", "start": 722, "end": 809},
    "galar": {"name": "Galar", "start": 810, "end": 898},  # special: historical, we can treat as no ID filter? maybe just show none unless we have specific IDs? We'll treat as no filter for now.
    "paldea": {"name": "Paldea", "start": 906, "end": 1025},
}

@app.route('/')
def index():
    if 'user_id' not in session:
        return render_template('index.html')

    pokemon_list = fetch_pokemon()
    total_count = get_pokemon_count()

    return render_template(
        'pokemon.html',
        pokemon_list=pokemon_list,
        regions=REGIONS,
        active_region=None,
        total_count=total_count,
        user_email=session.get('email')
    )

@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'GET':
        return render_template('register.html')

    email = request.form.get('email', '').strip()
    password = request.form.get('password', '')
    password_confirm = request.form.get('password_confirm', '')

    if not email or not password:
        flash('Completa todos los campos.', 'error')
        return redirect(url_for('register'))

    if password != password_confirm:
        flash('Las contraseñas no coinciden.', 'error')
        return redirect(url_for('register'))

    if len(password) < 6:
        flash('La contraseña debe tener al menos 6 caracteres.', 'error')
        return redirect(url_for('register'))

    supabase = get_supabase_client()

    if not supabase:
        flash('Supabase no está configurado.', 'error')
        return redirect(url_for('register'))

    try:

        response = supabase.auth.sign_up({
        'email': email,
        'password': password,
        'options': {
            'email_redirect_to':
                'http://127.0.0.1:5000/auth/callback'
            }
        })

        if response.user:
            flash(
                'Cuenta creada correctamente. Revisa tu email para confirmar la cuenta.',
                'success'
            )
            return redirect(url_for('login'))

        flash('No se pudo crear la cuenta.', 'error')
        return redirect(url_for('register'))

    except Exception as e:
        print("=" * 60)
        print("ERROR REAL DE SUPABASE AL REGISTRAR:")
        print(repr(e))
        print("=" * 60)

        flash(f"Error: {e}", "error")
        return render_template("register.html")

@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'GET':
        return render_template('login.html')

    email = request.form.get('email', '').strip()
    password = request.form.get('password', '')

    if not email or not password:
        flash('Completa todos los campos.', 'error')
        return redirect(url_for('login'))

    supabase = get_supabase_client()

    if not supabase:
        flash('Supabase no está configurado.', 'error')
        return redirect(url_for('login'))

    try:

        response = supabase.auth.sign_in_with_password({
            'email': email,
            'password': password
        })

        if response.user and response.session:
            session['user_id'] = str(response.user.id)
            session['email'] = response.user.email
            session['access_token'] = response.session.access_token

            flash('Sesión iniciada correctamente.', 'success')
            return redirect(url_for('index'))

        flash('No se pudo iniciar sesión.', 'error')
        return redirect(url_for('login'))

    except Exception as e:
        print("=" * 60)
        print("ERROR REAL DE LOGIN:")
        print(repr(e))
        print("=" * 60)

        flash(f'Error: {e}', 'error')
        return redirect(url_for('login'))

@app.route('/auth/callback')
def auth_callback():
    code = request.args.get('code')

    if not code:
        flash(
            'No se recibió el código de autenticación.',
            'error'
        )
        return redirect(url_for('login'))

    supabase = get_supabase_client()

    if not supabase:
        flash(
            'Supabase no está configurado.',
            'error'
        )
        return redirect(url_for('login'))

    try:
        response = supabase.auth.exchange_code_for_session(code)

        if not response.user:
            flash(
                'No se pudo obtener el usuario autenticado.',
                'error'
            )
            return redirect(url_for('login'))

        session['user_id'] = str(response.user.id)
        session['email'] = response.user.email
        session['access_token'] = response.session.access_token

        flash(
            'Cuenta confirmada correctamente.',
            'success'
        )

        return redirect(url_for('index'))

    except Exception as e:
        print("=" * 60)
        print("ERROR REAL EN AUTH CALLBACK:")
        print(repr(e))
        print("=" * 60)

        flash(
            'No se pudo completar la autenticación.',
            'error'
        )

        return redirect(url_for('login'))

@app.route('/logout')
def logout():

    supabase = get_supabase_client()

    try:
        if supabase:
            supabase.auth.sign_out()
    except Exception as e:
        print(f'Error signing out: {e}')

    session.clear()

    flash('Sesión cerrada correctamente.', 'success')

    return redirect(url_for('index'))

@app.route('/collection')
@login_required
def collection():

    user_id = session['user_id']
    access_token = session.get('access_token')

    if not access_token:
        flash(
            'Tu sesión ha expirado. Inicia sesión nuevamente.',
            'error'
        )

        return redirect(url_for('login'))

    collection = get_user_collection(
        user_id,
        access_token
    )

    return render_template(
        'collection.html',
        collection=collection
    )

@app.route('/collection/add/<int:pokemon_id>',methods=['POST'])
@login_required
def add_to_collection(pokemon_id):

    user_id = session['user_id']
    access_token = session.get('access_token')

    if not access_token:
        flash(
            'Tu sesión ha expirado. Inicia sesión nuevamente.',
            'error'
        )

        return redirect(url_for('login'))

    success, message = add_pokemon_to_collection(
        user_id,
        pokemon_id,
        access_token
    )

    flash(
        message,
        'success' if success else 'error'
    )

    return redirect(
        request.referrer or url_for('index')
    )

@app.route('/region/<slug>')
@login_required
def region(slug):
    region_info = REGIONS.get(slug)
    if not region_info:
        # If region not found, fallback to all
        pokemon_list = fetch_pokemon()
        active = None
    else:
        start = region_info.get('start')
        end = region_info.get('end')
        filters = {}
        if start is not None:
            filters['gte_id'] = start
        if end is not None:
            filters['lte_id'] = end
        pokemon_list = fetch_pokemon(filters)
        active = slug
    # For hisui (historical) we have no ID range; we will show none unless we have specific IDs? We'll just show empty list.
    total_count = get_pokemon_count()
    return render_template(
        'pokemon.html',
        pokemon_list=pokemon_list,
        regions=REGIONS,
        active_region=active,
        total_count=total_count,
        user_email=session.get('email')
    )

@app.route('/search-random')
@login_required
def search_random():
    supabase = get_supabase_client()
    if not supabase:
        flash('Supabase not configured', 'error')
        return redirect(request.referrer or url_for('index'))
    try:
        # get 3 random ids up to 1025
        ids = get_random_pokemon_ids(3, max_id=1025)
        stored = 0
        for pid in ids:
            pokemon_data = get_pokemon_by_id(pid)
            if pokemon_data:
                image_url = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/{pid}.png"
                # Check current count
                existing = supabase.table('pokemon').select('count').eq('id', pid).execute()
                if existing.data and len(existing.data) > 0:
                    current_count = existing.data[0].get('count', 0)
                    new_count = current_count + 1
                    # Update the record
                    supabase.table('pokemon').update({
                        "name": pokemon_data["name"],
                        "image": image_url,
                        "api_response": pokemon_data,
                        "count": new_count
                    }).eq('id', pid).execute()
                else:
                    # Insert new record with count 1
                    supabase.table('pokemon').insert({
                        "id": pid,
                        "name": pokemon_data["name"],
                        "image": image_url,
                        "api_response": pokemon_data,
                        "count": 1
                    }).execute()
                stored += 1
        flash(f'Se han buscado y almacenado {stored} pokémons al azar.', 'success')
    except Exception as e:
        flash(f'Error: {e}', 'error')
    return redirect(request.referrer or url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)