from app.models.models import Members
from app.api import db

def get_members(id):
    return Members.query.filter_by(team_id=id).all()

def create_member(
    name, role, points, team_id
):
    new_member = Members(
        name=name, role=role, points=points, team_id=team_id
    )
    db.session.add(new_member)
    db.session.commit()
    return True

def get_members_by_id(id):
    return Members.query.filter_by(id_id=id).all()

def get_member_by_board_id(id):
    return Members.query.filter_by(board_id=id).all()

def follow_a_board(board, member):
    return member.follow_board(board)

def un_follow_a_board(board, member):
    return member.un_follow_board(board)

def follow_a_ticket(ticket, member):
    return member.follow_ticket(ticket)

def un_follow_a_ticket(ticket, member):
    return member.un_follow_ticket(ticket)

def edit_member(id, data):
    member = get_members_by_id(id)
    if len(member) > 0:
        member[0].name = data['name'],
        member[0].role = data["role"],
        member[0].points = data["points"]
        db.session.commit()
        return member[0]
    return False
