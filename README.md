# Pokémon Explorer

Una aplicación web para explorar y gestionar tu colección personal de Pokémon almacenada en Supabase.

## Características

- 🎴 Grid responsivo de tarjetas de Pokémon (6/5/4/3/2/1 columnas)
- 🔢 Contador de apariciones por Pokémon (esquina superior derecha de cada tarjeta)
- 🎲 Botón para buscar y almacenar 3 Pokémon aleatorios
- 📊 Total de Pokémon almacenados en el encabezado
- 🌓 Interruptor de tema claro/oscuro con persistencia
- 🔍 Tarjetas clickeables que llevan a una página de detalle
- 📱 Diseño completamente responsive

## Requisitos

- Python 3.x
- Paquetes listados en `requirements.txt`
- Una base de datos Supabase con una tabla `pokemon` que tenga:
  - `id` (integer, primary key)
  - `name` (text)
  - `image` (text)
  - `api_response` (jsonb) - contiene el JSON completo de la PokeAPI
  - `count` (integer) - contador de apariciones

## Configuración

1. Copia tus credenciales de Supabase a un archivo `.env` en la raíz del proyecto:
   ```
   SUPABASE_URL=tu_url_de_supabase
   SUPABASE_KEY=tu_anon_key_de_supabase
   ```

2. Asegúrate de que la tabla `pokemon` exista y tenga las columnas requeridas. Si no existe, ejecuta esta SQL en el editor SQL de tu proyecto Supabase:
   ```sql
   CREATE TABLE public.pokemon (
     id INTEGER PRIMARY KEY,
     name TEXT,
     image TEXT,
     api_response JSONB,
     count INTEGER DEFAULT 0
   );
   ```

3. Instala las dependencias:
   ```bash
   source venv/bin/activate && pip install -r requirements.txt
   ```

## Uso

```bash
source venv/bin/activate && python3 app.py
```

Luego abre tu navegador en `http://localhost:5000` (o `http://127.0.0.1:5000`).

## Estructura del proyecto

```
pokeapi/
├─ app.py                     # ← Aplicación Flask principal
├─ backend/
│   └─ services/
│      └─ pokemon_service.py   # ← Servicio para interactuar con la PokeAPI
├─ .env                       # ← Credenciales de Supabase
├─ requirements.txt           # ← Dependencias: flask, requests, supabase, python-dotenv
├─ static/
│   └─ css/
│      └─ style.css          # ← Hoja de estilos con tema claro/oscuro
├─ templates/
│   ├─ pokemon.html          # ← Plantilla principal con grid de Pokémon
│   └─ pokemon_detail.html   # ← Plantilla de detalle de Pokémon
└─ venv/                     # ← Entorno virtual de Python
```

## Funcionalidad

- La aplicación **no** se conecta a la PokeAPI en tiempo de ejecución (excepto al usar el botón "Buscar 3 al azar"). 
- Muestra los datos ya almacenados en Supabase.
- Cada tarjeta muestra el número de veces que ese Pokémon ha sido buscado/almacenado.
- Al hacer clic en una tarjeta, se abre la página de detalle con información completa del Pokémon.
- El botón "Buscar 3 al azar" obtiene 3 Pokémon aleatorios de la PokeAPI y los almacena/actualiza en Supabase, incrementando su contador.
- El interruptor de tema permite alternar entre modo claro y oscuro, guardando la preferencia en localStorage.

¡Disfruta explorando tu Pokédex personal! 🚀