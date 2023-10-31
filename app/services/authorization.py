from flask import request, jsonify, session
import jwt  # , secrets, os, uuid
from datetime import datetime, timedelta
from functools import wraps
from app.api import app

def verify_token(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        token = request.headers.get('auth_token')
        print(token)
        if not token:
            session['logged-in'] = False
            return jsonify({'Alert!': 'Not Authorized!'}), 401
        try:
            data = jwt.decode(
                token, app.config['SECRET_KEY'], algorithms='HS256')
            session['logged-in'] = True
        except Exception as e:
            print(e)
            session['logged-in'] = False
            return jsonify({'Message': 'Invalid token'}), 403
        return func(*args, **kwargs)
    return decorated

def log_datetime(func):
    '''Log the date and time of a function'''
    def wrapper(*args, **kwargs):
        print(
            f'Function: {func.__name__}\nRun on: {datetime.today().strftime("%Y-%m-%d %H:%M:%S")}')
        print(f'{"-"*30}')
        return func(*args, **kwargs)
    return wrapper

@log_datetime
def produce_token(name, id):
    session['logged_in'] = True
    token = jwt.encode({
        'id_id': id,
        'expiration': str(datetime.utcnow() + timedelta(minutes=1))
    },
        app.config['SECRET_KEY'])
    return token
