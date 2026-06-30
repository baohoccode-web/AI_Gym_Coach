import sqlite3
from pathlib import Path

#đường dẫn tới file database
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DB_PATH = DATA_DIR / "gym_coach.db"

#tạo kết nối tới SQLite database và nếu chưa có thì tự tạo
def get_db_connection():
    DATA_DIR.mkdir(exist_ok=True)

    connection = sqlite3.connect(DB_PATH)
    connection.execute("PRAGMA foreign_keys = ON")
    return connection

#tạo các bảng chính cho web
def create_tables():
    connection = get_db_connection()
    cursor = connection.cursor()

    #bảng user lưu thông tin người dùng
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            goal TEXT,
            training_level TEXT,
            body_weight REAL,
            training_frequency INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """

    )

    #bảng exercises lưu danh sách các bài tập
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS exercises (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            muscle_group TEXT,
            exercise_type TEXT,
            equipment TEXT,
            is_compound INTEGER DEFAULT 0
        )
        """
    )
    

    #bảng workout_sesions lưu từng buổi tập
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS workout_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            date TEXT NOT NULL,
            workout_type TEXT,
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
        """
    )

    #bảng set_logs lưu từng set trong buổi tập
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS set_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id INTEGER NOT NULL,
            exercise_id INTEGER NOT NULL,
            set_number INTEGER NOT NULL,
            weight REAL NOT NULL,
            reps INTEGER NOT NULL,
            rpe REAL,
            notes TEXT,
            
            FOREIGN KEY (session_id) REFERENCES workout_sessions(id),
            FOREIGN KEY (exercise_id) REFERENCES exercises(id)
            )
            """
    )
    connection.commit()
    connection.close()

#tạo user mặc định
def create_default_user():
    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO users (name, goal, training_level, body_weight, training_frequency)
        SELECT ?, ?, ?, ?, ?
        WHERE NOT EXISTS (
            SELECT 1 FROM users WHERE name = ?
        )
        """,
        (
            "Default User",
            "Hypertrophy",
            "Beginner",
            70.0,
            4,
            "Default User",
        ),
    )

    connection.commit()
    connection.close()

#hàm khởi tạo database trống, chạy hàm là khởi tạo bảng + user mặc định
def initialize_database():
    create_tables()
    create_default_user()

if __name__ == "__main__":
    initialize_database()
    print(f"Database initialized successfully at: {DB_PATH}")

    

