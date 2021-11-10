from src.data_store import data_store
from src.error import InputError, AccessError
from src.auth import auth_register_v1
from src.auth_auth_helpers import check_and_get_user_id
from src.notifications import alert_user_dm_invited
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
    user_ids = u_ids[:]
    
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

    # Notify relevant users that they have been added to a DM
    # u_ids.pop()

    for u_id in user_ids:
        alert_user_dm_invited(auth_user_id, u_id, dm_id)

    data_store.set(store)

    return {'dm_id': dm_id}

def dm_list_v1(token):
    '''
    Creates a list of dictionaries that contain the name and ID of all DMs that the user is a member of
    
    Arguments:
        token <string>:  identifying value for the calling user

    Exceptions:
        AccessError: where the token given is invalid or doesnt exist in database

    Return Value:
        dms <list>: list of dictionaries containing fields dm_id and name
    
    '''
    # Checks token for validity
    auth_user_id = check_and_get_user_id(token)

    store = data_store.get()
    new_list = {'dms':[]}

    # creates a list of dictionaries using the index given by the dm_id in data_store
    for idx in range(len(store['dms']['dm_id'])):
        index = index_from_dm_id(idx, store)
        if auth_user_id in store['dms']['all_members'][index]:
            new_dict = {'dm_id': store['dms']['dm_id'][index], 'name': store['dms']['dm_name'][index]}
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

    # Validity checks for user_id, dm_id and original owner
    auth_user_id = check_and_get_user_id(token)
    check_valid_dm(dm_id, store)
    check_original_dm(auth_user_id, dm_id, store)

    # removes the dm and its fields
    index = index_from_dm_id(dm_id, store)

    del store['dms']['dm_id'][index]
    del store['dms']['owner_user_id'][index]
    del store['dms']['dm_name'][index]
    del store['dms']['messages'][index]
    del store['dms']['all_members'][index]

      
    data_store.set(store)

    return {
    }

def dm_details_v1(token, dm_id):
    '''
    Provides the basic details of the DM being called, including the name, members and
    all associated details for each member in a list of dicionaries  

    Arguments:
        token <string>:  identifying value for the calling user
        dm_id <integer>: identifying value for the dm being called

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

    # get requests using .args() stringate the given fields so we need to cast them as ints for use
    dm_id = int(dm_id)

    # Validity checks as above 
    auth_user_id = check_and_get_user_id(token)
    check_valid_dm(dm_id, store)
    check_user_in_dm(auth_user_id, dm_id, store)

    name_index = index_from_dm_id(dm_id, store)
    name = store['dms']['dm_name'][name_index]

    # Gets the index of the u_id in the data_store and uses that to extract member information from users
    # u_id is just the index they are in the users library
    for u_id in store['dms']['all_members'][name_index]:
        u_id_index = index_from_u_id(u_id, store)
        new_dict = {
            'u_id': store['users']['user_id'][u_id_index],
            'email': store['users']['emails'][u_id_index],
            'name_first': store['users']['first_names'][u_id_index],
            'name_last': store['users']['last_names'][u_id_index],
            'handle_str': store['users']['user_handles'][u_id_index]
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
        dm_id <integer>: identifying value for the dm being called

    Exceptions:
        AccessError: where the token given is invalid or doesnt exist in database
        AccessError: where the authorised user is not a member of the DM
        InputError: dm_id does not exist in the database/is invalid

    Return Value:
        N/A
    '''
    store = data_store.get()

    # Validity checks as above
    auth_user_id = check_and_get_user_id(token)
    check_valid_dm(dm_id, store)
    check_user_in_dm(auth_user_id, dm_id, store)

    index = index_from_dm_id(dm_id, store)

    store['dms']['all_members'][index].remove(auth_user_id)

    #if the function call is made by the owner of the dm then he is removed 
    if store['dms']['owner_user_id'][index] == auth_user_id:
        # -1 states that there is no owner in the dm
        store['dms']['owner_user_id'][index] = -1
    
    data_store.set(store)
    return {}
    

