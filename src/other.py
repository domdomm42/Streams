from src.data_store import data_store

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

    store = data_store.get()
    
    store['users']['emails'] = []
    store['users']['passwords'] = []
    store['users']['first_names'] = []
    store['users']['last_names'] = []
    store['users']['user_handles'] = []

    store['channels']['owner_user_id'] = []
    store['channels']['channel_name'] = []
    store['channels']['is_public'] = []
    store['channels']['all_members'] = []
    store['channels']['messages'] = []

    data_store.set(store)

    return {}
    
