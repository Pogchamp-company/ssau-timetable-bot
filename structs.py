from dataclasses import dataclass
from datetime import date
from typing import List


@dataclass
class Lesson:
    title: str
    is_online: bool
    place: str
    teacher: str
    groups: List[str]

    start: str
    end: str


@dataclass
class ScheduleForTheDay:
    date: date
    lessons: List[Lesson]
