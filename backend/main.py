from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from database import get_db
from models import Word
from schemas import WordDto
from crud import get_words

app = FastAPI()

@app.get("/api/words", response_model=List[WordDto])
async def read_words(db: AsyncSession = Depends(get_db)):
    words = await get_words(db)
    return words
