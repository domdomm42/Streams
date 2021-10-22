from src.data_store import data_store
from src.error import InputError, AccessError
from src.auth import auth_register_v1
from src.auth_auth_helpers import check_and_get_user_id
from src.other import print_store_debug
import requests


def dm_create_v1(token, u_ids):
    '''
    Creates a new DM where the owner is the user calling the function (token),
    whereby all members are given by the u_ids list and the name is a stringated 
    version of the u_ids list + the owner.

    Arguments:
        token <string>: identifying value for the calling user
        u_ids <list>: all users that the message is directed to  

    Exceptions:
        AccessError: where the token given is invalid or doesnt exist in database
        InputError: any user ID's in u_ids list is invalid/non-existent in database
        
    Return Value:
        dm_id <integer>: the identifying number for each newly created DM

    '''
    store = data_store.get()

    # Validity checks for each token and u_ids
    auth_user_id = check_and_get_user_id(token)
    check_valid_user(u_ids, store)
    
    # Add function caller/dm owner to user list
    u_ids.append(auth_user_id)
    all_users = u_ids

    # Create name for dm as stringated list of u_ids
    all_names = []
    for name in all_users:
        index = store['users']['user_id'].index(name)
        all_names.append(store['users']['user_handles'][index])

    all_names.sort()
    dm_name = ''
    for element in all_names:
        dm_name = dm_name + ', ' + element
    dm_name = dm_name[2:]

    # Add all necessary fields into data store
    if len(store['dms']['dm_id']) == 0:
        dm_id = 0
    else:
        dm_id = store['dms']['dm_id'][-1] + 1

    store['dms']['dm_id'].append(dm_id)
    store['dms']['dm_name'].append(dm_name)
    store['dms']['owner_user_id'].append(auth_user_id)
    store['dms']['all_members'].append(all_users)
    store['dms']['messages'].append([])

    return {'dm_id': dm_id}

def dm_list_v1(token):
    '''
    Creates a list of dictionaries that contain the name and ID of all DMs
    
    Arguments:
        token <string>:  identifying value for the calling user

    Exceptions:
        AccessError: where the token given is invalid or doesnt exist in database

    Return Value:
        dms <list>: list of dictionaries containing fields dm_id and name
    
    '''
    # Checks token for validity
    check_and_get_user_id(token)

    store = data_store.get()
    new_list = {'dms':[]}

    # creates a list of dictionaries using the index given by the dm_id in data_store
    for idx in range(len(store['dms']['dm_id'])):
        new_dict = {'dm_id': store['dms']['dm_id'][idx], 'name': store['dms']['dm_name'][idx]}
        new_list['dms'].append(new_dict)

    return new_list

def dm_remove_v1(token, dm_id):
    '''
    Removes an existing DM from the database, therefore all members are no longer in the DM
    Can only be done by the original creator/first owner of the DM

    Arguments:
        token <string>:  identifying value for the calling user
        dm_id <integer>: identifying value for the dm being removed

    Exceptions:
        AccessError: where the token given is invalid or doesnt exist in database
        AccessError: where the authorised user is not he original creator of the DM
        InputError: dm_id does not exist in the database/is invalid
    Return Value:
        N/A
    
    '''
    store = data_store.get()

    auth_user_id = check_and_get_user_id(token)
    check_valid_dm(dm_id, store)
    check_original_dm(auth_user_id, dm_id, store)

    index = index_from_dm_id(dm_id, store)

    del store['dms']['dm_id'][index]
    del store['dms']['owner_user_id'][index]
    del store['dms']['dm_name'][index]
    del store['dms']['messages'][index]
    del store['dms']['all_members'][index]

    #might neeed to add something to delete from the messages dictionary    

    return {
    }

def dm_details_v1(token, dm_id):
    '''
    Provides the basic details of the DM being called, including the name, members and
    all associated details for each member in a list of dicionaries  

    Arguments:
        token <string>:  identifying value for the calling user
        dm_id <integer>: identifying value for the dm being removed

    Exceptions:
        AccessError: where the token given is invalid or doesnt exist in database
        AccessError: where the authorised user is not a member of the DM
        InputError: dm_id does not exist in the database/is invalid

    Return Value:
        name <string>: the name of the DM
        members <list>: list of dictionaries containing the fields u_ids, email, first name
                        last name and user handle for all members of the DM    
    '''
    store = data_store.get()
    u_id_list = []

    auth_user_id = check_and_get_user_id(token)
    check_valid_dm(dm_id, store)
    check_user_in_dm(auth_user_id, dm_id, store)

    index = index_from_dm_id(dm_id, store)
    name = store['dms']['dm_name'][index]

    #gets the index of the u_id in the data_store and uses that to extract memebr information from users
    #u_id is just he index they are in the users library for this iteration
    for u_id in store['dms']['all_members'][index]:
        new_dict = {
            'u_id': store['users']['user_id'][u_id],
            'email': store['users']['emails'][u_id],
            'name_first': store['users']['first_names'][u_id],
            'name_last': store['users']['last_names'][u_id],
            'handle_str': store['users']['user_handles'][u_id]
        }
        u_id_list.append(new_dict)
            

    return {
        'name': name,
        'members': u_id_list
    }

