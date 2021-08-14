from datetime import datetime
from typing import Optional, List

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Profile(BaseModel):
    first_name: str
    last_name: str
    age: Optional[int]
    children: List[str] = []
    city: Optional[str]
    resume: Optional[str]


@app.post("/")
def home(profile: Profile):
    data = profile.dict()
    data |= {'time': datetime.utcnow().isoformat()}
    return data
