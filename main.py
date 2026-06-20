# from fastapi import FastAPI
# from pydantic import BaseModel
# from sqlmodel import SQLModel, Field

# class Register(SQLModel, table=True):
#     name: str = Field(index=True, primary_key=True)
#     age: int = Field()
#     city: str = Field()
#     contact = str = Field()

# # class Register(BaseModel):
# #     name: str
# #     age: int
# #     city: str
# #     contact: str
# #     course: str

# app = FastAPI()

# @app.post("/register")
# def register_user(register: Register):
#     register.name.title()
#     register.city.title()
#     register.contact.title()
#     register.course.title()
#     return register

from fastapi import FastAPI,Depends,HTTPException,status
from sqlmodel import SQLModel,Session,Field,select,create_engine
from typing  import Annotated
from pydantic import BaseModel, validator


class Student(SQLModel,table=True):
    name: str = Field(index=True, primary_key=True)
    age: int  = Field(index=True)
    contact:str | None = Field(default=None)
    city: str | None = Field(default="unknown")
    course: str = Field(index=True)



sqlite_filename = "students.db"
sqlite_db_url = f"sqlite:///{sqlite_filename}"

connect_arg =  {"check_same_thread": False}
engine =create_engine(sqlite_db_url, connect_args=connect_arg)

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]

def create_db():
     return SQLModel.metadata.create_all(engine)

app = FastAPI()

@app.on_event("startup")
def startup():         
    create_db()

@app.post("/register")
def create_student(student:Student,session:SessionDep):
    session.add(student)
    session.commit()
    session.refresh(student)
    return student

@app.get("/show")
def get_student(student_name:str,session:SessionDep):  
    student = session.exec(select(Student))
    session.commit()
    session.refresh(Student)
    return student