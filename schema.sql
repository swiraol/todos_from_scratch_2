DROP TABLE IF EXISTS todos, lists CASCADE;

CREATE TABLE IF NOT EXISTS lists (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS todos (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    completed BOOLEAN NOT NULL DEFAULT False,
    list_id INTEGER NOT NULL REFERENCES lists (id) ON DELETE CASCADE
);

INSERT INTO lists (title) VALUES ('Groceries');
INSERT INTO lists (title) VALUES ('Home');
INSERT INTO lists (title) VALUES ('Work');

INSERT INTO todos (title, list_id) VALUES ('Buy milk', 1);
INSERT INTO todos (title, list_id) VALUES ('Finish paper', 2);
INSERT INTO todos (title, completed, list_id) VALUES ('Grade homework', True, 3);