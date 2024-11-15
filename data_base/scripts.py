import psycopg2

sessions_db = """CREATE TABLE IF NOT EXISTS sessions
               (ID SERIAL PRIMARY KEY NOT NULL,
               uid INTEGER NOT NULL,
               token VARCHAR(255) NOT NULL,
               state VARCHAR(255) NOT NULL,
               spot_id INTEGER NOT NULL,
               "start" INTEGER NOT NULL,
               "end" INTEGER NOT NULL,             
               price INTEGER);"""


spots_db = (
    'CREATE TABLE IF NOT EXISTS spots ('
    'ID SERIAL PRIMARY KEY, '
    'floor INTEGER NOT NULL, '
    'building INTEGER DEFAULT NULL, '
    'spot_number INTEGER NOT NULL, '
    'is_available INTEGER DEFAULT 1)'
)

show_available_spots = 'SELECT * FROM spots WHERE is_available = 1'