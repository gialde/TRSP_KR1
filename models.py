from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
import re

# Задание 1.4 - Модель User
class User(BaseModel):
    name: str
    id: int

# Задание 1.5 - Модель User с age
class UserAge(BaseModel):
    name: str
    age: int

# Задание 2.1 - Модель Feedback
class Feedback(BaseModel):
    name: str
    message: str

# Задание 2.2 - Модель Feedback с валидацией
class FeedbackValidated(BaseModel):
    name: str = Field(..., min_length=2, max_length=50, description="Имя от 2 до 50 символов")
    message: str = Field(..., min_length=10, max_length=500, description="Сообщение от 10 до 500 символов")
    
    # Список недопустимых слов
    forbidden_words = ["кринг", "рофл", "вайб"]
    
    @field_validator('message')
    def check_forbidden_words(cls, v):
        # Приводим к нижнему регистру для проверки
        v_lower = v.lower()
        # Проверяем каждое запрещенное слово
        for word in cls.forbidden_words:
            # Используем регулярное выражение для поиска слова независимо от падежа
            pattern = r'\b' + re.escape(word) + r'\b'
            if re.search(pattern, v_lower):
                raise ValueError('Использование недопустимых слов')
        return v

# Для хранения отзывов
feedback_storage: List[FeedbackValidated] = []