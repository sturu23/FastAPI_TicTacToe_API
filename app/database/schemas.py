from pydantic import BaseModel


class GameSymbols(BaseModel):
    type: str
    position: int


    class Config:
        orm_mode = True
