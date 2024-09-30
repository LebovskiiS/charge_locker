users_db = ('CREATE TABLE IF NOT EXISTS users ('
                       'ID INTEGER PRIMARY KEY AUTOINCREMENT,'
                       ' token TEXT NOT NULL,'
                       ' session_id INTEGER NOT NULL,'
                       ' spot_id INTEGER NOT NULL,'
                       ' FOREIGN KEY (session_id) REFERENCES sessions(ID),'
                       ' FOREIGN KEY (spot_id) REFERENCES spots(ID))')

sessions_db = ('CREATE TABLE IF NOT EXISTS sessions ('
               'ID INTEGER PRIMARY KEY AUTOINCREMENT,'
               ' start INTEGER NOT NULL,'
               ' end INTEGER DEFAULT 0,'
               ' status BOOLEAN)')

spots_db = ('CREATE TABLE IF NOT EXISTS spots ('
            'ID INTEGER PRIMARY KEY AUTOINCREMENT,'
            ' floore INTEGER NOT NULL,'
            ' building INTEGER DEFAULT NULL,'
            ' spot_number INTEGER NOT NULL)')
