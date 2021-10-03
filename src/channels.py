from src.data_store import data_store
from src.error import InputError

''' 
Both Channels list functions create a new list of dictionaries
structure that utilize the data store to gather details of all 
existing channels and those that contain a given user ID.
'''

def channels_list_v1(auth_user_id):
    '''
    Arguements:
        auth_user_id (int) - idetifying variable for each user 

    Return Value:
        returns new_list: list of dicionaries containing channel 
        id's and names of all existing channels that the given 
        User ID is a member of.
    '''

    new_list = {'channels':[]}

    store = data_store.get()
    i = 0
    for members in store['channels']['all_members']:

        # Tracks the Channel ID by its index in the 'channel' data_store
        name = store['channels']['channel_name'][i]
        new_dict = { 'channel_id': i, 'name': name}

        # Filters the added channels by the existance of User in 
        # the members
        if auth_user_id in members:
            new_list['channels'].append(new_dict)

        i += 1

    return new_list

# Works like the previous function with the ommission of User Filter
def channels_listall_v1(auth_user_id):
    '''
    Arguements:
        auth_user_id (int) - idetifying variable for each user 

    Return Value:
        returns new_list: list of dicionaries containing channel 
        id's and names of all existing channels.
    '''

    new_list = {'channels':[]}

    store = data_store.get()
    i = 0
    for name in store['channels']['channel_name']:
        
        new_dict = {'channel_id': i, 'name': name}
        new_list['channels'].append(new_dict)

        i += 1

    return new_list

def channels_create_v1(auth_user_id, name, is_public):

    check_channel_name(name)

    all_members_in_channel = []

    all_members_in_channel.append(auth_user_id)
 
    store = data_store.get()

    store['channels']['owner_user_id'].append(auth_user_id)
    store['channels']['channel_name'].append(name)
    store['channels']['is_public'].append(is_public)
    store['channels']['all_members'].append(all_members_in_channel)

    data_store.set(store)

    i = 0
    for data_owner_user_id in store["channels"]["owner_user_id"]:
        i += 1
    

    channel_id = i - 1

    return {
        'channel_id': channel_id,
    } 

    '''
    The function above takes in the auth_user_id and name and is_public
    and checks if the channel name the user has given us is valid, if it 
    is valid, store the channel_creator user id in all members and stores user
    data in data store.

    Arguments:
        auth_user_id - Integers      -  Used to identify users.
        name - Strings               -  Channel name.
        is_public - Boolean          -  Checks if channel is public.

    Exceptions:
        InputError - InputError is given when length of channel_name is not in between 1 and 20
                     inclusive.

    Return Value:
        Return 'channel_id': channel_id - If channel name is between 1 and 20 inclusive then 
                                          return 'channel_id': channel_id.

    '''


    # Function to check if name is within 1 and 20 characters.
def check_channel_name(name):
    if len(name) >= 1 and len(name) <= 20:
        pass
    else:
        raise InputError('Length of channel name must be between 1 and 20 characters!')
