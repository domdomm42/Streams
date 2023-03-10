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

    store['users']['channels_joined'].append(0)

    time_stamp = int(datetime.now(timezone.utc).timestamp())

    # First user to be created i.e. a GLOBAL OWNER
    if store['users']['user_id'] == []: 
        store['users']['user_id'].append(0)
        store['users']['is_global_owner'].append(True)
        store['users']['permissions'].append(1)
        store['users']['removed_user'].append(False)

        # Workspace statistics
        channel_initial_workspacestat = {'num_channels_exist': 0, 'time_stamp': time_stamp}
        dm_initial_workspacestat = {'num_dms_exist': 0, 'time_stamp': time_stamp}
        msg_initial_workspacestate = {'num_messages_exist': 0, 'time_stamp': time_stamp}
        store['workspace_stat_channels'].append(channel_initial_workspacestat)
        store['workspace_stat_dms'].append(dm_initial_workspacestat)
        store['workspace_stat_messages'].append(msg_initial_workspacestate)
    
    else:
        store['users']['user_id'].append(store['users']['user_id'][-1] + 1)
        store['users']['is_global_owner'].append(False)
        store['users']['permissions'].append(2)
        store['users']['removed_user'].append(False)

    # Initialise values
    store['users']['emails'].append(email)
    store['users']['passwords'].append(hash(password))
    store['users']['first_names'].append(name_first)
    store['users']['last_names'].append(name_last)
    store['users']['password_reset_code'].append(0) 
    store['users']['notifications'].append([])
    store['users']['profile_img_url'].append('')
    store['users']['channels_joined'].append(0)
    store['users']['dms_joined'].append(0)
    store['users']['messages_sent'].append(0)

    # User statistics
    channel_initial_stat = {'num_channels_joined': 0, 'time_stamp': time_stamp}
    dm_initial_stat = {'num_dms_joined': 0, 'time_stamp': time_stamp}
    msg_initial_state = {'num_messages_sent': 0, 'time_stamp': time_stamp}
    store['users']['channels_user_data'].append([channel_initial_stat])
    store['users']['dms_user_data'].append([dm_initial_stat])
    store['users']['messages_sent_user_data'].append([msg_initial_state])
    store['users']['involvement_rate'].append(0)

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

    counter = 0
    for data in store['logged_in_users']:
        if data['user_id'] == user_id and data['session_id'] == session_id:
            store['logged_in_users'].remove({'user_id': user_id, 'session_id': session_id})
            counter = counter + 1

    if counter == 0:
        raise AccessError('Invalid token!')

    data_store.set(store)
    return {}


def auth_passwordreset_request_v1(email):
    '''
    This function sends a password reset code to the user's email.

    Arguments:
        email (string)    - The user's email.

    Return Value:
        Returns an empty dictionary.
    '''
    store = data_store.get()

    check_valid_email(email)
    idx = store['users']['emails'].index(email)

    # Create reset code
    reset_code = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))

    store['users']['password_reset_code'][idx] = reset_code
    
    gmail_user = 'TeamBeagleSender@gmail.com'
    gmail_password = '@beaglesend1531'

    sent_from = gmail_user
    to = ['me@gmail.com', email]
    subject = 'Password Reset code'
    body = reset_code

    # Create email body
    email_text = """\
    From: %s
    To: %s
    Subject: %s

    %s
    """ % (sent_from, ", ".join(to), subject, body)

    # Send an email
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.ehlo()
    server.login(gmail_user, gmail_password)
    server.sendmail(sent_from, to, email_text)
    server.close()

    print('The reset code has been sent to your email!')

    logged_in_users_list = store['logged_in_users'][:]

    for loggedin in logged_in_users_list:
        if loggedin['user_id'] == idx:
            store['logged_in_users'].remove({'user_id': idx, 'session_id': loggedin['session_id']})

    data_store.set(store)

def auth_passwordreset_reset_v1(reset_code, new_password):
    '''
    This function resets the password of a user with a valid email and reset code.

    Arguments:
        reset_code (string)    - the reset code sent to email

    Exceptions:
        InputError  - Invalid email or reset code.

    Return Value:
        Returns an empty dictionary.
    '''
    store = data_store.get()

    try:
        idx = store['users']['password_reset_code'].index(reset_code)
    except:
        raise InputError(description="Reset code is not a valid reset code!") from None
    
    if len(new_password) < 6:
        raise InputError(description="Password entered is less than 6 characters long!")

    store['users']['passwords'][idx] = hash(new_password)
    store['users']['password_reset_code'][idx] = 0

    data_store.set(store)

    return {}

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
