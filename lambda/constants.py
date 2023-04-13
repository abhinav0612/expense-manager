from enum import Enum, auto

class Action(Enum):
    EXPENSE = auto()
    SUMMARY = auto()
    TRENDS = auto()
    ANALYSIS = auto()

class ExpenseAction(Enum):
    ADD = auto()
    UPDATE = auto()
    DELETE = auto()

DATE_TIME_FORMATTER = '%d-%m-%Y'

BASE_URL = 'http://localhost:8000/api'
