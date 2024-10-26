sessions_db = (
    'CREATE TABLE IF NOT EXISTS sessions ('
    'ID INTEGER PRIMARY KEY AUTOINCREMENT, '
    'spot_id INTEGER NOT NULL, '
    'start INTEGER NOT NULL, '
    'end INTEGER DEFAULT NULL, '
    'token TEXT NOT NULL,'
    'FOREIGN KEY(spot_id) REFERENCES spots(ID))'
)

spots_db = (
    'CREATE TABLE IF NOT EXISTS spots ('
    'ID INTEGER PRIMARY KEY AUTOINCREMENT, '
    'floor INTEGER NOT NULL, '
    'building INTEGER DEFAULT NULL, '
    'spot_number INTEGER NOT NULL, '
    'is_available INTEGER DEFAULT 1)'
)






show_available_spots = 'SELECT * FROM spots WHERE is_available = 1'

