from dataclasses import dataclass
from datetime import date


@dataclass
class Lesson:
    title: str
    is_online: bool
    place: str
    teacher: str
    groups: list[str]

    start: str
    end: str


@dataclass
class ScheduleForTheDay:
    date: date
    lessons: list[Lesson]
