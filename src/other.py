from src.data_store import data_store

def clear_v1():

    store = data_store.get()
    
    store['users']['emails'] = []
    store['users']['passwords'] = []
    store['users']['first_names'] = []
    store['users']['last_names'] = []
    store['users']['user_handles'] = []

    store['channels']['owner_user_id'] = []
    store['channels']['name'] = []
    store['channels']['is_public'] = []
    store['channels']['all_members'] = []
    store['channels']['messages'] = []

    data_store.set(store)
