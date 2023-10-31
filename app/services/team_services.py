from app.models.models import Team
from app.api import db, app
from flask_bcrypt import Bcrypt 
bc = Bcrypt(app)

def check_name_in_db(param_type,param):
    if param_type == 'name':
        return Team.query.filter_by(name=param).first()
    
    if param_type == 'email':
        return Team.query.filter_by(email=param).first()

def create_Team(name, password, email, about_me):
    password_hashed = bc.generate_password_hash(password=password)
    new_hash = bc.check_password_hash(password_hashed,password)
    print(new_hash)
    new_Team = Team(
        name=name,
        password_hash=password_hashed,
        email=email,
        about=about_me        
    )
    db.session.add(new_Team)
    db.session.commit()
    return new_Team

def check_password_match(password, team):
    return bc.check_password_hash(str(team.password_hash),password)
