from src.data_store import data_store
from src.error import InputError, AccessError
from src.auth_auth_helpers import check_and_get_user_id
from src.message import message_send_v1
from datetime import datetime, timezone
import threading

import time

def standup_start_v1(token, channel_id, length):

    user_id = check_and_get_user_id(token)
    check_channel_id(channel_id)
    check_user_authority_in_channel(user_id, channel_id)
    check_time_length(length)
    check_channel_has_active_standup(channel_id)

    store = data_store.get()
    store['channels']['is_standup_active'][channel_id] = True
    
    time_finish = int(datetime.now(timezone.utc).timestamp()) + length
    store['channels']['standup_time_finish'][channel_id] = time_finish

    start_standup = threading.Thread(target=when_standup_finishes, args=(token, channel_id, time_finish))
    start_standup.start()

    return {
        'time_finish': time_finish
    }


def when_standup_finishes(token, channel_id, time_finishes):
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
    check_and_get_user_id(token)

    while (True):
        if (int(datetime.now(timezone.utc).timestamp()) == int(time_finishes)):
            break
    
    store = data_store.get()
    store['channels']['is_standup_active'][channel_id] = False
    store['channels']['standup_time_finish'][channel_id] = 0

    standup_messages = store['channels']['standup_messages'][channel_id]
    standup_messages = '\n'.join(standup_messages)
    message_send_v1(token, channel_id, standup_messages)
    store['channels']['standup_messages'][channel_id] = []
    data_store.set(store)

def standup_send_v1(token, channel_id, message):

    user_id = check_and_get_user_id(token)
    check_channel_id(channel_id)
    check_user_authority_in_channel(user_id, channel_id)
    check_channel_does_not_has_active_standup(channel_id)
    check_if_message_too_long(message)
    
    store = data_store.get()
    user_handle = store['users']['user_handles'][user_id]
    store['channels']['standup_messages'][channel_id].append(f'{user_handle}: {message}')

    data_store.set(store)

    return {}

def standup_active_v1(token, channel_id):
    user_id = check_and_get_user_id(token)
    check_channel_id(channel_id)
    check_user_authority_in_channel(user_id, channel_id)

    store = data_store.get()
    if store['channels']['is_standup_active'][channel_id] == False:
        is_active = False
        time_finish = None
    else:
        is_active = True
        time_finish = store['channels']['standup_time_finish'][channel_id]

    return {
        'is_active': is_active,
        'time_finish': time_finish
    }


















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

def check_time_length(length):
    if length < 0:
        raise InputError(description='Time length is negative')

def check_channel_has_active_standup(channel_id):
    store = data_store.get()
    if store['channels']['is_standup_active'][channel_id]:
        raise InputError(description="Channel has active standup")

def check_channel_does_not_has_active_standup(channel_id):
    store = data_store.get()
    if not store['channels']['is_standup_active'][channel_id]:
        raise InputError(description="Channel does not have active standup")

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

