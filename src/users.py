from src.data_store import data_store
from src.error import InputError, AccessError
from src.auth_auth_helpers import check_and_get_user_id
import re

def user_profile_sethandle_v1(token, handle_str):
    '''
    Update the authorised user's handle (i.e. display name)

    Arguments:
        token(string)   - use to identify users
        handle_str(string)  - the name user want to replace

    Exceptions:
        400 Error:
            InputError('Invalid input') - length of handle_str is not between 3 and 20 characters inclusive
                                        - handle_str contains characters that are not alphanumeric
                                        - the handle is already used by another user
    
    Return value:
        return {}
    '''
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
    return {}


def user_all_v1(token):
    check_and_get_user_id(token)

    store = data_store.get()

    users = []
    for user_id in store['users']['user_id']:
        if store['users']['removed_user'][user_id] == False:
            
            user_email = store['users']['emails'][user_id]
            user_name_first = store['users']['first_names'][user_id]
            user_name_last = store['users']['last_names'][user_id]
            user_handle_str = store['users']['user_handles'][user_id]
            users.append({'u_id': user_id, 'email': user_email, 
                            'name_first': user_name_first, 
                            'name_last': user_name_last, 
                            'handle_str': user_handle_str})

    data_store.set(store)

    return {'users': users}


# List of all valid users
def user_profile_v1(token, u_id):

    store = data_store.get()

    check_invalid_u_id(u_id)

    return {'user_id': store['users']['user_id'][u_id], 
            'emails': store['users']['emails'][u_id], 
            'first_names': store['users']['first_names'][u_id], 
            'last_names': store['users']['last_names'][u_id],
            'user_handles': store['users']['user_handles'][u_id]}


# Update name
def user_profile_setname_v1(token, name_first, name_last):
    
    user_id = check_and_get_user_id(token)

    check_name_first_len(name_first)
    check_name_last_len(name_last)

    store = data_store.get()

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

    store = data_store.get()

    idx = 0
    for _ in store['users']['emails']:
        if idx == user_id:
            store['users']['emails'][idx] = email
            
            break
        idx = idx + 1

    data_store.set(store)

    return {}

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

def check_invalid_u_id(u_id):
    store = data_store.get()
    if u_id not in store['users']['user_id']:
        raise InputError(description='This user does not exist!')











