import hashlib
import jwt
from src.data_store import data_store
from src.error import AccessError

SESSION_TRACKER = 0
SECRET = 'BEAGLE'

def reset_session_tracker():
    '''
    Resets the session tracker for tokens

    Return value:
        No return value
    '''
    global SESSION_TRACKER
    SESSION_TRACKER = 0

def generate_new_session_id():
    '''
    Generates a new session ID for a user which registers or logs in
    
    Return value:
        Returns a new session tracker
    '''
    global SESSION_TRACKER
    SESSION_TRACKER += 1
    return SESSION_TRACKER

def hash(input_string):
    '''
    Hashes a string using SHA256 algorithm

    Arguments:
        input_string    (string)    - The string which is to be hased.
    
    Return value:
        Returns a hashed string
    '''
    return hashlib.sha256(input_string.encode()).hexdigest()

def generate_jwt(user_id):
    '''
    Generates a JWT given a user_id

    Arguments:
        user_id    (integer)    - The user_id which a token will be generated for
    
    Return value:
        Returns a hashed string
    '''
    session_id = generate_new_session_id()

    store = data_store.get()
    store['logged_in_users'].append({'user_id': user_id, 'session_id': session_id})
    data_store.set(store)

    return jwt.encode({'user_id': user_id, 'session_id': session_id}, SECRET, algorithm='HS256')


def check_and_get_user_id(token):
    '''
    Checks a token and gets the user_id which the token belongs to

    Arguments:
        token    (string)    - JWT token

    Exceptions:
        AccessError     - If token is invalid
    
    Return value:
        Returns user_id of token given that no error occurs
    '''

    try:
        decoded_token = jwt.decode(token, SECRET, algorithms=['HS256'])
    except:
        raise AccessError('Invalid token')
    user_id = decoded_token['user_id']
    session_id = decoded_token['session_id']

    store = data_store.get()

    for token in store['logged_in_users']:
        if token['user_id'] == user_id and token['session_id'] == session_id:
            return user_id
    else:
        raise AccessError('Invalid token!')