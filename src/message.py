from src.data_store import data_store
from src.error import InputError, AccessError
from src.auth_auth_helpers import check_and_get_user_id
from src.notifications import tag_users_in_channel_message, tag_users_in_dm_message
from datetime import datetime, timezone
import threading

MESSAGE_ID_TRACKER = -1

def reset_message_id_tracker():
    '''
    Resets the message ID tracker for tokens

    Return value:
        No return value
    '''
    global MESSAGE_ID_TRACKER
    MESSAGE_ID_TRACKER = -1

def generate_new_message_id():
    '''
    Generates a new message ID for a new message
    
    Return value:
        Returns a new message ID
    '''
    global MESSAGE_ID_TRACKER
    MESSAGE_ID_TRACKER += 1
    return MESSAGE_ID_TRACKER

def message_send_v1(token, channel_id, message):
    ''' 
    This function sends a message to a specified channel, given a valid token.

    Arguments:
        token       (string)    - Used to check whether the user attempting to send a message is a valid user.
        channel_id  (integer)   - The channel_id which the message will be sent to.
        message     (string)    - The message the user wishes to send to the specified channel.
    
    Exceptions:
        Access Error    -   Invalid token.
                        -   channel_id is valid and the authorised user is not a member of the channel.
        Input Error     -   channel_id does not refer to a valid channel.
                        -   Length of message is less than 1 or over 1000 characters.
    
    Return Value:
        Returns {message_id} when no error occurs.
    '''

    # Check for any errors
    user_id = check_and_get_user_id(token)
    check_channel_id(channel_id)
    check_user_authority_in_channel(user_id, channel_id)
    check_if_message_too_long(message)
    check_if_message_too_short(message)

    store = data_store.get()
    
    # Create a message_id
    message_id = generate_new_message_id()

    time_created = int(datetime.now(timezone.utc).timestamp())

    message_react = {'react_id': 1, 'u_ids': [], 'is_this_user_reacted': False}
    message_info = {'message_id': message_id, 'u_id': user_id, 'message': message, 'time_created': time_created, 'reacts': [message_react], 'is_pinned': False}

    store['messages'].append(message_info)

    idx = store['channels']['channel_id'].index(channel_id)
    store['channels']['messages'][idx].append(message_id)
    
    tag_users_in_channel_message(user_id, message, channel_id)
    store['users']['messages_sent'][user_id] += 1
    append_user_stat_data_msg(user_id)
    
    store['messages_exist'] += 1
    append_workspace_stats_msg()

    data_store.set(store)

    return {
        'message_id': message_id
    }

def message_senddm_v1(token, dm_id, message):
    ''' 
    This function sends a message to a DM, given a valid token.

    Arguments:
        token       (string)    - Used to check whether the user attempting to send a message is a valid user.
        dm_id       (integer)   - The dm_id which the message will be sent to.
        message     (string)    - The message the user wishes to send to the specified DM.
    
    Exceptions:
        Access Error    -   Invalid token.
                        -   dm_id is valid and the authorised user is not a member of the DM.
        Input Error     -   dm_id does not refer to a valid DM.
                        -   Length of message is less than 1 or over 1000 characters.
    
    Return Value:
        Returns {message_id} when no error occurs.
    '''

    # Check for any errors
    user_id = check_and_get_user_id(token)
    check_dm_id(dm_id)
    check_user_authority_in_dm(user_id, dm_id)
    check_if_message_too_long(message)
    check_if_message_too_short(message)

    store = data_store.get()
    
    # Create a message_id
    message_id = generate_new_message_id()

    time_created = int(datetime.now(timezone.utc).timestamp())

    message_react = {'react_id': 1, 'u_ids': [], 'is_this_user_reacted': False}
    message_info = {'message_id': message_id, 'u_id': user_id, 'message': message, 'time_created': time_created, 'reacts': [message_react], 'is_pinned': False}

    store['messages'].append(message_info)

    idx = store['dms']['dm_id'].index(dm_id)
    store['dms']['messages'][idx].append(message_id)
    
    tag_users_in_dm_message(user_id, message, dm_id)
    
    store['users']['messages_sent'][user_id] += 1
    append_user_stat_data_msg(user_id)   
    
    store['messages_exist'] += 1
    append_workspace_stats_msg()

    data_store.set(store)
    return {
        'message_id': message_id
    }

