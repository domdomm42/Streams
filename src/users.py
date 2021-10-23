from src.data_store import data_store
from src.error import InputError, AccessError
from src.auth_auth_helpers import check_and_get_user_id

import re


def user_profile_sethandle_v1(token, handle_str):
    user_id = check_and_get_user_id(token)
    check_len(handle_str)
    check_alphanumeric(handle_str)
    check_duplicate(handle_str)
    store = data_store.get()
    idx = 0
    for _ in store['users']['user_handles']:
        if idx == user_id:
            store['users']['user_handles'][idx] = handle_str
            
            break
        idx = idx + 1




    
    data_store.set(store)
    return {

    }




# Users functions


# List of all users
def user_all_v1(token):
    # user_id = check_and_get_user_id(token)

    store = data_store.get()

    user = []

    for x in store['users']:
        user.append({ 'user_id': store['users']['user_id'][x], 'emails': store['users']['emails'][x], 'first_names': store['users']['first_names'][x], 'last_names': store['users']['last_names'][x],
                     'user_handles': store['users']['user_handles'][x]})

    data_store.set(store)

    return {'users': user}


# List of all valid users
def user_profile_v1(token, u_id):
    
    # user_id = check_and_get_user_id(token)

    store = data_store.get()

    user = []

    for x in store['users']:

        if int(u_id) < len(store['users']['user_handles']):
            user.append({ 'user_id': store['users']['user_id'][x], 'emails': store['users']['emails'][x], 'first_names': store['users']['first_names'][x], 'last_names': store['users']['last_names'][x],
                     'user_handles': store['users']['user_handles'][x]})
        else: 
            raise InputError(description='Invalid User ID')
    data_store.set(store)

    return {'users': user}


# Update name
def user_profile_setname_v1(token, name_first, name_last):
    




    
    user_id = check_and_get_user_id(token)

    check_name_first_len(name_first)
    check_name_last_len(name_last)

    store = data_store.get()

    # new_name = {'first_names': name_first, 'last_names': name_last}

    # store['users']['user_id'].append(new_name)




    idx = 0
    for _ in store['users']:
        if idx == user_id:
            store['users']['first_names'][idx] = name_first
            store['users']['last_names'][idx] = name_last


            break
        idx = idx + 1





    data_store.set(store)

    return {}


# Update email
def user_profile_setemail_v1(token, email):
    user_id = check_and_get_user_id(token)

    check_invalid_emails(email)

    # check_duplicate_email(email)


    store = data_store.get()

    idx = 0
    for _ in store['users']['emails']:
        if idx == user_id:
            store['users']['emails'][idx] = email
            
            break
        idx = idx + 1




    # new_email = {'emails': email}

    # store['users']['user_id'].append(new_email)

    data_store.set(store)

    return {}


# # Update handle
# def user_profile_sethandle_v1(toke, handle_str):
#     user_id = check_and_get_user_id(token)

#     store = data_store.get()

#     new_handle = {'handle_str': user_handles}

#     store['users']['u_id'].update(new_handle)

#     data_store.set(store)

#     return {}








def check_len(handle_str):
    if len(handle_str)  in range(3, 20):
        pass
    else:
        raise InputError(description='Invalid User Name')
    
def check_alphanumeric(handle_str):
    if handle_str.isalnum() == True:
        pass
    else:
        raise InputError(description='Invalid User Name')

def check_duplicate(handle_str):
    store = data_store.get()
    for name in store['users']['user_handles']:
        if name == handle_str:
            raise InputError(description='This name has been used!')
    
    pass
    





def check_name_first_len(first_names):
    if len(first_names) in range(1, 50):
        pass
    else:
        raise InputError(description='Invalid User Name')


def check_name_last_len(first_names):
    if len(first_names) in range(1, 50):
        pass
    else:
        raise InputError(description='Invalid User Name')


def check_invalid_emails(email):

    store = data_store.get()

    regex = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$'

    if re.fullmatch(regex, email) and email not in store['users']['emails']:
        pass
    else:
        raise InputError(description = 'This email is already registered!')




# def check_duplicate_email(email):
#     store = data_store.get()
#     for name in store['users']['emails']:
#         if name == email:
#             raise InputError(description='This name has been used!')
    
#     pass















