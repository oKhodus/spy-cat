from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import requests

from database import engine
from models import Base, Cat, Mission, Target
from schemas import CatCreate, CatUpdate, CatOut, MissionCreate, MissionOut, TargetUpdate
from deps import get_db

app = FastAPI(title="Spy Cat Agency")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

def validate_breed(breed: str):
    res = requests.get("https://api.thecatapi.com/v1/breeds")
    breeds = [b["name"].lower() for b in res.json()]
    if breed.lower() not in breeds:
        raise HTTPException(status_code=400, detail="Invalid cat breed")

@app.post("/cats", response_model=CatOut)
def create_cat(cat: CatCreate, db: Session = Depends(get_db)):
    validate_breed(cat.breed)
    db_cat = Cat(**cat.dict())
    db.add(db_cat)
    db.commit()
    db.refresh(db_cat)
    return db_cat

@app.get("/cats", response_model=list[CatOut])
def list_cats(db: Session = Depends(get_db)):
    return db.query(Cat).all()

@app.get("/cats/{cat_id}", response_model=CatOut)
def get_cat(cat_id: int, db: Session = Depends(get_db)):
    cat = db.query(Cat).get(cat_id)
    if not cat:
        raise HTTPException(404)
    return cat

@app.patch("/cats/{cat_id}", response_model=CatOut)
def update_cat(cat_id: int, data: CatUpdate, db: Session = Depends(get_db)):
    cat = db.query(Cat).get(cat_id)
    if not cat:
        raise HTTPException(404)
    cat.salary = data.salary
    db.commit()
    db.refresh(cat)
    return cat

@app.delete("/cats/{cat_id}")
def delete_cat(cat_id: int, db: Session = Depends(get_db)):
    cat = db.query(Cat).get(cat_id)
    if not cat:
        raise HTTPException(404)
    db.delete(cat)
    db.commit()
    return {"ok": True}

@app.post("/missions", response_model=MissionOut)
def create_mission(data: MissionCreate, db: Session = Depends(get_db)):
    if not (1 <= len(data.targets) <= 3):
        raise HTTPException(400, "Targets must be 1–3")

    mission = Mission()
    db.add(mission)
    db.commit()
    db.refresh(mission)

    for t in data.targets:
        target = Target(mission_id=mission.id, **t.dict())
        db.add(target)

    db.commit()
    return {
        **mission.__dict__,
        "targets": db.query(Target).filter_by(mission_id=mission.id).all()
    }


@app.post("/missions/{mission_id}/assign/{cat_id}")
def assign_cat(mission_id: int, cat_id: int, db: Session = Depends(get_db)):
    mission = db.query(Mission).get(mission_id)
    cat = db.query(Cat).get(cat_id)

    if not mission or not cat:
        raise HTTPException(404)

    mission.cat_id = cat_id
    db.commit()
    return {"ok": True}


@app.patch("/targets/{target_id}")
def update_target(
    target_id: int,
    data: TargetUpdate,
    db: Session = Depends(get_db)
):
    target = db.query(Target).get(target_id)
    if not target:
        raise HTTPException(404)

    mission = db.query(Mission).get(target.mission_id)
    if target.completed or mission.completed:
        raise HTTPException(400, "Target is locked")

    if data.notes is not None:
        target.notes = data.notes

    if data.completed is not None:
        target.completed = data.completed

    if all(t.completed for t in db.query(Target).filter_by(mission_id=mission.id)):
        mission.completed = True

    db.commit()
    return {"ok": True}


@app.delete("/missions/{mission_id}")
def delete_mission(mission_id: int, db: Session = Depends(get_db)):
    mission = db.query(Mission).get(mission_id)
    if not mission:
        raise HTTPException(404)
    if mission.cat_id:
        raise HTTPException(400, "Mission assigned")

    db.query(Target).filter_by(mission_id=mission.id).delete()
    db.delete(mission)
    db.commit()
    return {"ok": True}


@app.get("/missions")
def list_missions(db: Session = Depends(get_db)):
    missions = db.query(Mission).all()
    result = []
    for m in missions:
        targets = db.query(Target).filter_by(mission_id=m.id).all()
        result.append({**m.__dict__, "targets": targets})
    return result

@app.get("/missions/{mission_id}")
def get_mission(mission_id: int, db: Session = Depends(get_db)):
    m = db.query(Mission).get(mission_id)
    if not m:
        raise HTTPException(404)
    targets = db.query(Target).filter_by(mission_id=m.id).all()
    return {**m.__dict__, "targets": targets}



# uvicorn main:app --reload
# http://127.0.0.1:8000/docs