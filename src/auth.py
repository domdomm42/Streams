from src.data_store import data_store
from src.error import InputError, AccessError
from src.auth_auth_helpers import hash, generate_jwt
import jwt
import smtplib
from src.other import *

from datetime import datetime, timezone

import string
import random
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
    # time_stamp = datetime.now().replace(tzinfo=timezone.utc).timestamp() # Augustus and Simon add this line

    datetime.now().replace(tzinfo=timezone.utc).timestamp()  # Augustus and Simon add this line

    #store['users']['channels_joined'].append(0)
    #store['users']['channels_joined'].append(0)
    #store['users']['dms_joined'].append(0)

    #store['users']['messages_sent'].append(0)
    
    
    if store['users']['user_id'] == []:  # First user to register
        store['users']['user_id'].append(0)
        store['users']['is_global_owner'].append(True)
        # dom's added line
        store['users']['permissions'].append(1)
        store['users']['removed_user'].append(False)

        # Augustus and Simon add these

        #store['users']['channels_joined'].append(0)

        #store['users']['dms_joined'].append(0)

        #store['users']['messages_sent'].append(0)

    else:
        store['users']['user_id'].append(store['users']['user_id'][-1] + 1)
        store['users']['is_global_owner'].append(False)
        # dom's added line
        store['users']['permissions'].append(2)
        store['users']['removed_user'].append(False)

    store['users']['emails'].append(email)
    store['users']['passwords'].append(hash(password))
    store['users']['first_names'].append(name_first)
    store['users']['last_names'].append(name_last)
    store['users']['password_reset_code'].append(0)  # dom added new line
    store['users']['notifications'].append([])

    user_id = store['users']['user_id'][-1]

    data_store.set(store)

    return {
        'token': generate_jwt(user_id),
        'auth_user_id': user_id
    }


def auth_logout_v1(token):
    '''
    This function takes in a token and if user is logged in, logout the user.

    Arguments:
        token(string) - Token of the user that gets logged out

    Exceptions:
        No given exceptions.

    Return Value:
        {}
    '''

    decoded_token = jwt.decode(token, SECRET, algorithms=['HS256'])
    user_id = decoded_token['user_id']
    session_id = decoded_token['session_id']

    store = data_store.get()

    if decoded_token == 'X':
        raise AccessError(description='User does not exist!')

    counter = 0
    for data in store['logged_in_users']:
        if data['user_id'] == user_id and data['session_id'] == session_id:
            store['logged_in_users'].remove({'user_id': user_id, 'session_id': session_id})
            counter = counter + 1

    if counter == 0:
        raise AccessError('Invalid token!')

    data_store.set(store)
    return ({})


def auth_passwordreset_request_v1(email):
    store = data_store.get()
    valid_email_check = 0
    counter = 0

    for stored_email in store['users']['emails']:
        if email != stored_email:
            counter += 1

        valid_email_check += 1
        break

    if counter == len(store['users']['emails']) and email != store['users']['emails'][counter - 1]:
        return 1

    if valid_email_check > 0:
        reset_code = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))

    store['users']['password_reset_code'][counter] = reset_code

    ################################################################################
    gmail_user = 'TeamBeagleSender@gmail.com'
    gmail_password = '@beaglesend1531'

    sent_from = gmail_user
    to = ['me@gmail.com', 'TeamBeagle1531@gmail.com']
    subject = 'Password Reset code'
    body = reset_code

    email_text = """\
    From: %s
    To: %s
    Subject: %s

    %s
    """ % (sent_from, ", ".join(to), subject, body)

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmail_user, gmail_password)
        server.sendmail(sent_from, to, email_text)
        server.close()

        print('The reset code has been sent to your email!')
    except:
        print('Something went wrong...')

    logged_in_users_list = store['logged_in_users'][:]

    for loggedin in logged_in_users_list:
        if loggedin['user_id'] == counter:
            store['logged_in_users'].remove({'user_id': counter, 'session_id': loggedin['session_id']})

    data_store.set(store)


