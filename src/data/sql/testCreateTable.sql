-- SQLite

PRAGMA foreign_keys = ON;
--It seems this needs to be executed every time a session starts
--SQLITE does not enforce FK by default
--need to find appropriate place for this 

--need to understand more of daily operations to add CASCADE if needed.

CREATE TABLE IF NOT EXISTS event (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_name TEXT NOT NULL UNIQUE,
    location TEXT NOT NULL,
    start_date TEXT NOT NULL,
    end_date TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS race (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_id INTEGER NOT NULL,
    race_number INTEGER NOT NULL CHECK (race_number > 0),
    closed INTEGER DEFAULT 0 CHECK (closed IN (0, 1)), --Sqlite does not support boolean, we simulate it using int with a constraint

    FOREIGN KEY (event_id) REFERENCES event(id)
);

CREATE TABLE IF NOT EXISTS horse (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    race_id INTEGER NOT NULL,
    horse_number INTEGER NOT NULL CHECK (horse_number > 0),
    winner INTEGER DEFAULT 0 CHECK (winner IN (1, 0)), 
    scratched INTEGER DEFAULT 0 CHECK (scratched IN (1, 0)), 

    FOREIGN KEY (race_id) REFERENCES race(id)
);

CREATE TABLE IF NOT EXISTS ticket (
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    horse_id INTEGER NOT NULL,
    created_dttm TEXT DEFAULT (datetime('now', 'localtime')),

    
    status INTEGER NOT NULL DEFAULT 0 CHECK (status IN (0, 1, 2)),
    --0: "Issued/Valid"
    --1: "Redeemed"
    --2: "Refunded"


    FOREIGN KEY (horse_id) REFERENCES horse(id)
);
