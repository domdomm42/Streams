from src.data_store import data_store
from src.auth_auth_helpers import reset_session_tracker

def clear_v1():
    '''
    This function access all fields in the data structure from data_store
    and empties all of them to the original state at the beginning of the code.

    Arguements:
        N/A
    Exceptions:
        N/A
    Returns:
        Empty dictionary {} every time    
    '''

    reset_session_tracker()

    store = data_store.get()
    
    store['logged_in_users'] = []

    store['users']['user_id'] = []
    store['users']['emails'] = []
    store['users']['passwords'] = []
    store['users']['first_names'] = []
    store['users']['last_names'] = []
    store['users']['user_handles'] = []
    store['users']['is_global_owner'] = []
    store['users']['removed_user'] = []
    store['users']['permissions'] = []

    store['channels']['channel_id'] = []
    store['channels']['channel_name'] = []
    store['channels']['owner_user_id'] = []
    store['channels']['is_public'] = []
    store['channels']['all_members'] = []
    store['channels']['messages'] = []

    store['messages'] = []

    store['dms']['dm_id'] = []
    store['dms']['owner_user_id'] = []
    store['dms']['dm_name'] = []
    store['dms']['all_members'] = []
    store['dms']['messages'] = []
    #store['channels']['messages'] = []

    data_store.set(store)

    return 
