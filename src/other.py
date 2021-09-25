from src.data_store import data_store

def clear_v1():

    store = data_store.get()
    
    store['users']['emails'] = []
    store['users']['passwords'] = []
    store['users']['first_names'] = []
    store['users']['last_names'] = []
    store['users']['user_handles'] = []

    store['owner_user_id']['emails'] = []
    store['is_public']['passwords'] = []
    store['all_members']['first_names'] = []
    store['messages']['last_names'] = []

    data_store.set(store)
