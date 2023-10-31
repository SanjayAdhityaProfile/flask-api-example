from app.services.authorization import verify_token, produce_token
from flask import Blueprint, request, session, make_response
from app.services.team_services import check_name_in_db, create_Team, check_password_match
dicom_teams = Blueprint("dicom_teams", __name__)


@dicom_teams.route('/team/signup', methods=['POST'])
def signup_team():
    team_data = request.json
    name = team_data['name']
    email = team_data['email']

    # TODO check if already exists.
    if check_name_in_db('name', name):
        return {"err": "name already exists"}, 400
    if check_name_in_db('email', email):
        return {"err": "email already exists"}, 400

    # create a New Team Object and commit it
    password = team_data['password']
    about = team_data['about']

    resp = create_Team(name, password, email, about)

    # creating jwt with 15 mins of expiry to set on cookie of the user
    if resp:
        token = produce_token(resp.name, resp.id_id)
        session['name'] = name
        session['logged-in'] = True
        response = make_response({
            "mdg": "success",
            "auth_token": str(token)
        })
        response.set_cookie('auth_token', token)
        return response, 201
    return 400


@dicom_teams.route('/team/signin', methods=['POST'])
def signin_team():
    team_data = request.json
    name = team_data['name']
    team = check_name_in_db('name', name)
    # TODO check if already exists.
    if team:
        password = team_data['password']
        if check_password_match(password, team):
            # TODO - log in logic
            token = produce_token(team.name, team.id_id)
            response = make_response({
                "msg": "success",
                "auth_token": str(token)
            })
            # Set secure and samesite options for the cookie
            print(token)
            response.set_cookie('auth_token', token)
            return response, 200
        return {"err": "password mismatch"}, 400
    return {}, 400


@dicom_teams.route('/team/logout', methods=['POST'])
@verify_token
def logout():
    if session['logged-in'] == True:
        data = {
            # "user": session['name'],
            "msg": "logged out",
            "auth_token":''
        }
        session['logged-in'] = False
        # session['name'] = False
        response = make_response(data)
        response.set_cookie('auth_token', '')
        return response, 200
    return {}, 400
