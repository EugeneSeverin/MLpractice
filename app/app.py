from fastapi import FastAPI

app = FastAPI()


students_dict = {'Armen':"A good student"}

@app.get("/", tags=['Ping'])
async def read_root(a:str):
    return {f"Oh! {a}"}

@app.get("/students/{name}")
async def read_item(name: str):
    return {"Students": students_dict[name]}

@app.post("/new_student")
async def add_student(new_student: dict):
    students_dict.update(new_student)
    return students_dict
