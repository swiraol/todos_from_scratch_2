### The "No-Guardrails" Build Plan

We are not going to build "Layer by Layer" (Database first, then Python, then HTML). We are going to build **Vertical Slices**. We build one complete feature from the database all the way to the browser before moving to the next.

Here is your roadmap:

#### Slice 0: The Skeleton 🦴

* **Goal:** A working Flask app that connects to a database and shows a blank screen without crashing.
* **Tasks:**
1. `poetry init` & install dependencies (`flask`, `psycopg2-binary`, `python-dotenv`).
2. `schema.sql` (Create the tables).
3. `database_persistence.py` (Just the connection logic).
4. `app.py` (Hello World route).



#### Slice 1: The Dashboard (Read) 📖

* **Goal:** View all lists on the homepage with those fancy "3/5" counts.
* **Key Move:** The `all_lists` method with the **Left Join** you just mastered.

#### Slice 2: The Action (Create & Update) ⚡

* **Goal:** Create new lists and check off items.
* **Key Move:** The `update_todo_status` method (handling that tricky Boolean logic).

#### Slice 3: The Danger Zone (Delete) 💣

* **Goal:** Delete a list safely.
* **Key Move:** The `delete_list` transaction (Children first, then Parent).

---

### Your First Move

Open your terminal.

1. Create a directory: `todos_rematch`
2. Initialize the project.
3. Create your `schema.sql` and run it against a new database named `todos_rematch`.

**Let me know when you have an empty database and a running Flask app, and we will attack Slice 1.**