def message_edit_v1(token, message_id, message):
    ''' 
    This function edits a message in a channel or DM, given a valid token.

    Arguments:
        token       (string)    - Used to check whether the user attempting to send a message is a valid user.
        message_id  (integer)   - The message_id of the message.
        message     (string)    - The message the user wishes to send to the specified channel.
    
    Exceptions:
        Access Error    -   Invalid token.
                        -   message_id refers to a valid message in a joined channel/DM and the message was not sent by the authorised user making this request.
                        -   message_id refers to a valid message in a joined channel/DM and the authorised user does not have owner permissions in the channel/DM.
        Input Error     -   message_id does not refer to a valid message within a channel/DM that the authorised user has joined.
                        -   Length of message is over 1000 characters
    
    Return Value:
        Returns {} when no error occurs.
    '''

    if message == "":
        message_remove_v1(token, message_id)
    else:
        # Check for any errors
        user_id = check_and_get_user_id(token)
        check_if_message_too_long(message)
        sender_id = check_if_message_id_exists_and_get_sender_id(message_id)

        store = data_store.get()
        for msg in store['messages']:
            if msg['message_id'] == message_id:
                message_idx = store['messages'].index(msg)

        # Determine whether the message belongs to a channel or DM
        dm_or_channel_id_of_message = get_dm_or_channel_id_of_message(message_id)

        # Message belongs to a channel
        if (dm_or_channel_id_of_message[1] == 'channel'): 
            channel_id = dm_or_channel_id_of_message[0]
            check_if_user_is_owner_of_channel_or_sender_or_global_owner(user_id, channel_id, sender_id)
            store['messages'][message_idx]['message'] = message

            # Assumes the person who is editing the message is the owner of the message
            tag_users_in_channel_message(user_id, message, channel_id)

        # Message belongs to a DM
        else:
            dm_id = dm_or_channel_id_of_message[0]
            check_if_user_is_owner_of_dm_or_sender(user_id, dm_id, sender_id)
            store['messages'][message_idx]['message'] = message

            # Assumes the person who is editing the message is the owner of the message
            tag_users_in_dm_message(user_id, message, dm_id)

        data_store.set(store)

    return {}
    
def message_remove_v1(token, message_id):
    ''' 
    This function removes a message in a channel or DM, given a valid token.

    Arguments:
        token       (string)    - Used to check whether the user attempting to send a message is a valid user.
        message_id  (integer)   - The message_id of the message.
    
    Exceptions:
        Access Error    -   Invalid token.
                        -   message_id refers to a valid message in a joined channel/DM and the message was not sent by the authorised user making this request.
                        -   message_id refers to a valid message in a joined channel/DM and the authorised user does not have owner permissions in the channel/DM.
        Input Error     -   message_id does not refer to a valid message within a channel/DM that the authorised user has joined.
    
    Return Value:
        Returns {} when no error occurs.
    '''

    # Check for any errors
    user_id = check_and_get_user_id(token)
    sender_id = check_if_message_id_exists_and_get_sender_id(message_id)

    # Get the index of the message
    store = data_store.get()
    for msg in store['messages']:
        if msg['message_id'] == message_id:
            message_idx = store['messages'].index(msg)

    # Determine whether the message belongs to a channel or DM
    dm_or_channel_id_of_message = get_dm_or_channel_id_of_message(message_id)

    # Message belongs to a channel
    if (dm_or_channel_id_of_message[1] == 'channel'): 
        channel_id = dm_or_channel_id_of_message[0]
        check_if_user_is_owner_of_channel_or_sender_or_global_owner(user_id, channel_id, sender_id)
        channel_idx = store['channels']['channel_id'].index(channel_id)
        store['messages'].pop(message_idx)
        store['channels']['messages'][channel_idx].remove(message_id)
        
    # Message belongs to a DM
    else:
        dm_id = dm_or_channel_id_of_message[0]
        check_if_user_is_owner_of_dm_or_sender(user_id, dm_id, sender_id)
        dm_idx = store['dms']['dm_id'].index(dm_id)
        store['messages'].pop(message_idx)
        store['dms']['messages'][dm_idx].remove(message_id)


    data_store.set(store)

    return {}

