from src.data_store import data_store
from src.error import InputError
from src.auth_auth_helpers import hash, generate_jwt

from src.server import *
import requests
import jwt

from src.config import *

import re

SECRET = 'BEAGLE'
BASE_URL = url

def auth_login_v1(email, password):
    ''' 
    The Function above takes in email and password and checks if the email is 
    registered, if email is registered, it will then check if password matches,
    if email and password is registered and correct, the user id will be returned

    Arguments:
        email - Integers      - Used to check whether the email given is registered
        password - Integers   - Used to check whether the password matches the email
    
    Exceptions:
        Input Error - Occurs when either the email is not registered or the password given 
                      does not match the email.
    
    Return Value:
        Returns 'auth_user_id': counter - When check_valid_email and check_valid_password == 1 and
                                          when the index of the list of password == index of list of email.

    '''

    store = data_store.get()
    email_list = []
    user_handles_list = []


    if check_valid_email(email) == 1 and check_valid_password(email, hash(password)) == 1:


        for data_email in store["users"]["emails"]:
            email_list.append(data_email)

        for data_user_handles in store["users"]["user_handles"]:
            user_handles_list.append(data_user_handles)

        counter = 0
        for list_emails in email_list:
            if list_emails == email:
                break
            else:
                counter = counter + 1

        user_id = store['users']['user_id'][counter]

        # session_id + 1 
        # store['logged_in_users'].append('user_id': user_id)
        # store['logged_in_users'].append('session_id': )

        return {
            'token': generate_jwt(user_id),
            'auth_user_id': user_id,
        }
    else:
        raise InputError('Wrong email and/or password!')


def auth_register_v1(email, password, name_first, name_last):
    '''
    This function registers a user with valid inputs and will store the user's data
    in data_store.

    Arguments:
        email (string)    - the user's email
        password (string)    - the user's password
        name_first (string)    - the user's first name
        name_last (string)   - the user's last name

    Exceptions:
        InputError  - Occurs when email is not a valid email
                      or the email address is already being used
                      or the length of password is less than 6 characters
                      or the length of first/last name is not 1-50 characters inclusive

    Return Value:
        {
            'token': str(user_id),
            'auth_user_id': user_id
        } (dictionary) - contains token (string) and auth_user_id (int)
    '''
    store = data_store.get()

    check_email(email)
    check_password(password)
    check_first_name(name_first)
    check_last_name(name_last)

    create_user_handle(name_first, name_last)

    if store['users']['user_id'] == []: # First user to register
        store['users']['user_id'].append(0)
        store['users']['is_global_owner'].append(True) 
        #Dom's added line
        store['users']['permissions'].append(1)
    else:
        store['users']['user_id'].append(store['users']['user_id'][-1] + 1)
        store['users']['is_global_owner'].append(False) 
        #Dom's added line
        store['users']['permissions'].append(2)

    store['users']['emails'].append(email)
    store['users']['passwords'].append(hash(password))
    store['users']['first_names'].append(name_first)
    store['users']['last_names'].append(name_last)

    user_id = store['users']['user_id'][-1]

    data_store.set(store)

    return {
        'token': generate_jwt(user_id),
        'auth_user_id': user_id
    }

def auth_logout_v1(token):
    decoded_token = jwt.decode(token, SECRET, algorithms=['HS256'])
    user_id = decoded_token['user_id']
    session_id = decoded_token['session_id']

    store = data_store.get()
    for data in store['logged_in_users']:
        if user_id == data['user_id'] and session_id == data['session_id']:
            store['logged_in_users'].remove({'user_id': user_id, 'session_id': session_id})

    data_store.set(store)

# --- Check email ---
# This function takes in an email (string) and checks if email is
# in the correct format and unique
# This function returns a unique user_handle
def check_email(email):

    store = data_store.get()

    regex = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$'

    if re.fullmatch(regex, email) and email not in store['users']['emails']:
        pass
    else:
        raise InputError(description='This email is already registered!')

