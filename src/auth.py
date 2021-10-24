from src.data_store import data_store
from src.error import InputError, AccessError
from src.auth_auth_helpers import hash, generate_jwt
import jwt

import re

SECRET = 'BEAGLE'

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

    check_valid_email(email) 
    check_valid_password(email, hash(password))

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

    return {
        'token': generate_jwt(user_id),
        'auth_user_id': user_id,
    }


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
        #dom's added line
        store['users']['permissions'].append(1)
        store['users']['removed_user'].append(False)
    else:
        store['users']['user_id'].append(store['users']['user_id'][-1] + 1)
        store['users']['is_global_owner'].append(False)
        #dom's added line 
        store['users']['permissions'].append(2)
        store['users']['removed_user'].append(False)

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

    counter = 0
    for data in store['logged_in_users']:
        if data['user_id'] == user_id and data['session_id'] == session_id:
            store['logged_in_users'].remove({'user_id': user_id, 'session_id': session_id})
            counter = counter + 1

    if counter == 0:
        raise AccessError('Invalid token!')

    data_store.set(store)
    return ({})



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
        raise InputError(description = 'This email is already registered!')

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
        raise InputError('Invalid last name!')

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
    
    raise InputError('Email not registered!')

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

    raise InputError('Invalid Password!')

# if __name__ == '__main__':
#     token = auth_register_v1('joejim123@gmail.com', 'password', 'Jim', 's')['token']
#     auth_register_v1('joejim123234@gmail.com', 'password', 'SEW', 's')
    
#     print_store_debug()

#     auth_logout_v1(token)
#     print_store_debug()