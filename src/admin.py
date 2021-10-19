from src.data_store import data_store
from src.error import InputError, AccessError
from src.auth_auth_helpers import check_and_get_user_id

def admin_user_remove_v1(token, user_id):

    store = data_store.get()
    remover_id = check_and_get_user_id(token)

    list_user_id = []
    list_global_owner = []

    # Stores all user_id in a seperate list
    for user_data_id in store["users"]["user_id"]:
        list_user_id.append(user_data_id)

    idx_of_user_id = 0
    for user_ids in list_user_id:
        if user_ids == user_id:
            break
        else:
            idx_of_user_id = idx_of_user_id + 1


    num_of_global_owner = 0

    # Stores all global owner in a seperate list and counts no. of global owner.
    for global_owner in store["users"]["is_global_owner"]:
        if global_owner == True:
            num_of_global_owner = num_of_global_owner + 1

        list_global_owner.append(global_owner)

    # Invalid User_ID
    if user_id not in list_user_id:
        raise InputError('user_id does not refer to a valid user!')
        
    # User_id is the only global owner
    if user_id in list_global_owner and num_of_global_owner == 1:
        raise InputError('user_id refers to a user who is the only global owner!')

    # Finds the index of the Remover_ID
    counter = 0
    for index_of_user_ids in list_user_id:
        if index_of_user_ids == remover_id:
            break
        else:
            counter = counter + 1

    # Checks if the remover is global Owner
    check_if_global_owner = store['users']['is_global_owner'][counter]

    # Raise error if Remover is not global owner
    if check_if_global_owner is False:
        raise AccessError(description='The authorised user is not a global owner!')

    # Set messages sent by removed user to be 'Removed User'
    for message in store['messages']:
        if message['u_id'] == remover_id:
            idx = store['messages'].index(message)
            store['messages'][idx]['message'] = 'Removed User'

    store['users']['first_names'][idx_of_user_id] = 'Removed'
    store['users']['last_names'][idx_of_user_id] = 'User'
    store['users']['emails'][idx_of_user_id] = 'X'
    store['users']['passwords'][idx_of_user_id] = 'X'
    store['users']['user_handles'][idx_of_user_id] = 'X'
    store['users']['is_global_owner'][idx_of_user_id] = False
    store['users']['remove_user'][idx_of_user_id] = True

    data_store.set(store)


    
def admin_userpermission_change_v1(token, user_id, permission_id):
    
    store = data_store.get()
    # Wrong Permission ID
    if int(permission_id) is not 1 or int(permission_id) is not 2 :
        raise InputError(description='Invalid Permission_ID!')

    # Non-existent user_id
    if user_id not in store['users']['user_id']:
        raise InputError(description='User_id does not refer to a valid user')

    list_user_id = []
    list_global_owner = []

    # Stores user_ids in a list
    for user_data_id in store["users"]["user_id"]:
        list_user_id.append(user_data_id)

    idx_of_user_id = 0
    for user_ids in list_user_id:
        if user_ids == user_id:
            break
        else:
            idx_of_user_id = idx_of_user_id + 1

    num_of_global_owner = 0

    check_if_global_owner = store['users']['is_global_owner'][idx_of_user_id]

    # Stores all global owner in a seperate list and counts no. of global owner.
    for global_owner in store["users"]["is_global_owner"]:
        if global_owner == True:
            num_of_global_owner = num_of_global_owner + 1

        list_global_owner.append(global_owner)

    if permission_id == 2 and check_if_global_owner and num_of_global_owner == 1:
        raise InputError(description='u_id refers to a user who is the only global owner and they are being demoted to a user')

    changer_id = check_and_get_user_id(token)

    for all_user_id in store['users']['user_id']:
        if all_user_id == changer_id:
            changer_idx = store['users']['user_id'].index(all_user_id)

    if list_global_owner[changer_idx] == False:
        raise AccessError(description='the authorised user is not a global owner')


    store['users']['permissions'][idx_of_user_id] == permission_id

    data_store.set(store)

