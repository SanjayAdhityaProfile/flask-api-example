from app.models.models import Ticket
from app.api import db

def get_ticket():
    return Ticket.query.all()

def create_ticket(
    body, status, board_id, points
):
    new_ticket = Ticket(
        body=body, points=points, board_id=board_id, status=status
    )
    db.session.add(new_ticket)
    db.session.commit()
    return True

def get_ticket_by_board_id(id):
    return Ticket.query.filter_by(board_id=id).all()

def get_ticket_by_id(id):
    return Ticket.query.filter_by(id_id=id).all()

def edit_ticket(id, data):
    ticket = get_ticket_by_id(id)
    if len(ticket) > 0:
        ticket[0].body = data['body'],
        ticket[0].status = data["status"],
        ticket[0].points = data["points"]
        db.session.commit()
        return ticket[0]
    return False
