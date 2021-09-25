from src.data_store import data_store
from src.error import InputError

import re

def auth_login_v1(email, password):
    return {
        'auth_user_id': 1,
    }

def auth_register_v1(email, password, name_first, name_last):

    store = data_store.get()

    # Check all inputs and store in data_store
    check_email(email)
    store['emails'].append(email)

    check_password(password)
    store['passwords'].append(password)

    check_first_name(name_first)
    store['first_names'].append(name_first)

    check_last_name(name_last)
    store['last_names'].append(name_last)
    
    # Create user_handle and store in data_store, return auth_user_id
    # NOTE: auth_user_id is the index of the user in the lists
    auth_user_ID = create_user_handle(name_first, name_last)
    
    return auth_user_ID


def check_email(email):

    store = data_store.get()

    regex = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$'

    if re.fullmatch(regex, email) and email not in store['emails']:
        pass
    else:
        raise InputError('Invalid email!')

def check_password(password):
    if len(password) >= 6:
        pass
    else: 
        raise InputError('Invalid password!')

def check_first_name(name_first):
    if len(name_first) >= 1 and len(name_first) <= 50:
        pass
    else: 
        raise InputError('Invalid first name!')

def check_last_name(name_last):
    if len(name_last) >= 1 and len(name_last) <= 50:
        pass
    else:
        raise Exception('Invalid last name!')

def create_user_handle(name_first, name_last):

    user_handle = (name_first.lower() + name_last.lower())[0:19]

    # Obtain data
    store = data_store.get()
    
    # Check if the user_handle is unique,
    # If user_handle is not unique, then the function will add
    # a number at the end of the function
    user_handle_copy = user_handle

    i = 1
    while user_handle in store['user_handles']:
        user_handle = user_handle_copy + str(i)
        i += 1
    
    store['user_handles'].append(user_handle)
    auth_user_ID = store['user_handles'].index(user_handle)
    print(store)
    return auth_user_ID

# Debugging + Testing purposes
if __name__ == '__main__':

    
    auth_register_v1('joe123@gmail.com', 'password', 'Joe', 'Smith')
    auth_register_v1('joe1233@gmail.com', 'password', 'Joe', 'Smith')


    # Testing create_user_handle works correctly for people with the same name
    # create_user_handle('Joe', 'Jimsfkjhydsyfdysfdyhs')
    # create_user_handle('Joe', 'Jimsfkjhydsyfdysfdyhs')
    # create_user_handle('Joe', 'Jimsfkjhydsyfdysfdyhs')
    # create_user_handle('Joe', 'Jimsfkjhydsyfdysfdyhs')
    