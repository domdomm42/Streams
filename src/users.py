from src.data_store import data_store
from src.error import InputError, AccessError
from src.auth_auth_helpers import check_and_get_user_id

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
    





