# --- Check password ---
# This function takes in a password (string) and checks if the 
# password is >= 6 characters
# This function does not return anything
def check_password(password):
    if len(password) >= 6:
        pass
    else: 
        raise InputError('Invalid password!')

# --- Check first name ---
# This function takes in the user's first name (string) and checks 
# if the first name is between 1 and 50 characters inclusive
# This function does not return anything
def check_first_name(name_first):
    if len(name_first) >= 1 and len(name_first) <= 50:
        pass
    else: 
        raise InputError('Invalid first name!')

# --- Check last name ---
# This function takes in the user's last name (string) and checks 
# if the last name is between 1 and 50 characters inclusive
# This function does not return anything
def check_last_name(name_last):
    if len(name_last) >= 1 and len(name_last) <= 50:
        pass
    else:
        raise InputError(description='Invalid last name!')

# --- Create user_handle ---
# This function takes in the user's first and last name (strings)
# and creates a unique user_handle (string)
# This function does not return anything
def create_user_handle(name_first, name_last):

    user_handle = (name_first.lower() + name_last.lower())[0:20]

    # Obtain data
    store = data_store.get()
    
    # Check if the user_handle is unique,
    # If user_handle is not unique, then the function will add
    # a number at the end of the function
    user_handle_copy = user_handle
    i = 0
    while user_handle in store['users']['user_handles']:
        user_handle = user_handle_copy + str(i)
        i += 1
    
    store['users']['user_handles'].append(user_handle)

    data_store.set(store)

# --- Checks if email is registered ---
# This function takes in an email and checks if
# email used to log in is registed. If email
# is not stored, return error.
def check_valid_email(email):

    store = data_store.get()
    email_list = []


    for data_email in store["users"]["emails"]:
        email_list.append(data_email)

    for stored_email_list in email_list:
        if stored_email_list == email:
            
            return 1
    
    raise InputError(description='Email not registered!')

# --- Checks if password matches registered email ---
# This function takes in password and check if 
# password matches the registered email, if it doesn't, return
# Error.
def check_valid_password(email, password):
    email_list = []
    password_list = []
    

    store = data_store.get()
    for data_email in store["users"]["emails"]:
        email_list.append(data_email)

    for data_password in store["users"]["passwords"]:
        password_list.append(data_password)

    counter = 0

    for idx in email_list:
        if idx == email:
            if password == password_list[counter]:
                return 1
        else:
            counter = counter + 1

    raise InputError(description='Invalid Password!')

if __name__ == '__main__':
#     data = first = auth_register_v1('joejim123@gmail.com', 'passwordJ', '123456789', '1234567890')
#     second = auth_register_v1('joejim1234@gmail.com', 'password', '1234567890', 'a1234567890')

#     store = data_store.get()
#     print(store)
#     auth_logout_v1(data['token'])
    
#     print(store)
###############################################
    # store = data_store.get()
    # print(store['logged_in_users'])
    # requests.delete(f'{BASE_URL}/clear/v1')
    
    # user_info_reg_1 = {"email": "marryjane@gmail.com", "password": "passwordM", "name_first": "Marry", "name_last": "Jane"}
    # user_info_reg_2 = {"email": "marryjoe@gmail.com", "password": "password", "name_first": "Marry", "name_last": "Joe"}
    
    # response_data_1 = requests.post(f'{BASE_URL}/auth/register/v2', json = user_info_reg_1)
    # response_data_2 = requests.post(f'{BASE_URL}/auth/register/v2', json = user_info_reg_2)
    # print(store)

    # user_info_logout_1 = response_data_1.json()
    # # user_info_logout_1 = user_info_logout_1['token']

    # user_info_logout_2 = response_data_2.json()
    # # user_info_logout_2 = user_info_logout_2['token']

    # requests.post(f'{BASE_URL}/auth/logout/v1', json = user_info_logout_2['token'])

    # print(store['logged_in_users'])