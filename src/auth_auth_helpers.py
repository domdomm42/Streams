import hashlib
import jwt
from src.data_store import data_store
from src.error import AccessError
#from src.other import print_store_debug

SESSION_TRACKER = 0
SECRET = 'BEAGLE'

def reset_session_tracker():
    global SESSION_TRACKER
    SESSION_TRACKER = 0

def generate_new_session_id():
    global SESSION_TRACKER
    SESSION_TRACKER += 1
    return SESSION_TRACKER

def hash(input_string):
    return hashlib.sha256(input_string.encode()).hexdigest()

def generate_jwt(user_id):
    session_id = generate_new_session_id()

    store = data_store.get()
    store['logged_in_users'].append({'user_id': user_id, 'session_id': session_id})
    data_store.set(store)

    return jwt.encode({'user_id': user_id, 'session_id': session_id}, SECRET, algorithm='HS256')

# def decode_jwt(encoded_jwt):
#     return jwt.decode(encoded_jwt, SECRET, algorithm=['HS256'])

def check_and_get_user_id(token):
    decoded_token = jwt.decode(token, SECRET, algorithms=['HS256'])
    user_id = decoded_token['user_id']
    session_id = decoded_token['session_id']


    store = data_store.get()

    for token in store['logged_in_users']:
        if token['user_id'] == user_id and token['session_id'] == session_id:
            return user_id
    else:
        raise AccessError('Invalid token!')