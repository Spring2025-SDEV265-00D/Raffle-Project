-- SQLite

CREATE TABLE IF NOT EXISTS EVENT
(
    event_id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_name TEXT NOT NULL UNIQUE,
    start_date DATE NOT NULL DEFAULT(DATE('now')),
    end_date DATE DEFAULT NULL
);

CREATE TABLE IF NOT EXISTS PARTICIPANT
(
    par_id INTEGER PRIMARY KEY AUTOINCREMENT,
    par_name TEXT NOT NULL UNIQUE CHECK (LENGTH(par_name) > 0),
    registerer TEXT NOT NULL CHECK (LENGTH(registerer) > 0),
    date_registered DATE DEFAULT (DATE('now'))

);

CREATE TABLE IF NOT EXISTS SUB_EVENT
(
    sub_id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_id INTEGER NOT NULL,
    num_of_participants INTEGER NOT NULL CHECK (num_of_participants > 1),
    winner_id INTEGER DEFAULT NULL,

    FOREIGN KEY (winner_id) REFERENCES PARTICIPANT(par_id),
    FOREIGN KEY (event_id) REFERENCES EVENT(event_id)
);

CREATE TABLE IF NOT EXISTS SUBEVENT_PARTICIPANT
(
    sub_id INTEGER NOT NULL,
    par_id INTEGER NOT NULL,
    race_entry_num INTEGER NOT NULL CHECK (race_entry_num > 0),
    par_status TEXT NOT NULL CHECK (par_status IN ('OK', 'Scratched')),

    PRIMARY KEY (sub_id, par_id),
    FOREIGN KEY (sub_id) REFERENCES SUB_EVENT(sub_id),
    FOREIGN KEY (par_id) REFERENCES PARTICIPANT(par_id)


);
--    UNIQUE (sub_id, race_entry_num) -- Ensures unique race numbers per race
--might need this depending how backend handles it


CREATE TABLE IF NOT EXISTS TICKET
(
    ticket_id INTEGER PRIMARY KEY AUTOINCREMENT,
    sub_id INTEGER NOT NULL,
    par_id INTEGER NOT NULL,
    ticket_status TEXT NOT NULL DEFAULT ('Active') CHECK (ticket_status IN ('Active', 'Refunded', 'Redeemed')),
    winning_ticket INTEGER NOT NULL DEFAULT (0) CHECK(winning_ticket IN (0, 1)),

    FOREIGN KEY (sub_id) REFERENCES SUB_EVENT(sub_id),
    FOREIGN KEY (par_id) REFERENCES PARTICIPANT(par_id)
);


