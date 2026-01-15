from pydantic import BaseModel
from typing import List

class CatCreate(BaseModel):
    name: str
    experience_years: int
    breed: str
    salary: float

class CatUpdate(BaseModel):
    salary: float

class CatOut(BaseModel):
    id: int
    name: str
    experience_years: int
    breed: str
    salary: float

    class Config:
        orm_mode = True

class TargetCreate(BaseModel):
    name: str
    country: str
    notes: str = ""

class TargetUpdate(BaseModel):
    notes: str | None = None
    completed: bool | None = None

class TargetOut(BaseModel):
    id: int
    name: str
    country: str
    notes: str
    completed: bool

    class Config:
        orm_mode = True

class MissionCreate(BaseModel):
    targets: List[TargetCreate]

class MissionOut(BaseModel):
    id: int
    cat_id: int | None
    completed: bool
    targets: List[TargetOut]

    class Config:
        orm_mode = True