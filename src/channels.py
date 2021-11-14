from src.data_store import data_store
from src.error import InputError
from src.auth_auth_helpers import check_and_get_user_id
from datetime import datetime, timezone

''' 
Both Channels list functions create a new list of dictionaries
structure that utilize the data store to gather details of all 
existing channels and those that contain a given user ID.
'''

def channels_list_v1(token):
    '''
    Arguments:
        token(strings) - Identifies User

    Return Value:
        returns new_list: list of dicionaries containing channel 
        id's and names of all existing channels that the given 
        User ID is a member of.
    '''
    auth_user_id = check_and_get_user_id(token)

    new_list = []

    store = data_store.get()
    i = 0
    for members in store['channels']['all_members']:

        name = store['channels']['channel_name'][i]
        new_dict = {'channel_id': i, 'name': name}

        if auth_user_id in members:
            new_list.append(new_dict)

        i += 1

    return {'channels': new_list}

def channels_listall_v1(token):
    '''
    Arguments:
        token(strings) - Identifies the user 

    Return Value:
        returns new_list: list of dicionaries containing channel 
        id's and names of all existing channels.
    '''

    check_and_get_user_id(token)
    
    new_list = {'channels':[]}

    store = data_store.get()
    i = 0
    for name in store['channels']['channel_name']:
        
        new_dict = {'channel_id': i, 'name': name}
        new_list['channels'].append(new_dict)

        i += 1

    return new_list

def channels_create_v1(token, name, is_public):
    '''
    The function above takes in the auth_user_id and name and is_public
    and checks if the channel name the user has given us is valid, if it 
    is valid, store the channel_creator user id in all members and stores user
    data in data store.

    Arguments:
        token - String               -  Used to identify users.
        name - Strings               -  Channel name.
        is_public - Boolean          -  Checks if channel is public.

    Exceptions:
        InputError - InputError is given when length of channel_name is not in between 1 and 20
                     inclusive.

    Return Value:
        Return 'channel_id': channel_id - If channel name is between 1 and 20 inclusive then 
                                          return 'channel_id': channel_id.

    '''

    user_id = check_and_get_user_id(token)
    check_channel_name(name)
    all_members_in_channel = []
    all_members_in_channel.append(user_id)
    store = data_store.get()

    store['channels']['owner_user_id'].append([user_id])
    store['channels']['channel_name'].append(name)
    store['channels']['is_public'].append(is_public)
    store['channels']['all_members'].append(all_members_in_channel)
    store['channels']['messages'].append([])
    store['channels']['is_standup_active'].append(False)
    store['channels']['standup_time_finish'].append(0)
    store['channels']['standup_messages'].append([])

    i = 0
    for _ in store["channels"]["owner_user_id"]:
        i += 1
    
    channel_id = i - 1
    store['channels']['channel_id'].append(channel_id)
    data_store.set(store)

    store['users']['channels_joined'][user_id] += 1
    append_user_stat_data_channel(user_id)

    store['channels_exist'] += 1
    append_workspace_stats_channel()  

    return {'channel_id': channel_id} 

def check_channel_name(name):
    '''
    Checks if a channel name is valid, between 1 and 20 characters inclusive.

    Arguments:
        name    (string)    - Channel name

    Return Value:
        returns new_list: list of dicionaries containing channel 
        id's and names of all existing channels that the given 
        User ID is a member of.
    '''
    if len(name) < 1 or len(name) > 20:
        raise InputError('Length of channel name must be between 1 and 20 characters!')

def append_user_stat_data_channel(u_id):
    '''
    This function updates the user statitics data once a change is made in the number of channels.

    Arguments:
        u_id (int) - The user id.

    Exceptions:
        No given exceptions
    ''' 

    store = data_store.get()
    
    # Determine how many channels, dms and messages the user has joined/sent
    channels_joined = store['users']['channels_joined'][u_id]
    dms_joined = store['users']['dms_joined'][u_id]
    messages_sent = store['users']['messages_sent'][u_id]    
    
    # Determine total number of channels
    total_channels = len(store['channels']['channel_id'])
    total_dms = len(store['dms']['dm_id'])
    total_messages = len(store['messages'])

    time_stamp = int(datetime.now(timezone.utc).timestamp())

    channel_new_stat = {'num_channels_joined': channels_joined, 'time_stamp': time_stamp}

    store['users']['channels_user_data'][u_id].append(channel_new_stat)
    
    involvement_rate = 0
    if (channels_joined + dms_joined + messages_sent) > 0:
        involvement_rate = (channels_joined + dms_joined + messages_sent) / (total_channels + total_dms + total_messages)

    if involvement_rate > 1:
        involvement_rate = 1

    store['users']['involvement_rate'][u_id] = involvement_rate

def append_workspace_stats_channel():
    '''
    This function updates the workspace statitics data once a change is made in the number of channels.

    Exceptions:
        No given exceptions
    ''' 
    store = data_store.get()
    
    # Determine how many channels, dms and messages exists
    channels_exist = store['channels_exist']
    # dms_exist = store['dms_exist']
    # messages_exist = store['messages_exist']

    time_stamp = int(datetime.now(timezone.utc).timestamp())

    channels_new_stat = {'num_channels_exist': channels_exist, 'time_stamp': time_stamp}
    store['workspace_stat_channels'].append(channels_new_stat)

    num_users_who_have_joined_at_least_one_channel_or_dm = 0
    num_users = len(store['users']['user_id'])
    for u_id in store['users']['user_id']:
        if store['users']['channels_joined'][u_id] > 0:
            num_users_who_have_joined_at_least_one_channel_or_dm += 1
        elif store['users']['dms_joined'][u_id] > 0:
            num_users_who_have_joined_at_least_one_channel_or_dm += 1

    store['utilization_rate'] = num_users_who_have_joined_at_least_one_channel_or_dm / num_users
