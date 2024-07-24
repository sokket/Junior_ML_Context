from pydantic import BaseModel


class WordDto(BaseModel):
    id: int
    word: str

    class Config:
        orm_mode = True
