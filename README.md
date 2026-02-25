Slice 0: The Skeleton
Goal: Initialize environment, set up database schema, establish database connection, and create basic Flask app structure.

Slice 1: The Dashboard
Goal: Implement the main dashboard view displaying all Todo Lists with summary statistics (e.g., "3/5 items completed") using complex SQL LEFT JOIN queries.

Slice 2: The Single List
Goal: Implement individual list views. Clicking a list title on the dashboard navigates to a dynamic route (e.g., /lists/1) displaying all Todos for that specific list.

Slice 3: The Creator
Goal: Implement POST routes and HTML forms to allow users to create new Todo Lists and add new Todos to existing lists.

Slice 4: The Editor
Goal: Implement functionality to mark Todos as completed/uncompleted and edit the titles of Lists and Todos using UPDATE SQL operations.

Slice 5: The Destroyer
Goal: Implement DELETE operations to remove Lists and Todos permanently from the database.

## Refactoring Roadmap: Developer Experience (DX)

The current codebase is functional but relies on repetitive patterns. The next phase of development focuses on improving maintainability, reducing boilerplate, and moving from procedural "plumbing" to declarative logic.

### 1. Automated Environment Setup
* Current State: The application requires manual execution of SQL scripts to initialize the database schema. Deployment or setup on new environments fails without manual intervention.
* Goal: Implement automatic schema verification on application startup. Ensure the application self-heals by creating missing tables dynamically. Provide CLI utilities to reset or seed the database state for testing purposes.

### 2. Database Abstraction Layer
* Current State: The persistence layer contains repetitive context manager code for connection handling and cursor management across every method.
* Goal: Encapsulate connection logic and cursor lifecycle management into a centralized internal interface. Reduce individual database methods to focus solely on SQL logic rather than plumbing. Eliminate redundant error handling blocks by managing them at the adapter level.

### 3. Declarative Resource Handling
* Current State: Route handlers (controllers) are responsible for repetitive tasks such as retrieving objects by ID and manually handling 404 errors.
* Goal: Implement a decorator-based pipeline to handle resource retrieval before the route handler executes. Centralize validation and error handling upstream. Inject retrieved resources directly into view functions to keep controller logic strictly focused on the response.

### 4. Custom Template Filters
* **The Requirement:** "Using template variables and custom template filters"
* **The Gap:** We built a Context Processor (`@app.context_processor`) to inject functions, but a Template Filter is different. It uses the pipe character (`|`) in Jinja2 (e.g., `{{ todo.title | capitalize }}`).
* **Action Item:** Learn how to build custom filters using the `@app.template_filter()` decorator in Flask to format data directly inside the HTML templates.

### 5. Seeding the Database
* **The Requirement:** "Provide the SQL needed to create and seed any databases you require."
* **The Gap:** The `init_db()` method wrote the SQL to *create* tables, but didn't *seed* them with initial data.
* **Action Item:** Create a `schema.sql` or `seed.sql` file filled with `INSERT INTO` statements. This ensures the database is automatically populated with dummy data (e.g., sample lists and todos) for immediate testing without manual data entry.

### 6. Serving Static Files
* **The Requirement:** "Serving static files in Flask (like CSS, JavaScript, and images)"
* **The Gap:** The project focused entirely on backend logic and HTML generation, without hooking up external stylesheets or images.
* **Action Item:** Understand how Flask serves files from a root `static/` directory and practice using `{{ url_for('static', filename='style.css') }}` inside the Jinja2 `<head>` tag.

### 7. Sessions and Persistence
* **The Requirement:** "Sessions and persistence"
* **The Gap:** The app successfully used Flask's `flash()` function (which relies on secure browser sessions under the hood), but didn't explicitly manipulate the `session` dictionary.
* **Action Item:** Import `session` from `flask` and practice manually storing state across the request/response cycle (e.g., `session['username'] = 'admin'`). This is foundational for maintaining state, such as keeping a user logged in.