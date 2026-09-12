# Pokemon TCG Explorer (Simplified CLI Version)

This is a simplified command-line tool that fetches random Pokemon data from the PokeAPI and can store tracking information in a Supabase database.

## Current Functionality

When you run `buscar_carta.py`:
1. Fetches a random Pokemon from the PokeAPI
2. Shows only the Pokemon name in the terminal (bash)
3. Optionally stores tracking data in Supabase (if configured)

## Features

- **Random Pokemon Selection**: Uses PokeAPI to get a random Pokemon
- **Terminal Output**: Prints only the Pokemon name to stdout
- **Supabase Tracking** (Optional): 
  - Tracks how many times each Pokemon has appeared
  - Uses a counter in the database that increments on duplicates
  - Stores Pokemon ID, name, image URL, appearance count, and timestamp

## Setup

### 1. Configure Supabase
Create a `.env` file in the project root with:
```
SUPABASE_URL=your_supabase_project_url
SUPABASE_KEY=your_supabase_anon_key
```

### 2. Database Setup
Run the setup script to verify your Supabase connection and get table creation instructions:
```bash
. venv/bin/activate && python setup_supabase_flask.py
```

The script will tell you exactly how to create the required table. You need a table named `pokemon` with these columns:
- `id` (integer, primary key) - Pokemon ID from PokeAPI
- `name` (text) - Pokemon name
- `image` (text) - URL to official artwork
- `count` (integer, default: 1) - Tracks appearances (increments on duplicates)
- `created_at` (timestamp with timezone, default: now())

### 3. Install Dependencies
```bash
. venv/bin/activate && pip install -r requirements.txt
```

## Usage

```bash
. venv/bin/activate && python buscar_carta.py
```

Example output:
```
pikachu
```

Each time you run the script, it will show a random Pokemon name. If you have Supabase configured correctly, it will also:
- Insert new Pokemon records with count = 1
- Increment the count column when the same Pokemon appears again

## Files

- `buscar_carta.py` - Main script: fetches random Pokemon, shows name, optionally stores in Supabase
- `setup_supabase_flask.py` - Helper script to verify Supabase connection and table setup
- `backend/services/pokemon_service.py` - Service layer for Pokemon API interactions
- `requirements.txt` - Python dependencies

## Notes

- The Supabase storage is optional - the script will work without it (just showing the Pokemon name)
- Storage errors are ignored silently to ensure the main function (showing Pokemon name) always works
- The count feature requires the `count` column to exist in your Supabase table