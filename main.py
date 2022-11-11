from fastapi import FastAPI
from app.Game import TicTacToe

app = FastAPI()


app.include_router(TicTacToe.router)


