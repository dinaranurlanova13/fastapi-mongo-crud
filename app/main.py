from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from pymongo import MongoClient
from bson.objectid import ObjectId
import os

# Подключение к MongoDB
MONGO_URL = os.getenv("MONGO_URL", "mongodb://admin:adminpass@mongo:27017/")
client = MongoClient(MONGO_URL)
db = client["mydb"]
users_collection = db["users"]

app = FastAPI(title="FastAPI + MongoDB Example")

# Модель пользователя (для создания)
class User(BaseModel):
    name: str
    email: str
    age: int

# Главная страница
@app.get("/")
def read_root():
    return {"message": "Добро пожаловать в FastAPI + MongoDB проект!"}

# О проекте
@app.get("/about")
def about():
    return {"project": "FastAPI + MongoDB CRUD", "author": "Dinara"}

# ✅ Получение всех пользователей
@app.get("/users")
def get_users():
    users = []
    for user in users_collection.find():
        user["_id"] = str(user["_id"])  # преобразуем ObjectId в строку
        users.append(user)
    return {"users": users}

# ✅ Добавление нового пользователя
@app.post("/create")
def create_user(user: User):
    if users_collection.find_one({"email": user.email}):
        raise HTTPException(status_code=400, detail="Пользователь с таким email уже существует")
    users_collection.insert_one(user.dict())
    return {"message": "Пользователь добавлен", "user": user.dict()}

# ✅ Удаление пользователя по email
@app.post("/delete")
def delete_user(email: str):
    result = users_collection.delete_one({"email": email})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return {"message": "Пользователь удалён", "email": email}