def auth_passwordreset_reset_v1(reset_code, new_password):
    if reset_code == 0:
        raise InputError(description="Reset code is not a valid reset code!")

    store = data_store.get()
    counter = 0
    for codes in store['users']['password_reset_code']:
        if reset_code != codes:
            counter += 1
        break

    if counter == len(store['users']['password_reset_code']) and reset_code != store['users']['password_reset_code'][
        counter - 1]:
        raise InputError(description="Reset code is not a valid reset code!")

    # if counter == 0:
    #     raise InputError(description="Reset code is not a valid reset code!")

    if len(new_password) < 6:
        raise InputError(description="Password entered is less than 6 characters long!")

    store['users']['passwords'][counter] = hash(new_password)
    store['users']['password_reset_code'][counter] = 0

    data_store.set(store)


# --- Check email ---
# This function takes in an email (string) and checks if email is
# in the correct format and unique
# This function returns a unique user_handle
def check_email(email):
    '''
    This function checks whether an email(string) is valid and is in the correct
    format.

    Arguments:
        email (string)    - the user's email

    Exceptions:
        InputError  - Occurs when email is already registered

    Return Value:
        No return value, only raises error if email is registered.
    '''

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
    '''
    This function checks whether a password(string) is valid and is >= 6 in length

    Arguments:
        password (string)    - the user's password

    Exceptions:
        InputError  - Occurs when password is longer than 6 inclusive

    Return Value:
        No return value, only raises error if password is invalid.
    '''

    if len(password) < 6:
        raise InputError('Invalid password!')


# --- Check first name ---
# This function takes in the user's first name (string) and checks
# if the first name is between 1 and 50 characters inclusive
# This function does not return anything
def check_first_name(name_first):
    '''
    This function checks whether the first name is valid and is within 1-50 characters.

    Arguments:
        name_first (string)    - the user's first name

    Exceptions:
        InputError  - Occurs when length of first name is not between 1 and 50 characters inclusive

    Return Value:
        No return value, only raises error if first name is invalid.
    '''

    if len(name_first) < 1 or len(name_first) > 50:
        raise InputError('Invalid first name!')


# --- Check last name ---
# This function takes in the user's last name (string) and checks
# if the last name is between 1 and 50 characters inclusive
# This function does not return anything
def check_last_name(name_last):
    '''
    This function checks whether the last name is valid and is within 1-50 characters.

    Arguments:
        name_last (string)    - the user's last name

    Exceptions:
        InputError  - Occurs when length of last name is not between 1 and 50 characters inclusive

    Return Value:
        No return value, only raises error if last name is invalid.
    '''

    if len(name_last) < 1 or len(name_last) > 50:
        raise InputError('Invalid last name!')


# --- Create user_handle ---
# This function takes in the user's first and last name (strings)
# and creates a unique user_handle (string)
# This function does not return anything
def create_user_handle(name_first, name_last):
    '''
    This function creates a unique user_handle given first and last name

    Arguments:
        name_first (string)    - the user's first name
        name_last (string)     - the user's last name

    Exceptions:
        No exceptions
    Return Value:
        No return value, just appends to the dictionary in data_store.
    '''

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
    '''
    This function checks whether the email given is registered

    Arguments:
        email(string)   - the user's email

    Exceptions:
        InputError  - Email not registered
    Return Value:
        No return value, only raises error if email is not registered.
    '''

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
    '''
    This function checks whether the password matches the email given.

    Arguments:
        email(string)   - the user's email
        password(string) - password to test if match with email

    Exceptions:
        InputError  - Password is invalid(doesn't match).
    Return Value:
        No return value, only raises error password doesn't match email.
    '''

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


if __name__ == "__main__":
    auth_register_v1("TeamBeagle1531@gmail.com", "password", "Joe", "Tim")
    auth_login_v1("TeamBeagle1531@gmail.com", "password")
    auth_passwordreset_request_v1("TeamBeagle1531@gmail.com")

    store = data_store.get()
    code = store['users']['password_reset_code'][0]

    auth_passwordreset_reset_v1(code, "dompassword")
    auth_login_v1("TeamBeagle1531@gmail.com", "dompassword")
    print_store_debug()
