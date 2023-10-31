from flask import Blueprint, request
from app.services.user_services import (
    get_members, create_member, follow_a_board, get_members_by_id,
    un_follow_a_board, un_follow_a_ticket, follow_a_ticket, edit_member
)
from app.services.board_services import get_boards_by_id
from app.services.ticket_services import get_ticket_by_id
from app.services.authorization import verify_token

dicom_user = Blueprint("dicom_user", __name__)

@dicom_user.route("/user_for_a_team/<team_id>", methods=["GET"])
@verify_token
def get_all_user(team_id):

    # TODO logic
    data = get_members(team_id)
    data = [
        {
            "name": d.name,
            "id": d.id_id,
            "role": d.role,
            "points": d.points,
            "team_id":d.team_id
        } for d in data
    ]
    return {"data": data}, 200

@dicom_user.route("/user", methods=["POST"])
@verify_token
def create_user():
    member_data = request.json

    # TODO logic
    create_member(
        member_data['name'], member_data['role'], member_data['points'],member_data['team_id']
    )

    return {}, 200

@dicom_user.route("/user/<id>", methods=["PATCH"])
@verify_token
def edit_user_with_id(id):

    # TODO logic
    data = request.json
    data = edit_member(id, data)
    if data:
        return {}, 200
    return {}, 400

@dicom_user.route("/user/<id>", methods=["GET"])
@verify_token
def get_user_with_id(id):

    # TODO logic
    member = get_members_by_id(int(id))
    member = [
        {
            "name": d.name,
            "id": d.id_id,
            "points": d.points,
            "role": d.role
        } for d in member
    ]
    return {"data": member}, 200

@dicom_user.route("/user/follow/<member_id>/board/<board_id>", methods=["PUT"])
@verify_token
def follow_board(member_id, board_id):

    board = get_boards_by_id(int(board_id))
    member = get_members_by_id(int(member_id))
    if board and member:
        resp = follow_a_board(board[0], member[0])
        if resp:
            return {}, 200
    return {}, 400

@dicom_user.route("/user/un_follow/<member_id>/board/<board_id>", methods=["PUT"])
@verify_token
def un_follow_board(member_id, board_id):

    board = get_boards_by_id(int(board_id))
    member = get_members_by_id(int(member_id))
    if board and member:
        resp = un_follow_a_board(board[0], member[0])
        if resp:
            return {}, 200
    return {}, 400

@dicom_user.route("/user/follow/<member_id>/ticket/<ticket_id>", methods=["PUT"])
@verify_token
def follow_ticket(member_id, ticket_id):

    board = get_ticket_by_id(int(ticket_id))
    member = get_members_by_id(int(member_id))
    if board and member:
        resp = follow_a_ticket(board[0], member[0])
        if resp:
            return {}, 200
    return {}, 400

@dicom_user.route("/user/un_follow/<member_id>/ticket/<ticket_id>", methods=["PUT"])
@verify_token
def un_follow_ticket(member_id, ticket_id):

    ticket = get_ticket_by_id(int(ticket_id))
    member = get_members_by_id(int(member_id))
    if ticket and member:
        resp = un_follow_a_ticket(ticket[0], member[0])
        if resp:
            return {}, 200
    return {}, 400
