from src.data_store import data_store
from src.error import InputError, AccessError
from src.auth_auth_helpers import check_and_get_user_id

def user_profile_sethandle_v1(token, handle_str):
    user_id = check_and_get_user_id(token)
    check_len(handle_str)
    check_alphanumeric(handle_str)
    check_duplicate(handle_str)
    store = data_store.get()
    store['users']['user_handles'][user_id] = handle_str
    data_store.set(store)
    return {

    }












def check_len(handle_str):
    if len(handle_str) not in range(3, 20):
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
    if handle_str not in store['users'][handle_str]:
        pass
    else:
        raise InputError(description='This name has been used!')
