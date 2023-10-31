import enum
from datetime import datetime

from sqlalchemy import VARCHAR, INTEGER, Enum
from app.api import db
from flask_login import UserMixin


class IsActiveEnum(enum.Enum):
    active = 1
    un_activate = 2 


member_board = db.Table(
    'member_board',
    db.Column('member_id', db.Integer, db.ForeignKey('member.id_id')),
    db.Column('board_id', db.Integer, db.ForeignKey('board.id_id'))
)

member_ticket = db.Table(
    'member_ticket',
    db.Column('member_id', db.Integer, db.ForeignKey('member.id_id')),
    db.Column('ticket_id', db.Integer, db.ForeignKey('ticket.id_id'))
)


class Board(db.Model):

    __tablename__ = 'board'
    id_id = db.Column(
        INTEGER, primary_key=True, index=True,
        nullable=False, autoincrement=True
    )
    board_id = db.Column(VARCHAR(length=36))
    name = db.Column(VARCHAR(length=36), nullable=False)
    description = db.Column(VARCHAR(length=250), nullable=False)
    is_active = db.Column(
        Enum(IsActiveEnum), default=IsActiveEnum.active, index=True, nullable=True)
    created_at = db.Column(
        db.DateTime, index=True,
        default=datetime.utcnow, nullable=True
    )
    deleted_at = db.Column(db.DateTime, nullable=True)
    team_id = db.Column(db.Integer, db.ForeignKey('team.id_id'))

    def get_following_members(self):
        return self.followers


class Ticket(db.Model):

    __tablename__ = 'ticket'
    id_id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    points = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Integer, nullable=False)
    board_id = db.Column(db.Integer, db.ForeignKey('board.id_id'))
    team_id = db.Column(db.Integer, db.ForeignKey('team.id_id'))

    def get_following_members(self):
        return self.followers


class Members(db.Model):

    __tablename__ = 'member'
    id_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(140))
    points = db.Column(db.Integer, nullable=False)
    role = db.Column(db.String(36), nullable=False)
    team_id = db.Column(db.Integer, db.ForeignKey('team.id_id'))

    following_board = db.relationship(
        'Board', secondary=member_board, backref='followers')
    following_tickets = db.relationship(
        'Ticket', secondary=member_ticket, backref='followers')

    # To follow someone.
    def follow_board(self, board):
        if self.is_following_board(board):
            return False
        self.following_board.append(board)
        db.session.commit()
        return True

    def follow_ticket(self, ticket):
        if self.is_following_ticket(ticket):
            return False
        self.following_tickets.append(ticket)
        db.session.commit()
        return True

    def un_follow_board(self, board):
        if not self.is_following_board(board):
            return False
        self.following_board.remove(board)
        db.session.commit()
        return True

    def un_follow_ticket(self, ticket):
        if not self.is_following_ticket(ticket):
            return False
        self.following_tickets.remove(ticket)
        db.session.commit()

    def is_following_ticket(self, ticket):
        if ticket in self.following_tickets:
            return True
        return False

    def is_following_board(self, board):
        if board in self.following_board:
            return True
        return False


class Team(db.Model, UserMixin):
    id_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False, unique=True)    
    password_hash = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(120), index=True, unique=True)
    about = db.Column(db.String(140))
    admin_name = db.Column(db.String(20))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Team {}>'.format(self.username)
