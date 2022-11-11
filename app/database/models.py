from sqlalchemy import String, Integer, Boolean, Column, ForeignKey
from .db import Base


class Games(Base):
    __tablename__ = 'games'

    id = Column(Integer, primary_key=True, index=True)



class GameSymbols(Base):
    __tablename__ = 'game_symbols'

    id = Column(Integer, primary_key=True,index=True)
    game_id = Column(Integer, ForeignKey('games.id'))
    symbol = Column(String(1))
    position = Column(Integer)
