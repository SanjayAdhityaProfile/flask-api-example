from app.models.models import Board
from app.api import db

def get_boards(team_id):
    return Board.query.filter_by(team_id=team_id).all()

def create_board(board_id, name, description, team_id):
    new_board = Board(
        board_id=board_id,
        name=name,
        description=description,
        team_id=team_id
    )
    db.session.add(new_board)
    db.session.commit()
    return True

def get_boards_by_id(id):
    return Board.query.filter_by(id_id=id).all()

def edit_board_by_id(id, data):
    board = Board.query.filter_by(id_id=id).all()
    if len(board) > 0:
        board[0].name = data['name'],
        board[0].description = data["description"]
        db.session.commit()
        return board[0]
    return False

def de_activate(id):
    board = Board.query.filter_by(id_id=id).all()
    if len(board) > 0:
        board[0].is_active = 'un_activate'
        db.session.commit()
        return board[0]
    return False
