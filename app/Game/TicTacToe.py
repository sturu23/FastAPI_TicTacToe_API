from fastapi import APIRouter, Depends, status, Response, HTTPException
from sqlalchemy import desc
from app.database.models import GameSymbols, Games
from app.database.schemas import GameSymbols as schemas_gamesymbols
from app.database.db import Session
from app.dependencies import get_db

router = APIRouter()


@router.post('/start', status_code=status.HTTP_201_CREATED)
def start_game(db: Session = Depends(get_db)):
    game = Games()  # with check variable i am creating game and returning json with game id
    db.add(game)
    db.commit()
    db.refresh(game)

    return {'game_id': check.id}


@router.post('/move/{game_id}', status_code=status.HTTP_201_CREATED)
def move(game_id: int, response: Response, request: schemas_gamesymbols, db: Session = Depends(get_db)):
    last = db.query(GameSymbols).filter(GameSymbols.game_id == game_id).order_by(
        desc(GameSymbols.id)).first()  # in last variable i'm getting last symbols by id

    game = db.query(Games).filter(
        Games.id == game_id).all()  # query game with argument(game_id) if it's correct id of it

    all_item = db.query(GameSymbols).filter(GameSymbols.game_id == game_id).all()

    if not game:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Game with the id {game_id} is not avaliable!')  # if it is not correct,return json with 404

    elif len(all_item) == 9:
        return {'Game': 'Finished'}

    elif last is None or request.type != last.symbol and request.position != last.position and request.position <= 8:  # checking if its validate
        create = GameSymbols(game_id=game_id, symbol=request.type, position=request.position)
        db.add(create)
        db.commit()
        db.refresh(create)
        response.status_code = status.HTTP_201_CREATED
        return {"result": "success"}  # if every condition is done , I am returning json with success

    return {"result": "error", "error_code": "invalid_position"}  # else i return json with error


@router.get('/check/{game_id}', status_code=status.HTTP_200_OK)
def check(game_id: int, db: Session = Depends(get_db)):
    games = db.query(GameSymbols).filter(GameSymbols.game_id == game_id).all()

    check_winner = [[0, 1, 2],
                    [3, 4, 5],
                    [6, 7, 8],
                    [0, 3, 6],
                    [1, 4, 7],
                    [2, 5, 9],
                    [0, 4, 8],
                    [2, 4, 6]]
    result = {
        'X': [],
        'O': []
    }
    if not games:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            # if id is incorrect, i raise httpexception with 404 and return json
                            detail=f'Game with the id {game_id} is not avaliable!')

    for game in games:
        if game.symbol == 'X':
            result['X'].append(game.position)  # append positions of X in dict to get which positions are used by X
        else:
            result['O'].append(game.position)  # same to O

    position_sum = len(result['X']) + len(result['O'])  # with len ,count positions for check if its draw
    x_winner = False
    o_winner = False
    draw = False

    for check in check_winner:
        if check == sorted(result['X']):  # i use for loop in check_winner to check if any version of winning is True.
            x_winner = True
            progress = {"game": "finished", "winner": 'X'}
        elif check == sorted(result['O']):
            o_winner = True
            progress = {'game': 'finished', "winner": 'O'}
        elif position_sum == 9:
            draw = True
            progress = {"game": "finished", "winner": "null"}
        elif not x_winner and not o_winner and not draw:
            progress = {"game": "in_progress"}

    return progress


@router.get('/history')
def history(db: Session = Depends(get_db)):
    game = db.query(GameSymbols).all()
    result = {}

    for info in game:
        each_game = db.query(GameSymbols).filter(GameSymbols.game_id == info.game_id).all()
        result[info.game_id] = {'type': [x.symbol for x in each_game], 'position': [x.position for x in each_game]}

    return result
