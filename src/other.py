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

def print_store_debug():
    store = data_store.get()
    
    print("----------------")
    print("PRINTING LOGGED IN USERS")
    print("----------------")
    print(store['logged_in_users'])

    print(" ")

    print("----------------")
    print("PRINTING USERS")
    print("----------------")
    print("Printing user_id:")
    print(store['users']['user_id'])
    print("Printing emails:")
    print(store['users']['emails'])
    print("Printing passwords (hashed):")
    print(store['users']['passwords'])
    print("Printing first_names:")
    print(store['users']['first_names'])
    print("Printing last_names:")
    print(store['users']['last_names'])
    print("Printing user_handles:")
    print(store['users']['user_handles'])
    print("Printing is_global_owner")
    print(store['users']['is_global_owner'])
    print("Printing Permissions")
    print(store['users']['permissions'])

    print(" ")

    print("----------------")
    print("PRINTING CHANNELS")
    print("----------------")
    print("Printing channel_id:")
    print(store['channels']['channel_id'])
    print("Printing channel_name:")
    print(store['channels']['channel_name'])
    print("Printing owner_user_id:")
    print(store['channels']['owner_user_id'])
    print("Printing is_public:")
    print(store['channels']['is_public'])
    print("Printing all_members:")
    print(store['channels']['all_members'])
    print("Printing messages:")
    print(store['channels']['messages'])

    print(" ")

    print("----------------")
    print("PRINTING MESSAGES")
    print("----------------")
    print(store['messages'])

    print(" ")

    print("----------------")
    print("PRINTING DMS")
    print("----------------")
    print("Printing dm_id:")
    print(store['dms']['dm_id'])
    print("Printing owner_user_id:")
    print(store['dms']['owner_user_id'])
    print("Printing dm_name:")
    print(store['dms']['dm_name'])
    print("Printing all_members:")
    print(store['dms']['all_members'])
    print("Printing messages:")
    print(store['dms']['messages'])
    pass





