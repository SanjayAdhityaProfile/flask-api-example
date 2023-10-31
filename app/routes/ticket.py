from flask import Blueprint, request
from app.services.ticket_services import get_ticket, create_ticket, edit_ticket, get_ticket_by_id
from app.services.authorization import verify_token

dicom_ticket = Blueprint("dicom_ticket", __name__)

@dicom_ticket.route("/ticket", methods=["GET"])
@verify_token
def get_all_ticket():

    # TODO logic
    data = get_ticket()
    data = [
        {
            "body": d.body,
            "id": d.id_id,
            "board_id": d.board_id,
            "status": d.status,
            "points": d.points
        } for d in data
    ]
    return {"data": data}, 200

@dicom_ticket.route("/ticket", methods=["POST"])
@verify_token
def create_tickets():
    member_data = request.json

    # TODO logic
    create_ticket(
        body=member_data['body'], status=member_data['status'],
        board_id=member_data['board_id'], points=member_data['points']
    )

    return {}, 200

@dicom_ticket.route("/ticket/<id>", methods=["PUT"])
@verify_token
def edit_ticket_with_id(id):
    data = request.json

    # TODO logic
    data = edit_ticket(id, data)
    if data:
        return {}, 200
    return {}, 400

@dicom_ticket.route("/ticket/<id>", methods=["GET"])
@verify_token
def get_ticket_with_id(id):

    # TODO logic
    ticket = get_ticket_by_id(id)
    ticket = [
        {
            "body": d.body,
            "id": d.id_id,
            "points": d.points,
            "status": d.status
        } for d in ticket
    ]
    return {"data": ticket}, 200
