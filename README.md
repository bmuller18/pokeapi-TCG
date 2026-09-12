# Pokemon TCG Explorer (Flask Version)

Esta aplicación Flask muestra los Pokémon que tienes almacenados en tu base de datos Supabase.

## Funcionalidad

- Lee todos los registros de la tabla `pokemon` en Supabase.
- Para cada registro, extrae los siguientes campos (usando la columna `api_response` que contiene el JSON completo de la PokeAPI):
  - `id`
  - `name`
  - `height` (decímetros, convertido a metros en la plantilla)
  - `weight` (hectogramos, convertido a kg en la plantilla)
  - `types` (lista de tipos)
  - `hp` (puntos de salud)
  - `attack` (ataque)
  - `speed` (velocidad)
- Muestra una tarjeta para cada Pokémon con su imagen, nombre, tipos, altura, peso y estadísticas (HP, Ataque, Velocidad) incluyendo barras de progreso.
- Si no hay Pokémon almacenados, muestra un mensaje indicando que ejecutar `buscar_carta.py` para guardar algunos.

## Requisitos

- Python 3.x
- Paquetes listados en `requirements.txt`
- Una base de datos Supabase con una tabla `pokemon` que al menos tenga las columnas:
  - `id` (integer, primary key)
  - `name` (text)
  - `image` (text)
  - `api_response` (jsonb) - contiene el JSON completo de la PokeAPI
  - Opcionalmente: `count`, `created_at`

## Configuración

1. Copia tus credenciales de Supabase a un archivo `.env` en la raíz del proyecto:
   ```
   SUPABASE_URL=tu_url_de_supabase
   SUPABASE_KEY=tu_anon_key_de_supabase
   ```

2. Asegúrate de que la tabla `pokemon` exista y tenga la columna `api_response`. Si no existe, ejecuta esta SQL una vez en el editor SQL de tu proyecto Supabase:
   ```sql
   ALTER TABLE public.pokemon 
   ADD COLUMN IF NOT EXISTS api_response JSONB;
   ```

3. (Opcional) Para almacenar Pokémon en la base de datos, ejecuta el script CLI:
   ```bash
   . venv/bin/activate && python buscar_carta.py
   ```
   Este script obtiene un Pokémon aleatorio de la PokeAPI, muestra su JSON completo en la terminal y lo almacena/actualiza en Supabase.

## Uso

```bash
. venv/bin/activate && python app.py
```

Luego abre tu navegador en `http://localhost:5000` (o `http://127.0.0.1:5000`).

## Estructura del proyecto

```
pokeapi/
├─ app.py                     # ← Aplicación Flask principal
├─ buscar_carta.py            # ← Script CLI para obtener y almacenar Pokémon (opcional)
├─ requirements.txt           # ← Dependencias: flask, requests, supabase, python-dotenv
├─ .env                       # ← Credenciales de Supabase
├─ templates/
│   └─ pokemon.html           # ← Plantilla HTML que muestra los Pokémon almacenados
├─ static/
│   └─ css/
│       └─ style.css          # ← Hoja de estilos proporcionada por el usuario
└─ backend/
   └─ services/
      ├─ pokemon_service.py   # ← Servicio para interactuar con la PokeAPI
      └─ __init__.py
```

## Notas

- La aplicación **no** se conecta a la PokeAPI en tiempo de ejecución (excepto posiblemente al usar `buscar_carta.py`). Solo muestra los datos ya almacenados en Supabase.
- Si algún registro tiene `api_response` nulo o incompleto, la aplicación mostrará valores predeterminados (0 o listas vacías) para evitar errores.
- El CSS proporcionado por el usuario ya está integrado y da una apariencia moderna y responsiva.

¡Disfruta explorando tu Pokédex personal! 🚀