def message_sendlater_v1(token, channel_id, message, time_sent):
    ''' 
    This function sends a message to a specified channel at a specific time, given a valid token.

    Arguments:
        token       (string)    - Used to check whether the user attempting to send a message is a valid user.
        channel_id  (integer)   - The channel_id which the message will be sent to.
        message     (string)    - The message the user wishes to send to the specified channel.
        time_sent   (integer)   - The time which the message is to be sent at.
    
    Exceptions:
        Access Error    -   Invalid token.
                        -   channel_id is valid and the authorised user is not a member of the channel.
        Input Error     -   channel_id does not refer to a valid channel.
                        -   time_sent is in the past.
                        -   Length of message is over 1000 characters.
    
    Return Value:
        Returns {message_id} when no error occurs.
    '''

    # Check for any errors
    user_id = check_and_get_user_id(token)
    check_channel_id(channel_id)
    check_user_authority_in_channel(user_id, channel_id)
    check_if_message_too_long(message)
    check_time(time_sent)

    # Create a message_id
    message_id = generate_new_message_id()

    send_later = threading.Thread(target=send_msg_later_thread, args=(user_id, channel_id, message, time_sent, message_id))
    send_later.start()

    return {
        'message_id': message_id
    }

def send_msg_later_thread(user_id, channel_id, message, time_sent, message_id):
    ''' 
    This function is executed as a separate thread, in order to send the message later.

    Arguments:
        user_id     (integer)   - The user_id.
        channel_id  (integer)   - The channel_id which the message will be sent to.
        message     (string)    - The message the user wishes to send to the specified channel.
        time_sent   (integer)   - The time which the message is to be sent at.
    
    Exceptions:
        Access Error    -   Invalid token.
                        -   channel_id is valid and the authorised user is not a member of the channel.
        Input Error     -   channel_id does not refer to a valid channel.
                        -   Length of message is over 1000 characters.
    
    Return Value:
        Returns nothing when no error occurs.
    '''

    while (True):
        if (int(datetime.now(timezone.utc).timestamp()) == int(time_sent)):
            break

    store = data_store.get()

    message_react = {'react_id': 1, 'u_ids': [], 'is_this_user_reacted': False}
    message_info = {'message_id': message_id, 'u_id': user_id, 'message': message, 'time_created': time_sent, 'reacts': [message_react], 'is_pinned': False}

    store['messages'].append(message_info)

    idx = store['channels']['channel_id'].index(channel_id)
    store['channels']['messages'][idx].append(message_id)

    tag_users_in_channel_message(user_id, message, channel_id)

    store['users']['messages_sent'][user_id] += 1
    append_user_stat_data_msg(user_id)

    store['messages_exist'] += 1
    append_workspace_stats_msg()

    data_store.set(store)

def message_sendlaterdm_v1(token, dm_id, message, time_sent):
    ''' 
    This function sends a message to a specified channel at a specific time, given a valid token.

    Arguments:
        token       (string)    - Used to check whether the user attempting to send a message is a valid user.
        dm_id       (integer)   - The dm_id which the message will be sent to.
        message     (string)    - The message the user wishes to send to the specified DM.
        time_sent   (integer)   - The time which the message is to be sent at.
    
    Exceptions:
        Access Error    -   Invalid token.
                        -   dm_id is valid and the authorised user is not a member of the DM.
        Input Error     -   dm_id does not refer to a valid DM.
                        -   time_sent is in the past.
                        -   Length of message is over 1000 characters.
    
    Return Value:
        Returns {message_id} when no error occurs.
    '''

    # Check for any errors
    user_id = check_and_get_user_id(token)
    check_dm_id(dm_id)
    check_user_authority_in_dm(user_id, dm_id)
    check_if_message_too_long(message)
    check_time(time_sent)

    # Create a message_id
    message_id = generate_new_message_id()

    send_later = threading.Thread(target=send_msgdm_later_thread, args=(user_id, dm_id, message, time_sent, message_id))
    send_later.start()

    return {
        'message_id': message_id
    }