def dm_messages_v1(token, dm_id, start):
    '''
    Extracts messages and their associated details from the DM provided, 
    beginning at the index provided by the start. 
    Returns the first 50 messages from the start with the end being start + 50, 
    or -1 if there are no more messages to extract.

    Arguments:
        token <string>:  identifying value for the calling user
        dm_id <integer>: identifying value for the dm being called
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

    # Validity checks as above
    auth_user_id = check_and_get_user_id(token)
    check_valid_dm(dm_id, store)
    check_user_in_dm(auth_user_id, dm_id, store)
    
    dm_index = index_from_dm_id(dm_id, store)
    # if start is greater than number of messages return InputError
    if start > len(store['dms']['messages'][dm_index]) or start < 0:
        raise InputError('invalid start, fewer messages than expected.')
    
    messages = []

    end = start + 50
    
    for idx in range(start, end):
        try: 
            idx = store['dms']['messages'][dm_index][-1 - idx]
        except IndexError:
            end = -1
            break
        
        # Set is_this_user_reacted to True if the auth_user_id has reacted to the message
        msg = get_message(idx)
        if auth_user_id in msg['reacts']['u_ids']:
            msg['reacts']['is_this_user_reacted'] = True
        messages.append(msg)

    return {
        'messages': messages,
        'start': start,
        'end': end,
    }

# Helper functions

 
def check_valid_dm(dm_id, store):
    '''
    Checks if the dm is stored in the database/is a valid dm_id

    Arguments:
            dm_id <int>: dm ID being checked
            store <dictionary>: the data_store used to save all info

    Exceptions:
            InputError: for invalid dm_id        

    '''
    if dm_id not in store['dms']['dm_id']:
        raise InputError('Invalid DM ID given')
    

def check_user_in_dm(u_id, dm_id, store):
    '''
    Checks if the authorised user (token) is a member of the DM

    Arguments:
            u_id <int>: indetifying integer of the user
            dm_id <int>: dm ID being checked
            store <dictionary>: the data_store used to save all info

    Exceptions:
            InputError: for invalid dm_id        

    '''
    index = index_from_dm_id(dm_id, store)
    
    if u_id not in store['dms']['all_members'][index]:
        raise AccessError('Given User is not a memeber of DM')
    

def check_original_dm(u_id, dm_id, store):
    '''
    Checks if the authorised user (token) is the original owner of the DM

    Arguments:
            u_id <int>: indetifying integer of the user
            dm_id <int>: dm ID being checked
            store <dictionary>: the data_store used to save all info

    Exceptions:
            InputError: for invalid dm_id        

    '''
    index = index_from_dm_id(dm_id, store)

    if u_id != store['dms']['owner_user_id'][index]:
        raise AccessError('Only the original DM creator can remove a DM')
    
    
def check_valid_user(u_ids, store):
    '''
    Checks if the list of users given actually exists in streams

    Arguments:
            u_ids <list>: list of user ID's
            store <dictionary>: the data_store used to save all info

    Exceptions:
            InputError: invalid user given        

    '''
    for user in u_ids:
        if user not in store['users']['user_id']:
            raise InputError('One or more of given users are not valid')
             

def index_from_dm_id(dm_id, store):
    '''
    Loops through all dm_id's to find the index of the value given

    Arguments:
            dm_id <int>: dm ID being checked
            store <dictionary>: the data_store used to save all info

    Return Values:
            counter <int>: counts the index where the dm_id is located      

    '''
    counter = 0
    for num in store['dms']['dm_id']:
        if dm_id == num:
            break
        counter += 1
    return counter


def index_from_u_id(u_id, store):
    '''
    Loops through all u_id's to find the index of the value given
    
    Arguments:
            u_id <int>: indetifying integer of the user
            store <dictionary>: the data_store used to save all info

    Return Values:
            counter <int>: counts the index where the u_id is located      
    '''
    counter = 0
    for num in store['users']['user_id']:
        if u_id == num:
            break
        counter += 1
    return counter

def get_message(message_id):
    '''
    This function takes message_id and returns the message associated with message_id

    Arguments:
        message_id(int) - id of message you want to access

    Exceptions:
        No given exceptions

    Return Value:
       msg - message associated with message_id
    ''' 

    store = data_store.get()
    for msg in store['messages']:
        if msg['message_id'] == message_id:
            return msg

if __name__ == '__main__':
    # jim_joe_token = auth_register_v1('jimjoe@gmail.com', 'password', 'Jim', 'Joe')['token']
    # marry_mae_token = auth_register_v1('jimjoe12@gmail.com', 'password', 'Marry', 'Mae')['token']
    # darron_mike = auth_register_v1('jimjoe123@gmail.com', 'password', 'Darron', 'Mike')['token']

    # dm_create_v1(jim_joe_token, [1, 2])
 
    # print_store_debug()
    pass