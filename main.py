from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from fastapi import status
from typing import List
import models

# Создаем экземпляр приложения
app = FastAPI(title="Контрольная работа №1", 
              description="Технологии разработки серверных приложений",
              version="1.0.0")

# Задание 1.1 - Корневой маршрут
@app.get("/")
async def root():
    """
    Возвращает приветственное сообщение
    """
    return {"message": "Добро пожаловать в моё приложение FastAPI!"}

# Задание 1.2 - Возврат HTML страницы
@app.get("/html")
async def get_html():
    """
    Возвращает HTML страницу
    """
    return FileResponse("index.html", media_type="text/html")

# Задание 1.3 - POST запрос для сложения чисел
@app.post("/calculate")
async def calculate(num1: float, num2: float):
    """
    Принимает два числа и возвращает их сумму
    """
    result = num1 + num2
    return {"num1": num1, "num2": num2, "sum": result}

# Задание 1.4 - GET запрос для пользователя
# Создаем экземпляр пользователя
user_instance = models.User(name="Иван Петров", id=1)

@app.get("/users")
async def get_user():
    """
    Возвращает данные пользователя
    """
    return user_instance

# Задание 1.5 - POST запрос с проверкой на взрослого
@app.post("/user")
async def check_user_adult(user: models.UserAge):
    """
    Принимает пользователя и определяет, взрослый ли он
    """
    is_adult = user.age >= 18
    return {
        "name": user.name,
        "age": user.age,
        "is_adult": is_adult
    }

# Задание 2.1 - POST запрос для отзывов
@app.post("/feedback")
async def create_feedback(feedback: models.Feedback):
    """
    Сохраняет отзыв пользователя
    """
    # Преобразуем в валидированную модель для хранения
    feedback_validated = models.FeedbackValidated(
        name=feedback.name,
        message=feedback.message
    )
    
    # Сохраняем отзыв
    models.feedback_storage.append(feedback_validated)
    
    return {
        "message": f"Спасибо, {feedback.name}! Ваш отзыв сохранён.",
        "feedback_id": len(models.feedback_storage) - 1
    }

# Задание 2.2* - POST запрос с валидацией отзывов
@app.post("/feedback/v2", response_model=dict)
async def create_feedback_validated(feedback: models.FeedbackValidated):
    """
    Сохраняет отзыв с валидацией данных
    """
    # Сохраняем отзыв
    models.feedback_storage.append(feedback)
    
    return {
        "message": f"Спасибо, {feedback.name}! Ваш отзыв сохранён."
    }

# Дополнительный маршрут для просмотра всех отзывов (для проверки)
@app.get("/feedbacks", response_model=List[models.FeedbackValidated])
async def get_all_feedbacks():
    """
    Возвращает все сохраненные отзывы
    """
    return models.feedback_storage

# Маршрут для проверки работы с переменной приложения
# Запуск: uvicorn main:application --reload
application = app  # альтернативное имя для проверки задания 1.1

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)