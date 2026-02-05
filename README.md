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