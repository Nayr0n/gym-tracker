from dataclasses import dataclass
from typing import Optional

@dataclass
class Set:
    workout_id: int
    exercise_id: int
    status: str
    reps: int
    weight: float
    rest_time: int
    id: Optional[int] = None
    
@dataclass
class Exercise:
    name: str
    description: str
    img: str
    muscle_group: str
    sets: list[Set]
    id: Optional[int] = None

@dataclass
class Workout:
    name: str
    description: str
    img: str
    date: str
    exercises: list[Exercise]
    id: Optional[int] = None