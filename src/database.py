import sqlite3

class Database:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.create_tables()

    def create_tables(self):
        cursor = self.conn.cursor()

        cursor.execute('''CREATE TABLE IF NOT EXISTS sets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            workout_id INTEGER,
            exercise_id INTEGER,
            status TEXT,
            reps INTEGER,
            weight REAL,
            rest_time INTEGER,
            FOREIGN KEY(workout_id) REFERENCES workouts(id),
            FOREIGN KEY(exercise_id) REFERENCES exercises(id)
        )''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS exercises (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            description TEXT,
            img TEXT,
            muscle_group TEXT
        )''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS workouts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            description TEXT,
            img TEXT,
            date TEXT
        )''')

        self.conn.commit()

    def add_set(self, workout_id, exercise_id, set):
        cursor = self.conn.cursor()
        cursor.execute('''INSERT INTO sets (workout_id, exercise_id, status, reps, weight, rest_time) 
                          VALUES (?, ?, ?, ?, ?, ?)''', (workout_id, exercise_id, set.status, set.reps, set.weight, set.rest_time))
        return cursor.lastrowid
    
    def add_exercise(self, exercise):
        cursor = self.conn.cursor()
        cursor.execute('''INSERT INTO exercises (name, description, img, muscle_group) 
                          VALUES (?, ?, ?, ?)''', (exercise.name, exercise.description, exercise.img, exercise.muscle_group))
        self.conn.commit()
        return cursor.lastrowid
    
    def save_workout(self, workout):
        cursor = self.conn.cursor()
        cursor.execute('''INSERT INTO workouts (name, description, img, date) 
                          VALUES (?, ?, ?, ?)''', (workout.name, workout.description, workout.img, workout.date))
        
        workout_id = cursor.lastrowid
        for exercise in workout.exercises:
            exercise_id = exercise.id
            for set in exercise.sets:
                self.add_set(workout_id, exercise_id, set)
            
        self.conn.commit()
        return workout_id