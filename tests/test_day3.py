from core.database import (
    initialize_database,
    get_default_user_id,
    get_all_exercises,
    add_workout_session,
    add_set_log,
    get_workout_history,
)


initialize_database()

user_id = get_default_user_id()
print("Default user id:", user_id)

exercises = get_all_exercises()
print("\nExercises:")
for exercise in exercises[:5]:
    print(exercise)

bench_press = next(ex for ex in exercises if ex["name"] == "Bench Press")

session_id = add_workout_session(
    user_id=user_id,
    date="2026-07-01",
    workout_type="Push",
    notes="Test workout session",
)

add_set_log(
    session_id=session_id,
    exercise_id=bench_press["id"],
    set_number=1,
    weight=50,
    reps=8,
    rpe=8,
    notes="Test set 1",
)

add_set_log(
    session_id=session_id,
    exercise_id=bench_press["id"],
    set_number=2,
    weight=50,
    reps=8,
    rpe=9,
    notes="Test set 2",
)

history = get_workout_history()

print("\nWorkout history:")
for row in history:
    print(row)
    