from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Привет с FastAPI и Vercel!"}

@app.get("/hello/{name}")
def say_hello(name: str):
    return {"message": f"Привет, {name}!"}

@app.get("/about")
def about():
    return {"info": "Это тестовое API, развернутое на Vercel."}
