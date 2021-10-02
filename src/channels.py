from src.data_store import data_store
from src.error import InputError

''' 
Both Channels list functions create a new list of dictionaries
structure that utilize the data store to gather details of all 
existing channels and those that contain a given user ID, returning
the newly created structure upon completion
'''

def channels_list_v1(auth_user_id):
    new_list = {'channels':[]}

    store = data_store.get()
    i = 0
    for members in store['channels']['all_members']:

        # Tracks the Channel_id by its index in the 'channel' data_store'
        name = store['channels']['channel_name'][i]
        new_dict = { 'channel_id': i, 'name': name}

        # Filters the added channels by the existance of the User
        # in the members
        if auth_user_id in members:
            new_list['channels'].append(new_dict)

        i += 1

    return new_list

# Works in a similar fashion to previous function with the 
# ommision of User filter
def channels_listall_v1(auth_user_id):
    new_list = {'channels':[]}

    store = data_store.get()
    i = 0
    for name in store['channels']['channel_name']:
        
        new_dict = {'channel_id': i, 'name': name}
        new_list['channels'].append(new_dict)

        i += 1

    return new_list

def channels_create_v1(auth_user_id, name, is_public):

    # Check length of name
    check_channel_name(name)

    all_members_in_channel = []

    all_members_in_channel.append(auth_user_id)

    # Stores necessary data into the data store 
    store = data_store.get()

    store['channels']['owner_user_id'].append(auth_user_id)
    store['channels']['channel_name'].append(name)
    store['channels']['is_public'].append(is_public)
    store['channels']['all_members'].append(all_members_in_channel)

    data_store.set(store)

    # Loops through the channel owner_user_id with a seperate 
    # iterator to find the channel_id(index)
    i = 0
    for x in store["channels"]["owner_user_id"]:
        i += 1
    
    # We want to start index with 0, the for loop above
    # Gives index that is 1 over what we expect hence minus 1.
    channel_id = i - 1

    return channel_id 


    # Function to check if name is within 1 and 20 characters.
def check_channel_name(name):
    if len(name) >= 1 and len(name) <= 20:
        pass
    else:
        raise InputError('Length of channel name must be between 1 and 20 characters!')
        