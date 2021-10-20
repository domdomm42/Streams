from src.data_store import data_store
from src.error import InputError, AccessError
from src.auth_auth_helpers import check_and_get_user_id
from src.auth import *

def admin_user_remove_v1(token, user_id):

    store = data_store.get()
    remover_id = check_and_get_user_id(token)

    list_user_id = []
    list_globle_owner = []

    # Stores all user_id in a seperate list
    for user_data_id in store["users"]["user_id"]:
        list_user_id.append(user_data_id)

    idx_of_user_id = 0
    for user_ids in list_user_id:
        if user_ids == user_id:
            break
        else:
            idx_of_user_id = idx_of_user_id + 1


    num_of_globle_owner = 0

    # Stores all globle owner in a seperate list and counts no. of globle owner.
    for globle_owner in store["users"]["is_globle_owner"]:
        if globle_owner == True:
            num_of_globle_owner = num_of_globle_owner + 1

        list_globle_owner.append(globle_owner)

    # Invalid User_ID
    if user_id not in list_user_id:
        raise InputError('user_id does not refer to a valid user!')
        
    # User_id is the only globle owner
    if user_id in list_globle_owner and num_of_globle_owner == 1:
        raise InputError('user_id refers to a user who is the only globle owner!')

    # Finds the index of the Remover_ID
    counter = 0
    for index_of_user_ids in list_user_id:
        if index_of_user_ids == remover_id:
            break
        else:
            counter = counter + 1

    # Checks if the remover is globle Owner
    check_if_globle_owner = store['users']['is_globle_owner'][counter]

    # Raise error if Remover is not globle owner
    if check_if_globle_owner is False:
        raise AccessError(description='The authorised user is not a globle owner!')

    # Set messages sent by removed user to be 'Removed User'
    for message in store['messages']:
        if message['u_id'] == remover_id:
            idx = store['messages'].index(message)
            store['messages'][idx]['message'] = 'Removed User'

    # Loop through removed users
    idx_of_removed_users = 0
    for removed in store['users']['removed_user']:
        idx_of_removed_users = idx_of_removed_users + 1
        

    store['users']['first_names'][idx_of_user_id] = 'Removed'
    store['users']['last_names'][idx_of_user_id] = 'User'
    store['users']['emails'][idx_of_user_id] = 'X'
    store['users']['passwords'][idx_of_user_id] = 'X'
    store['users']['user_handles'][idx_of_user_id] = 'X'
    store['users']['is_globle_owner'][idx_of_user_id] = False
    # store['users']['removed_user'][idx_of_removed_users].append(True)

    data_store.set(store)
    return ({})


    
def admin_userpermission_change_v1(token, user_id, permission_id):
    
    store = data_store.get()
    # Wrong Permission ID
    if permission_id != 1 and permission_id != 2 :
        raise InputError(description='Invalid Permission_ID!')

    # Non-existent user_id
    if user_id not in store['users']['user_id']:
        raise InputError(description='User_id does not refer to a valid user')

    list_user_id = []
    list_globle_owner = []

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

    
    num_of_globle_owner = 0

    check_if_globle_owner = store['users']['is_globle_owner'][num_of_user_id]

    # Stores all globle owner in a seperate list and counts no. of globle owner.
    for globle_owner in store["users"]["is_globle_owner"]:
        if globle_owner == True:
            num_of_globle_owner = num_of_globle_owner + 1

        list_globle_owner.append(globle_owner)

    if permission_id == 2 and check_if_globle_owner == 1 and num_of_globle_owner == 1:
        raise InputError(description='u_id refers to a user who is the only globle owner and they are being demoted to a user')

    changer_id = check_and_get_user_id(token)

    for all_user_id in store['users']['user_id']:
        if all_user_id == changer_id:
            changer_idx = store['users']['user_id'].index(all_user_id)

    if list_globle_owner[changer_idx] == False:
        raise AccessError(description='the authorised user is not a globle owner')


    store['users']['permissions'][num_of_user_id] = permission_id
    
    if permission_id == 1:
        store['users']['is_globle_owner'][num_of_user_id] = True
    else:
        store['users']['is_globle_owner'][num_of_user_id] = False


    data_store.set(store)

    return ({})

if __name__ == '__main__':
    # requests.delete(f'{BASE_URL}/clear/v1')
    # user_info_reg_1 = {"email": "marryjoe@gmail.com", "password": "password", "name_first": "Marry", "name_last": "Joe"}
    # user_info_reg_2 = {"email": "marryjane@gmail.com", "password": "passwordJ", "name_first": "Marry", "name_last": "Jane"}

    # response_data_1 = requests.post(f'{BASE_URL}/auth/register/v2', json = user_info_reg_1)
    # response_data_2 = requests.post(f'{BASE_URL}/auth/register/v2', json = user_info_reg_1)

    # user_2_data = response_data_2.json()
    # user_2_data = {'token': response_data_1['token'], 'user_id': response_data_2['user_id'], 'permission_id': 1} 

    # requests.post(f'{BASE_URL}admin/userpermission/change/v1', json = user_2_data)


    # kick_data = {'token': response_data_2['token'], 'user_id': response_data_1['user_id']}
    # requests.post(f'{BASE_URL}admin_user_remove_v1', json = kick_data)
    ########################################################################################

    data_1 = auth_register_v1("marryjoe@gmail.com", "password", "Marry", "Joe")
    data_2 = auth_register_v1("marryjane@gmail.com", "passwordJ", "Marry", "Jane")

    print_store_debug()

    admin_userpermission_change_v1(data_1['token'], data_2['auth_user_id'], 1)
    print_store_debug()

    admin_user_remove_v1(data_2['token'], data_1['auth_user_id'])
    print_store_debug()




