import sqlite3

db_path = 'turf_plot.db'

sql_table_statements = [ 
    """CREATE TABLE IF NOT EXISTS camera (
            camera_id INTEGER PRIMARY KEY, 
            plot_angle INT NOT NULL
        );""",

    """CREATE TABLE IF NOT EXISTS image (
            image_id INTEGER PRIMARY KEY, 
            datetime DATETIME NOT NULL,
            path TEXT NOT NULL,
            name TEXT NOT NULL,
            camera_id INT NOT NULL,
            FOREIGN KEY (camera_id) REFERENCES camera (camera_id)
        );""",

    """CREATE TABLE IF NOT EXISTS analysis (
            analysis_id INT PRIMARY KEY,
            type TEXT NOT NULL,
            result REAL NOT NULL,
            image_id INT NOT NULL,
            FOREIGN KEY (image_id) REFERENCES image (image_id) ON DELETE CASCADE,
            UNIQUE (analysis_id, image_id)
        );"""
]

sql_row_statements = [
    """INSERT OR IGNORE INTO camera (camera_id, plot_angle) VALUES (1, 10)""",
    """INSERT OR IGNORE INTO camera (camera_id, plot_angle) VALUES (2, 20)""",
    """INSERT OR IGNORE INTO camera (camera_id, plot_angle) VALUES (3, 30)""",
    """INSERT OR IGNORE INTO camera (camera_id, plot_angle) VALUES (4, 40)""",
    """INSERT OR IGNORE INTO camera (camera_id, plot_angle) VALUES (5, 50)""",
    """INSERT OR IGNORE INTO camera (camera_id, plot_angle) VALUES (6, 60)""",
    """INSERT OR IGNORE INTO camera (camera_id, plot_angle) VALUES (7, 70)"""
]

def initTables():
    try:
        with sqlite3.connect(db_path) as conn:

            cursor = conn.cursor()

            for statement in sql_table_statements:
                cursor.execute(statement)

            conn.commit()

            print("Tables created successfully.")

    except sqlite3.OperationalError as e:
        print("Failed to create tables: ", e)

def initRows():
    try:
        with sqlite3.connect(db_path) as conn:

            cursor = conn.cursor()

            for statement in sql_row_statements:
                cursor.execute(statement)

            conn.commit()

            print("Rows created successfully.")

    except sqlite3.OperationalError as e:
        print("Failed to create rows: ", e)

def insertPictureData(camera_id, datetime, path, name):
    try:
        with sqlite3.connect(db_path) as conn:

            conn.execute("PRAGMA foreign_keys = ON;")
            cursor = conn.cursor()

            cursor.execute(
                """
                INSERT INTO image (datetime, path, name, camera_id) VALUES (?, ?, ?, ?)
                """,
                (datetime, path, name, camera_id)
            )

            conn.commit()

            print("Image row inserted successfully.")

    except sqlite3.OperationalError as e:
        print("Failed to insert image row: ", e)

def insertAnalysisData(type, result, image_id):
    try:
        with sqlite3.connect(db_path) as conn:

            conn.execute("PRAGMA foreign_keys = ON;")
            cursor = conn.cursor()

            cursor.execute(
                """
                INSERT INTO analysis (type, result, image_id) VALUES (?, ?, ?)
                """,
                (type, result, image_id)
            )

            conn.commit()

            print("Analysis row inserted successfully.")

    except sqlite3.OperationalError as e:
        print("Failed to insert analysis row: ", e)

def countCameras():
    try:
        with sqlite3.connect(db_path) as conn:
        
            conn.execute("PRAGMA foreign_keys = ON;")
            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT camera_id FROM camera
                """
            )

            camera_ids = [row[0] for row in cursor.fetchall()]
            print("Select camera_id successful.")
            return camera_ids

    except sqlite3.OperationalError as e:
        print("Failed to select camera_id from camera table: ", e)

def footerDisplay():
    try:
        with sqlite3.connect(db_path) as conn:

            conn.execute("PRAGMA foreign_keys = ON;")
            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT COUNT(*) FROM camera
                """
            )
            camera_count = cursor.fetchone()[0]

            cursor.execute(
                """
                SELECT COUNT(*) FROM image
                """
            )
            image_count = cursor.fetchone()[0]

            count_list = {
                "camera_count": camera_count,
                "image_count": image_count
            }

            print("Select count successful.")
            return count_list
            
    except sqlite3.OperationalError as e:
        print("Failed to select count from camera table: ", e)

def folderList(camera_id):
    try:
        with sqlite3.connect(db_path) as conn:

            conn.execute("PRAGMA foreign_keys = ON;")
            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT image_id, name FROM image WHERE camera_id = ?
                """,
                (camera_id)
            )

            images = cursor.fetchall()

            print("Select image_id, name successful.")
            return images

    except sqlite3.OperationalError as e:
        print("Failed to select image_id, name from image table: ", e)