from io import DEFAULT_BUFFER_SIZE
import sqlite3
from pathlib import Path
from typing import Any

#đường dẫn tới file database
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DB_PATH = DATA_DIR / "gym_coach.db"

#danh sách bài tập mẫu
DEFAULT_EXERCISES = [
    ("Bench Press", "Chest", "Barbell", "Push", 1),
    ("Incline Dumbbell Press", "Chest", "Push", "Dumbbell", 1),
    ("Overhead Press", "Shoulders", "Push", "Barbell", 1),
    ("Lateral Raise", "Shoulders", "Push", "Dumbbell", 0),
    ("Triceps Pushdown", "Triceps", "Push", "Cable", 0),

    ("Lat Pulldown", "Back", "Pull", "Machine", 1),
    ("Barbell Row", "Back", "Pull", "Barbell", 1),
    ("Seated Cable Row", "Back", "Pull", "Cable", 1),
    ("Biceps Curl", "Biceps", "Pull", "Dumbbell", 0),
    ("Face Pull", "Rear Delts", "Pull", "Cable", 0),

    ("Squat", "Legs", "Leg", "Barbell", 1),
    ("Deadlift", "Posterior Chain", "Pull", "Barbell", 1),
    ("Romanian Deadlift", "Hamstrings", "Leg", "Barbell", 1),
    ("Leg Press", "Legs", "Leg", "Machine", 1),
    ("Leg Curl", "Hamstrings", "Leg", "Machine", 0),
    ("Calf Raise", "Calves", "Leg", "Machine", 0),
]

#tạo kết nối tới SQLite database và nếu chưa có thì tự tạo
def get_db_connection():
    DATA_DIR.mkdir(exist_ok=True)

    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
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

#thêm danh sách bài tập mẫu vào bảng exercises
def seed_exercises():
    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.executemany(
        """
        INSERT OR IGNORE INTO exercises
        (name, muscle_group, exercise_type, equipment, is_compound)
        VALUES (?, ?, ?, ?, ?)
        """,
        DEFAULT_EXERCISES,
    )
    
    connection.commit()
    connection.close()

#hàm khởi tạo database trống, chạy hàm là khởi tạo bảng + user mặc định
def initialize_database():
    create_tables()
    create_default_user()
    seed_exercises()

if __name__ == "__main__":
    initialize_database()
    print(f"Database initialized successfully at: {DB_PATH}")

#hàm lấy user mặc định
def get_default_user_id():

    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT id FROM users WHERE name = ?
        """,
        ("Default User",),
    )
    
    user = cursor.fetchone()
    connection.close()
    if user is None:
        raise ValueError("Default user not found. Run initialize_database() first.")
    return user["id"]

#hàm lấy toàn bộ danh sách bài tập trong database
def get_all_exercises():
    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT id, name, muscle_group, exercise_type, equipment, is_compound
        FROM exercises
        ORDER BY name
        """
    )
    exercises = cursor.fetchall()
    connection.close()
    return [dict(exercise) for exercise in exercises]

#hàm thêm 1 buổi tập
def add_workout_session(user_id: int, date: str, workout_type: str, notes: str = None):

    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO workout_sessions (user_id, date, workout_type, notes)
        VALUES (?, ?, ?, ?)
        """,
        (user_id, date, workout_type, notes),
    )
    session_id = cursor.lastrowid
    connection.commit()
    connection.close()
    return session_id

#hàm thêm 1 set log
def add_set_log(session_id: int, exercise_id: int, set_number: int, weight: float, reps: int, rpe: float = None, notes: str = None):

    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO set_logs (session_id, exercise_id, set_number, weight, reps, rpe, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (session_id, exercise_id, set_number, weight, reps, rpe, notes),
    )
    set_log_id = cursor.lastrowid
    connection.commit()
    connection.close()
    return set_log_id

#hàm lấy lịch sử tập luyện
def get_workout_history():
    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            ws.id AS session_id,
            ws.date,
            ws.workout_type,
            e.name AS exercise_name,
            e.muscle_group,
            sl.set_number,
            sl.weight,
            sl.reps,
            sl.rpe,
            sl.notes
        FROM set_logs sl
        JOIN workout_sessions ws ON sl.session_id = ws.id
        JOIN exercises e ON sl.exercise_id = e.id
        ORDER BY ws.date DESC, ws.id DESC, sl.set_number ASC
        """
    )
    rows = cursor.fetchall()
    connection.close()
    return [dict(row) for row in rows]