def dm_leave_v1(token, dm_id):
    '''
    Removes the authorised user from the DM, this can be the owner/creator, without
    changing the name of the DM

    Arguments:
        token <string>:  identifying value for the calling user
        dm_id <integer>: identifying value for the dm being removed

    Exceptions:
        AccessError: where the token given is invalid or doesnt exist in database
        AccessError: where the authorised user is not a member of the DM
        InputError: dm_id does not exist in the database/is invalid

    Return Value:
        N/A
    '''
    store = data_store.get()

    
    auth_user_id = check_and_get_user_id(token)
    check_valid_dm(dm_id, store)
    check_user_in_dm(auth_user_id, dm_id, store)
    index = index_from_dm_id(dm_id, store)

    store['dms']['all_members'][index].remove(auth_user_id)

    #if the function call is made by the owner of the dm then he is removed 
    if store['dms']['owner_user_id'][index] == auth_user_id:
        # -1 states that there is no owner in the dm
        store['dms']['owner_user_id'][index] = -1

    
    return {}
    

def dm_messages_v1(token, dm_id, start):
    '''
    Extracts messages and their associated details from the DM provided, 
    beginning at the index provided by the start. 
    Returns the first 50 messages from the start with the end being start + 50, 
    or -1 if there are no more messages to extract.

    Arguments:
        token <string>:  identifying value for the calling user
        dm_id <integer>: identifying value for the dm being removed
        start <integer>: the message_id where the caller wants to begin extracting the most
                         recent 50 messages
    Exceptions:
        AccessError: where the token given is invalid or doesnt exist in database
        AccessError: where the authorised user is not a member of the DM
        InputError: dm_id does not exist in the database/is invalid
        InputError: where the provided start is greater than the total number of messages
                    in the DM

    Return Value:
        messages <list>: list of dictionaries containing the fields message_id, u_id,
                         message, time_created
        start <integer>: the index where the function began extracting messages
        end <integer>: the index where the function finished extracting messages
    
    '''
    # messages data_store is just a list of lists containing the messages by index based on whether they are in dm_id 1 or dm_id 2, etc.
    # this function just redirects to the messages data_store to get the details of the messages
    store = data_store.get()
    
    auth_user_id = check_and_get_user_id(token)
    check_valid_dm(dm_id, store)
    check_user_in_dm(auth_user_id, dm_id, store)
    

    # if start is greater than number of functions return InputError
    if start > len(store['dms']['messages']):
        raise InputError('invalid start, fewer messages than expected.')

    messages = []
    message_index = store['dms']['messages'][start:]

    num_message = 0
    for index in message_index:
        if num_message >= 50:
            break
        i = 0
        while i < len(store['messages']):

            if index == store['messages'][i]['message_id']:
                new_dict = {
                    'message_id': store['messages'][i]['message_id'],
                    'u_id': store['messages'][i]['u_id'],
                    'message': store['messages'][i]['message'],
                    'time_created': store['messages'][i]['time_created']
                }
                messages.append(new_dict)
                num_message += 1
                break
            i += 1
            
    if num_message < 50:
        end = -1
    else:
        end = start + 50

    return {'messages': messages, 'start': start, 'end': end}

# Helper functions

# Checks if the dm is stored in the database/is a valid dm_id
def check_valid_dm(dm_id, store):
    if dm_id not in store['dms']['dm_id']:
        raise InputError('Invalid DM ID given')
    else:
        return    

# Checks if the authorised user (token) is a member of the DM
def check_user_in_dm(u_id, dm_id, store):
    index = index_from_dm_id(dm_id, store)
    
    if u_id not in store['dms']['all_members'][index]:
        raise AccessError('Given User is not a memeber of DM')
    else:
        return

# Checks if the authorised user (token) is the original owner of the DM
def check_original_dm(u_id, dm_id, store):
    index = index_from_dm_id(dm_id, store)

    if u_id != store['dms']['owner_user_id'][index]:
        raise AccessError('Only the original DM creator can remove a DM')
    else:
        return

# Checks if the token given appears in the data store, if not it must be invalid
def check_valid_token(token, store):
    if token not in store['users']['tokens']:
        raise AccessError('Invalid Token given')
    else:
        return

# Checks if the list of users given actually exists in streams
def check_valid_user(u_ids, store):
    for user in u_ids:
        if user not in store['users']['user_id']:
            raise InputError('One or more of given users are not valid')
        else:
            pass     

# Loops through all id's to find the index of the value given
def index_from_dm_id(dm_id, store):
    i = 0
    for i in store['dms']['dm_id']:
        if dm_id == i:
            break
        i += 1
    return i
