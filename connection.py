import sqlite3

db_path = 'my.db'

sql_statements = [ 
    """CREATE TABLE IF NOT EXISTS camera (
            camera_id INTEGER PRIMARY KEY, 
            plot_angle INT NOT NULL
        );""",

    """CREATE TABLE IF NOT EXISTS image (
            image_id INTEGER PRIMARY KEY, 
            datetime DATETIME NOT NULL,
            path TEXT NOT NULL,
            name TEXT NOT NULL,
            FOREIGN KEY (camera_id) REFERENCES camera (camera_id)
        );""",

    """CREATE TABLE IF NOT EXISTS analysis (
            analysis_id INT PRIMARY KEY,
            type TEXT NOT NULL,
            result REAL NOT NULL,
            FOREIGN KEY (image_id) REFERENCES image (image_id) ON DELETE CASCADE,
            UNIQUE (analysis_id, image_id)
        );""",

    """INSERT INTO camera (camera_id, plot_angle) VALUES (x, y)"""
]

# create a database connection
try:
    with sqlite3.connect(db_path) as conn:

        cursor = conn.cursor()

        for statement in sql_statements:
            cursor.execute(statement)

        conn.commit()

        print("Tables created successfully.")

except sqlite3.OperationalError as e:
    print("Failed to create tables:", e)
