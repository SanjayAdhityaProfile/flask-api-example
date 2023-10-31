from flask import Blueprint, request
from app.services.board_services import get_boards, create_board, get_boards_by_id, edit_board_by_id, de_activate
from app.services.authorization import verify_token
from app.services.ticket_services import get_ticket_by_board_id

dicom_board = Blueprint("dicom_board", __name__)

@dicom_board.route("/board_for_a_team/<team_id>", methods=["GET"])
@verify_token
def get_all_board(team_id):

    # TODO logic
    data = get_boards(team_id=team_id)
    print(data)
    data = [
        {
            "name": d.name,
            "id": d.id_id
        } for d in data
    ]

    return {"data": data}, 200

@dicom_board.route("/board", methods=["POST"])
@verify_token
def create_boards():

    # TODO logic
    board_data = request.json
    resp = create_board(
        board_data['id'], board_data['name'],
        board_data['description'], board_data['team_id']
    )
    if resp == True:
        return {}, 201
    return {}, 400

@dicom_board.route("/board/<id>", methods=["GET"])
@verify_token
def get_single_board(id):

    # NOTE - Board name, detail, period, point-goal, point-burned-out
    board_data = get_boards_by_id(id)

    # NOTE - Members
    if board_data:
        followers = board_data[0].get_following_members()
        ticket_data = get_ticket_by_board_id(id)
        ticket_data = [
            {
                "body": d.body,
                "id": d.id_id,
                "board_id": d.board_id,
                "status": d.status,
                "points": d.points,
                "member_": [{"id": m.id_id, "name": m.name} for m in d.get_following_members()]
            } for d in ticket_data
        ]
        # member_data = get_member_by_board_id(id)
        followers = [
            {
                "name": d.name,
                "id": d.id_id,
                "role": d.role,
                "points": d.points
            } for d in followers
        ]
        board_data = [
            {
                "name": d.name,
                "id": d.id_id
            } for d in board_data
        ]
        return {
            "data": {
                "board_data": board_data,
                "member_data": followers,
                "ticket_data": ticket_data
            }
        }, 200
    return {}, 400

@dicom_board.route("/board/<id>", methods=["PUT"])
@verify_token
def edit_board(id):
    board_data = request.json
    board = edit_board_by_id(id, board_data)
    if board is not None:
        return {
            "id": board.id_id,
            "name": board.name
        }, 200
    return {}, 400

@dicom_board.route("/board/deactivate/<id>", methods=["PUT"])
@verify_token
def de_activate_board(id):
    board = de_activate(id)
    if board:
        return {
            "id": board.id_id,
            "name": board.name,
            "is_active": board.is_active
        }, 200
    return {}, 400
