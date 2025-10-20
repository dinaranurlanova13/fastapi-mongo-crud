from fastapi import FastAPI, Request, Form, status
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List
import uvicorn

app = FastAPI(title="FastAPI Demo App")
templates = Jinja2Templates(directory="app/templates")

# Поддерживаемые данные в памяти (для демонстрации)
class Item(BaseModel):
    id: int
    name: str
    description: str | None = ""

# начальные данные
items_db: List[Item] = [
    Item(id=1, name="Notebook", description="A simple notebook"),
    Item(id=2, name="Pen", description="Blue ink pen"),
]

# static (если понадобится)
# app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Главная страница — приветствие."""
    return templates.TemplateResponse("index.html", {"request": request, "title": "Главная"})

@app.get("/about", response_class=HTMLResponse)
async def about(request: Request):
    """Информация о проекте/разработчике."""
    return templates.TemplateResponse("about.html", {"request": request, "title": "О проекте"})

@app.get("/data", response_class=HTMLResponse)
async def data_page(request: Request):
    """Страница с таблицей данных из items_db."""
    return templates.TemplateResponse("data.html", {"request": request, "items": items_db, "title": "Данные"})

@app.get("/api/items", response_class=JSONResponse)
async def api_get_items():
    """API: возвращаем JSON всех элементов."""
    return JSONResponse(content=[item.dict() for item in items_db])

@app.get("/add", response_class=HTMLResponse)
async def add_form(request: Request):
    """Форма добавления нового элемента (GET)."""
    return templates.TemplateResponse("add.html", {"request": request, "title": "Добавить элемент"})

@app.post("/add")
async def add_item(name: str = Form(...), description: str = Form("")):
    """Обработка POST формы — добавление нового элемента."""
    new_id = (max([i.id for i in items_db]) + 1) if items_db else 1
    item = Item(id=new_id, name=name, description=description)
    items_db.append(item)
    # Перенаправление на страницу /data
    return RedirectResponse(url="/data", status_code=status.HTTP_303_SEE_OTHER)

# Дополнительный эндпоинт: удаление по id (для тестирования)
@app.post("/delete/{item_id}")
async def delete_item(item_id: int):
    global items_db
    items_db = [i for i in items_db if i.id != item_id]
    return JSONResponse(content={"status": "ok", "deleted_id": item_id})

# Запуск (локально, только если выполняется как скрипт)
if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