def send_msgdm_later_thread(user_id, dm_id, message, time_sent, message_id):
    ''' 
    This function is executed as a separate thread, in order to send the message later.

    Arguments:
        user_id     (integer)   - The user_id.
        dm_id       (integer)   - The dm_id which the message will be sent to.
        message     (string)    - The message the user wishes to send to the specified DM.
        time_sent   (integer)   - The time which the message is to be sent at.
    
    Exceptions:
        Access Error    -   Invalid token.
                        -   dm_id is valid and the authorised user is not a member of the DM.
        Input Error     -   dm_id does not refer to a valid DM.
                        -   Length of message is over 1000 characters.
    
    Return Value:
        Returns nothing when no error occurs.
    '''

    while (True):
        if (int(datetime.now(timezone.utc).timestamp()) == int(time_sent)):
            break

    store = data_store.get()

    message_react = {'react_id': 1, 'u_ids': [], 'is_this_user_reacted': False}
    message_info = {'message_id': message_id, 'u_id': user_id, 'message': message, 'time_created': time_sent, 'reacts': [message_react], 'is_pinned': False}

    store['messages'].append(message_info)

    idx = store['dms']['dm_id'].index(dm_id)
    store['dms']['messages'][idx].append(message_id)
    
    tag_users_in_dm_message(user_id, message, dm_id)

    store['users']['messages_sent'][user_id] += 1
    append_user_stat_data_msg(user_id)

    store['messages_exist'] += 1
    append_workspace_stats_msg()    

    data_store.set(store)

def check_channel_id(channel_id):
    ''' 
    This function checks if a channel_id exists.

    Arguments:
        channel_id  (integer)   - The channel_id of the specified channel.
    
    Exceptions:
        Input Error     -   channel_id does not refer to a valid channel.
    
    Return Value:
        Returns nothing when no error occurs.
    '''

    store = data_store.get()

    if channel_id not in store['channels']['channel_id']:
        raise InputError(description="This channel does not exist!")

def check_dm_id(dm_id):
    ''' 
    This function checks if a dm_id exists.

    Arguments:
        dm_id  (integer)   - The dm_id of the specified DM.
    
    Exceptions:
        Input Error     -   dm_id does not refer to a valid DM.
    
    Return Value:
        Returns nothing when no error occurs.
    '''

    store = data_store.get()

    if dm_id not in store['dms']['dm_id']:
        raise InputError(description="This DM does not exist!")

def check_if_message_too_long(message):
    ''' 
    This function checks if a message is too long (>1000 characters).

    Arguments:
        message     (string)   - A message.
    
    Exceptions:
        Input Error     -   Message is greater than 1000 characters.
    
    Return Value:
        Returns nothing when no error occurs.
    '''

    if len(message) > 1000:
        raise InputError(description="Message is too long")

def check_if_message_too_short(message):
    ''' 
    This function checks if a message is too short (<1 character).

    Arguments:
        message     (string)   - A message.
    
    Exceptions:
        Input Error     -   Message is less than 1 character.
    
    Return Value:
        Returns nothing when no error occurs.
    '''

    if len(message) < 1:
        raise InputError(description="Message is too short")

def check_if_message_id_exists_and_get_sender_id(message_id):
    ''' 
    This function checks if a message_id exists, and retrieves the user_id of the user that sent it.

    Arguments:
        message_id  (integer)   - The message_id of the message.
    
    Exceptions:
        Input Error     -   message_id does not exist.
    
    Return Value:
        Returns the user_id of the user that sent it if no error occurs.
    '''

    store = data_store.get()
    for message in store['messages']:
        if message_id == message['message_id']:
            return message['u_id']
    raise InputError(description="Message does not exist")

def get_dm_or_channel_id_of_message(message_id):
    ''' 
    This function retrieves the dm_id and channel_id of a given message_id.

    Arguments:
        message_id  (integer)   - The message_id of the message.
    
    Return Value:
        Returns (dm_id, 'dm') or (channel_id, 'channel') depending if the message belongs to a channel or DM.
    '''

    store = data_store.get()

    # Check in channels if the message belongs there
    for messages_group in store['channels']['messages']:
        if message_id in messages_group:
            idx = store['channels']['messages'].index(messages_group)
            return store['channels']['channel_id'][idx], 'channel'

    # Check in DMs if the message belongs there
    for messages_group in store['dms']['messages']:
        if message_id in messages_group:
            idx = store['dms']['messages'].index(messages_group)
            return store['dms']['dm_id'][idx], 'dm'

def check_if_user_is_owner_of_channel_or_sender_or_global_owner(user_id, channel_id, sender_id):
    ''' 
    This function checks if the user_id is the owner of the channel_id or the sender of the message or global owner.

    Arguments:
        user_id     (integer)   - The user_id of the user making the call.
        channel_id  (integer)   - The channel_id of the specified channel.
        sender_id   (integer)   - The id of the user who sent the message.

    Exceptions:
        Access Error    -   User is not the sender of the message or the user is not an owner of the channel or global owner.
    
    Return Value:
        Returns nothing when no error occurs.
    '''    

    store = data_store.get()
    idx = store['channels']['channel_id'].index(channel_id)

    if user_id == sender_id or user_id in store['channels']['owner_user_id'][idx] or store['users']['is_global_owner'][user_id]: #there are multiple owners, assume its a list
        pass
    else:
        raise AccessError(description="User is not the sender of the message or the user is not an owner of the channel")

