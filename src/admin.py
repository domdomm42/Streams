from src.data_store import data_store
from src.error import InputError, AccessError
from src.auth_auth_helpers import check_and_get_user_id
from src.auth import *

def admin_user_remove_v1(token, user_id):
    '''
    This function removes a user given an authorised user id

    Arguments:
        token(string) - Authorised user token
        user_id(int)  - Id of user you want to remove

    Exceptions:
        InputError  - u_id does not refer to a valid user
        InputError  - u_id refers to a user who is the only global owner
        AccessError - The authorised user is not a global owner

    Return Value:
       {}
    ''' 
    store = data_store.get()
    remover_id = check_and_get_user_id(token)

    # ACCESS ERROR
    if store['users']['is_global_owner'][remover_id] == False:
        raise AccessError(description="Authorised user is not a global owner")

    # Invalid User_ID
    if user_id not in store['users']['user_id']:
        raise InputError('user_id does not refer to a valid user!')

    num_of_global_owner = 0

    # Stores all global owner in a seperate list and counts no. of global owner.
    for global_owner in store["users"]["is_global_owner"]:
        if global_owner == True:
            num_of_global_owner = num_of_global_owner + 1

    # User_id is the only global owner
    if store['users']['is_global_owner'][user_id] == True and num_of_global_owner == 1:
        raise InputError('user_id refers to a user who is the only global owner!')

    # Set messages sent by removed user to be 'Removed user'
    for message in store['messages']:
        if message['u_id'] == user_id:
            idx = store['messages'].index(message)
            store['messages'][idx]['message'] = 'Removed user'
       
    store['users']['first_names'][user_id] = 'Removed'
    store['users']['last_names'][user_id] = 'user'
    store['users']['emails'][user_id] = 'X'
    store['users']['passwords'][user_id] = 'X'
    store['users']['user_handles'][user_id] = 'X'
    store['users']['is_global_owner'][user_id] = False
    store['users']['removed_user'][user_id] = True
    store['users']['permissions'][user_id] = 3

    for data in store['logged_in_users']:
        if data['user_id'] == user_id:
            store['logged_in_users'].remove({'user_id': user_id, 'session_id': data['session_id']})
    
    store['channels']['all_members'][user_id] = 'X'
    store['dms']['all_members'][user_id] = 'X'

    data_store.set(store)

    return ({})


    
def admin_userpermission_change_v1(token, user_id, permission_id):

    '''
    This function changes the permission of a user given an authorised user id
    and a valid permission_id

    Arguments:
        token(string) - Authorised user token
        user_id(int)  - Id of user you want to promote or demote
        permission_id(int) - 1 for global owner, 2 for standard user

    Exceptions:
        InputError  - u_id does not refer to a valid user
        InputError  - u_id refers to a user who is the only global owner and they are being demoted to user
        Input Error - Permission_id is invalid
        AccessError - The authorised user is not a global owner

    Return Value:
       {}
    '''
    
    store = data_store.get()
    # Wrong Permission ID
    if permission_id != 1 and permission_id != 2 :
        raise InputError(description='Invalid Permission_ID!')

    # Non-existent user_id
    if user_id not in store['users']['user_id']:
        raise InputError(description='User_id does not refer to a valid user')

    list_user_id = []
    list_global_owner = []

    # Stores user_ids in a list
    for user_data_id in store["users"]["user_id"]:
        list_user_id.append(user_data_id)

    # Get index of the user_id
    num_of_user_id = 0
    for user_ids in list_user_id:
        if user_ids == user_id:
            break
        else:
            num_of_user_id = num_of_user_id + 1

    
    num_of_global_owner = 0

    check_if_global_owner = store['users']['is_global_owner'][num_of_user_id]

    # Stores all global owner in a seperate list and counts no. of global owner.
    for global_owner in store["users"]["is_global_owner"]:
        if global_owner == True:
            num_of_global_owner = num_of_global_owner + 1

        list_global_owner.append(global_owner)

    if permission_id == 2 and check_if_global_owner == 1 and num_of_global_owner == 1:
        raise InputError(description='u_id refers to a user who is the only global owner and they are being demoted to a user')

    changer_id = check_and_get_user_id(token)

    for all_user_id in store['users']['user_id']:
        if all_user_id == changer_id:
            changer_idx = store['users']['user_id'].index(all_user_id)

    if list_global_owner[changer_idx] == False:
        raise AccessError(description='the authorised user is not a global owner')


    store['users']['permissions'][num_of_user_id] = permission_id
    
    if permission_id == 1:
        store['users']['is_global_owner'][num_of_user_id] = True
    else:
        store['users']['is_global_owner'][num_of_user_id] = False

    data_store.set(store)

    return ({})




