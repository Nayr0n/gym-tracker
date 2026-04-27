import sqlite3
import json
import os
from models import Workout, Exercise, Set

class Database:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.create_tables()
        self._seed_exercises()

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

    def _seed_exercises(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM exercises')
        if cursor.fetchone()[0] == 0:
            with open(os.path.join(os.path.dirname(__file__), 'assets', 'exercises.json'), 'r', encoding='utf-8') as f:
                exercises_data = json.load(f)
                for ex in exercises_data:
                    exercise = Exercise(name=ex['name'], description=ex['description'], img=ex['img'], muscle_group=ex['muscle_group'], sets=[])
                    self.add_exercise(exercise)

    def get_all_exercises(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM exercises')
        catalog = []
        for raw in cursor.fetchall():
            ex = Exercise(id=raw[0], name=raw[1], description=raw[2], img=raw[3], muscle_group=raw[4], sets=[])
            catalog.append(ex)
        return catalog

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
    
    def get_sets(self, workout_id, exercise_id):
        cursor = self.conn.cursor()
        cursor.execute('''SELECT * FROM sets WHERE workout_id = ? AND exercise_id = ?''', (workout_id, exercise_id))
        sets = []
        for raw in cursor.fetchall():
            set = Set(id=raw[0], workout_id=raw[1], exercise_id=raw[2], status=raw[3], reps=raw[4], weight=raw[5], rest_time=raw[6])
            sets.append(set)
        return sets

    def get_exercises(self, workout_id):
        cursor = self.conn.cursor()
        cursor.execute('''SELECT * FROM exercises WHERE id IN (SELECT exercise_id FROM sets WHERE workout_id = ?)''', (workout_id,))
        exercises = []
        for raw in cursor.fetchall():
            exercise = Exercise(id=raw[0], name=raw[1], description=raw[2], img=raw[3], muscle_group=raw[4], sets=[])
            exercise.sets = self.get_sets(workout_id, exercise.id)
            exercises.append(exercise)
        return exercises
    
    def get_workouts(self):
        cursor = self.conn.cursor()
        cursor.execute('''SELECT * FROM workouts''')
        workouts = []
        for raw in cursor.fetchall():
            workout = Workout(id=raw[0], name=raw[1], description=raw[2], img=raw[3], date=raw[4], exercises=[])
            workout.exercises = self.get_exercises(workout.id)
            workouts.append(workout)
        return workouts
    
        