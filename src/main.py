from models import Workout, Exercise, Set
from database import Database

def test_backend():
    print("🚀 Запуск тесту бази даних...\n")
    
    # 1. Підключаємось до бази (файл створиться автоматично у папці проєкту)
    db = Database('test_gym.db')

    # 2. НАПОВНЮЄМО ДОВІДНИК (імітуємо базові налаштування)
    bench_press = Exercise(name="Жим лежачи", description="База", img="", muscle_group="Груди", sets=[])
    squat = Exercise(name="Присідання", description="База", img="", muscle_group="Ноги", sets=[])

    bench_id = db.add_exercise(bench_press)
    squat_id = db.add_exercise(squat)
    print(f"✅ Довідник створено. Жим ID: {bench_id}, Присід ID: {squat_id}")

    # 3. ІМІТУЄМО ТРЕНУВАННЯ
    # Зробили 2 підходи жиму
    set1 = Set(workout_id=0, exercise_id=bench_id, status="done", reps=10, weight=60.0, rest_time=90)
    set2 = Set(workout_id=0, exercise_id=bench_id, status="done", reps=8, weight=65.0, rest_time=90)
    
    # Зробили 1 підхід присіду
    set3 = Set(workout_id=0, exercise_id=squat_id, status="done", reps=12, weight=80.0, rest_time=120)

    # Пакуємо підходи у вправи (саме так це робитиме Flet у майбутньому)
    bench_for_workout = Exercise(id=bench_id, name="Жим", description="", img="", muscle_group="Груди", sets=[set1, set2])
    squat_for_workout = Exercise(id=squat_id, name="Присід", description="", img="", muscle_group="Ноги", sets=[set3])

    # Пакуємо все у тренування
    my_workout = Workout(
        name="Важке тренування", 
        description="Груди + Ноги", 
        img="", 
        date="2023-11-01", 
        exercises=[bench_for_workout, squat_for_workout]
    )

    # 4. ЗБЕРІГАЄМО ТРЕНУВАННЯ В БАЗУ
    workout_id = db.save_workout(my_workout)
    print(f"✅ Тренування успішно збережено з ID: {workout_id}\n")

    # 5. ТЕСТУЄМО ЧИТАННЯ (Перевіряємо, чи працює get_workouts)
    print("🔍 Читаємо історію з бази даних...\n")
    history = db.get_workouts()

    # Красиво виводимо результат у консоль
    for w in history:
        print(f"📅 ТРЕНУВАННЯ: {w.name} ({w.date})")
        for ex in w.exercises:
            print(f"  💪 ВПРАВА: {ex.name} [{ex.muscle_group}]")
            for s in ex.sets:
                print(f"      - Підхід: {s.weight} кг х {s.reps} разів (Відпочинок: {s.rest_time}с)")

if __name__ == "__main__":
    test_backend()