from src.data_store import data_store
from src.auth_auth_helpers import check_and_get_user_id

def notifications_get_v1(token):
    ''' 
    This function obtains the 20 most recent notifications of the user.

    Arguments:
        token     (string)   - Used to check whether the user attempting to access this function is 

    Return Value:
        Returns 20 most recent notifications.
    '''
    user_id = check_and_get_user_id(token)
    
    store = data_store.get()
    notifications = store['users']['notifications'][user_id][-1:-21:-1]

    return {'notifications': notifications}

def tag_users_in_channel_message(sender_id, message, channel_id):
    ''' 
    Tags the users who are @'ed in a channel message. 
    Assumes that the sender of the message is the owner of the channel.

    Arguments:
        sender_id       (integer)   - The ID of the person who is sent the message
        message         (string)    - The message.
        channel_id      (integer)   - The ID of the channel which the message has been sent to

    Return Value:
        No return value.
    '''
    store = data_store.get()
    for user_handle in store['users']['user_handles']:
        tagged_user_id = store['users']['user_handles'].index(user_handle)
        sender_user_handle = store['users']['user_handles'][sender_id]
        channel_name = store['channels']['channel_name'][channel_id]
        user_handle = '@' + user_handle
        if user_handle in message and tagged_user_id in store['channels']['all_members'][channel_id] and tagged_user_id != sender_id:
            notification = {
                'channel_id': channel_id,
                'dm_id': -1,
                'notification_message': f'{sender_user_handle} tagged you in {channel_name}: {message[0:20]}' 
            }
            store['users']['notifications'][tagged_user_id].append(notification)

    data_store.set(store)

def alert_user_channel_invited(inviter_id, invitee_id, channel_id):
    ''' 
    Alerts the user that they have been invited to a channel through notifications.

    Arguments:
        inviter_id         (string)   - The ID of the inviter.
        invitee_id         (string)   - The ID of the invitee.
        channel_id         (string)   - The ID of the channel.

    Return Value:
        No return value.
    '''
    store = data_store.get()

    inviter_user_handle = store['users']['user_handles'][inviter_id]
    channel_name = store['channels']['channel_name'][channel_id]

    notification = {
        'channel_id': channel_id,
        'dm_id': -1,
        'notification_message': f'{inviter_user_handle} added you to {channel_name}'
    }

    store['users']['notifications'][invitee_id].append(notification)

    data_store.set(store)

def alert_user_dm_invited(inviter_id, invitee_id, dm_id):
    ''' 
    Alerts the user that they have been invited to a DM through notifications.

    Arguments:
        inviter_id         (string)   - The ID of the inviter.
        invitee_id         (string)   - The ID of the invitee.
        dm_id              (string)   - The ID of the DM.

    Return Value:
        No return value.
    '''
    store = data_store.get()

    inviter_user_handle = store['users']['user_handles'][inviter_id]
    dm_name = store['dms']['dm_name'][dm_id]

    notification = {
        'channel_id': -1,
        'dm_id': dm_id,
        'notification_message': f'{inviter_user_handle} added you to {dm_name}'
    }

    store['users']['notifications'][invitee_id].append(notification)

    data_store.set(store)

def tag_users_in_dm_message(sender_id, message, dm_id):
    ''' 
    Tags the users who are @'ed in a channel message. 
    Assumes that the sender of the message is the owner of the channel.

    Arguments:
        sender_id       (integer)   - The ID of the person who is sent the message
        message         (string)    - The message.
        dm_id           (integer)   - The ID of the DM which the message has been sent to

    Return Value:
        No return value.
    '''
    store = data_store.get()
    for user_handle in store['users']['user_handles']:
        tagged_user_id = store['users']['user_handles'].index(user_handle)
        sender_user_handle = store['users']['user_handles'][sender_id]
        dm_name = store['dms']['dm_name'][dm_id]
        user_handle = '@' + user_handle
        if user_handle in message and tagged_user_id in store['dms']['all_members'][dm_id] and tagged_user_id != sender_id:
            notification = {
                'channel_id': -1,
                'dm_id': dm_id,
                'notification_message': f'{sender_user_handle} tagged you in {dm_name}: {message[0:20]}' 
            }
            store['users']['notifications'][tagged_user_id].append(notification)

    data_store.set(store)

def alert_user_reacted_to_message_dm(reacter_to_message_id, owner_of_message_id, dm_id):
    ''' 
    Alerts the user that someone has reacted to their message in a DM.

    Arguments:
        reacter_to_message_id       (string)   - The ID of the person reacting to the message.
        owner_of_message_id         (string)   - The ID of the owner of the message.
        dm_id                       (integer)  - The ID of the DM.

    Return Value:
        No return value.
    '''
    store = data_store.get()

    reacter_to_message_user_handle = store['users']['user_handles'][reacter_to_message_id]
    dm_name = store['dms']['dm_name'][dm_id]

    notification = {
        'channel_id': -1,
        'dm_id': dm_id,
        'notification_message': f'{reacter_to_message_user_handle} reacted to your message in {dm_name}'
    }

    store['users']['notifications'][owner_of_message_id].append(notification)

    data_store.set(store)

def alert_user_reacted_to_message_channel(reacter_to_message_id, owner_of_message_id, channel_id):
    ''' 
    Alerts the user that someone has reacted to their message in a channel.

    Arguments:
        reacter_to_message_id       (string)   - The ID of the person reacting to the message.
        owner_of_message_id         (string)   - The ID of the owner of the message.
        channel_id                  (integer)  - The ID of the channel.

    Return Value:
        No return value.
    '''
    store = data_store.get()

    reacter_to_message_user_handle = store['users']['user_handles'][reacter_to_message_id]
    channel_name = store['channels']['channel_name'][channel_id]

    notification = {
        'channel_id': -1,
        'dm_id': channel_id,
        'notification_message': f'{reacter_to_message_user_handle} reacted to your message in {channel_name}'
    }

    store['users']['notifications'][owner_of_message_id].append(notification)

    data_store.set(store)