def check_if_user_is_owner_of_dm_or_sender(user_id, dm_id, sender_id):
    ''' 
    This function checks if the user_id is the owner of the dm_id or the sender of the message.

    Arguments:
        user_id     (integer)   - The user_id of the user making the call.
        dm_id       (integer)   - The dm_id of the specified DM.
        sender_id   (integer)   - The id of the user who sent the message.

    Exceptions:
        Access Error    -   User is not the sender of the message or the user is not an owner of the DM.
    
    Return Value:
        Returns nothing when no error occurs.
    '''

    store = data_store.get()
    idx = store['dms']['dm_id'].index(dm_id)

    if user_id == sender_id or user_id == store['dms']['owner_user_id'][idx]: #there is one owner for a dm
        pass
    else:
        raise AccessError(description="User is not the sender of the message or the user is not an owner of the DM")

def check_user_authority_in_channel(user_id, channel_id):
    ''' 
    This function checks if the user_id is apart of the channel members.

    Arguments:
        user_id     (integer)   - The user_id of the user making the call.
        channel_id  (integer)   - The channel_id of the specified channel.

    Exceptions:
        Access Error    -   User not a part of the channel members.
    
    Return Value:
        Returns nothing when no error occurs.
    '''

    store = data_store.get()
    idx = store['channels']['channel_id'].index(channel_id)

    if user_id not in store['channels']['all_members'][idx]:
        raise AccessError(description="User not a part of the channel members")

def check_user_authority_in_dm(user_id, dm_id):
    ''' 
    This function checks if the user_id is apart of the DM members.

    Arguments:
        user_id     (integer)   - The user_id of the user making the call.
        dm_id       (integer)   - The dm_id of the specified DM.

    Exceptions:
        Access Error    -   User not a part of the DM members.
    
    Return Value:
        Returns nothing when no error occurs.
    '''
    
    store = data_store.get()
    idx = store['dms']['dm_id'].index(dm_id)

    if user_id not in store['dms']['all_members'][idx]:
        raise AccessError(description="User not a part of the DM members")

def check_time(time_sent):
    ''' 
    This function checks if the time_sent is a valid time.

    Arguments:
        time_sent     (integer)   - The time the user wishes to sent the message.

    Exceptions:
        Input Error    -   Time is in the past.
    
    Return Value:
        Returns nothing when no error occurs.
    '''
    if time_sent < int(datetime.now(timezone.utc).timestamp()):
        raise InputError(description='Time incorrect')

def append_user_stat_data_msg(u_id):

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

    messages_new_stat = {'num_messages_sent': messages_sent, 'time_stamp': time_stamp}
    store['users']['messages_sent_user_data'][u_id].append(messages_new_stat)
    
    involvement_rate = 0
    if (channels_joined + dms_joined + messages_sent) > 0:
        involvement_rate = (channels_joined + dms_joined + messages_sent) / (total_channels + total_dms + total_messages)

    if involvement_rate > 1:
        involvement_rate = 1

    store['users']['involvement_rate'][u_id] = involvement_rate

def append_workspace_stats_msg():
    '''
    This function updates the workspace statitics data once a change is made in the number of messages.

    Arguments:
        u_id (int) - The user id.

    Exceptions:
        No given exceptions
    ''' 
    store = data_store.get()

    messages_exist = store['messages_exist']

    time_stamp = int(datetime.now(timezone.utc).timestamp())

    messages_new_stat = {'num_messages_exist': messages_exist, 'time_stamp': time_stamp}
    store['workspace_stat_messages'].append(messages_new_stat)

    num_users_who_have_joined_at_least_one_channel_or_dm = 0
    num_users = len(store['users']['user_id'])
    for u_id in store['users']['user_id']:
        if store['users']['channels_joined'][u_id] > 0:
            num_users_who_have_joined_at_least_one_channel_or_dm += 1
        elif store['users']['dms_joined'][u_id] > 0:
            num_users_who_have_joined_at_least_one_channel_or_dm += 1

    store['utilization_rate'] = num_users_who_have_joined_at_least_one_channel_or_dm / num_users
