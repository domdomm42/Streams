from src.data_store import data_store
from src.error import InputError, AccessError
from src.auth_auth_helpers import check_and_get_user_id
from src.auth import auth_register_v1
from src.channels import channels_create_v1
from src.other import print_store_debug
from datetime import datetime, timezone


def message_send_v1(token, channel_id, message):

    user_id = check_and_get_user_id(token)
    check_channel_id(channel_id)
    check_user_authority_in_channel(user_id, channel_id)
    check_if_message_too_long(message)
    check_if_message_too_short(message)

    store = data_store.get()
    
    message_id = 0
    if store['messages'] != []: #MESSAGES IS NOT EMPTY
        message_id = store['messages'][-1]['message_id'] + 1

    time_created = datetime.now().replace(tzinfo=timezone.utc).timestamp()

    message_info = {'message_id': message_id, 'u_id': user_id, 'message': message, 'time_created': time_created}

    store['messages'].append(message_info)

    idx = store['channels']['channel_id'].index(channel_id)
    store['channels']['messages'][idx].append(message_id)
    
    data_store.set(store)

    return {
        'message_id': message_id
    }

def message_edit_v1(token, message_id, message):

    if message == "":

        message_remove_v1(token, message_id)

    else:

        user_id = check_and_get_user_id(token)
        check_if_message_too_long(message)
        sender_id = check_if_message_id_exists_and_get_sender_id(message_id)

        store = data_store.get()
        for msg in store['messages']:
            if msg['message_id'] == message_id:
                message_idx = store['messages'].index(msg)

        dm_or_channel_id_of_message = get_dm_or_channel_id_of_message(message_id)
        if (dm_or_channel_id_of_message[1] == 'channel'): # Message belongs to a channel
            channel_id = dm_or_channel_id_of_message[0]
            check_if_user_is_owner_of_channel_or_sender(user_id, channel_id, sender_id)
            
            store['messages'][message_idx]['message'] = message
            
        else:
            dm_id = dm_or_channel_id_of_message[0]
            check_if_user_is_owner_of_dm_or_sender(user_id, dm_id, sender_id)

            store['messages'][message_idx]['message'] = message

        data_store.set(store)

    return {}
    
def message_remove_v1(token, message_id):
    user_id = check_and_get_user_id(token)
    sender_id = check_if_message_id_exists_and_get_sender_id(message_id)

    store = data_store.get()
    for msg in store['messages']:
        if msg['message_id'] == message_id:
            message_idx = store['messages'].index(msg)

    dm_or_channel_id_of_message = get_dm_or_channel_id_of_message(message_id)
    if (dm_or_channel_id_of_message[1] == 'channel'): # Message belongs to a channel
        channel_id = dm_or_channel_id_of_message[0]
        check_if_user_is_owner_of_channel_or_sender(user_id, channel_id, sender_id)
        
        channel_idx = store['channels']['channel_id'].index(channel_id)

        #print(store['messages'])
        store['messages'].pop(message_idx)
        #print(store['messages'])
        #print(store['channels']['messages'])
        store['channels']['messages'][channel_idx].remove(message_id)
        #print(store['channels']['messages'])
    else:
        dm_id = dm_or_channel_id_of_message[0]
        check_if_user_is_owner_of_dm_or_sender(user_id, dm_id, sender_id)

        dm_idx = store['dms']['dm_id'].index(dm_id)

        store['messages'].pop(message_idx)
        store['dms']['messages'][dm_idx].remove(message_id)

    data_store.set(store)

    return {}

def message_senddm_v1(token, dm_id, message):

    user_id = check_and_get_user_id(token)
    check_channel_id(dm_id)
    check_user_authority_in_dm(user_id, dm_id)
    check_if_message_too_long(message)
    check_if_message_too_short(message)

    store = data_store.get()
    
    message_id = 0
    if store['messages'] != []: #MESSAGES IS NOT EMPTY
        message_id = store['messages'][-1]['message_id'] + 1

    time_created = datetime.now().replace(tzinfo=timezone.utc).timestamp()

    message_info = {'message_id': message_id, 'u_id': user_id, 'message': message, 'time_created': time_created}

    store['messages'].append(message_info)

    idx = store['dms']['dm_id'].index(dm_id)
    store['dms']['messages'][idx].append(dm_id)
    
    data_store.set(store)

    return {
        'message_id': message_id
    }

def check_channel_id(channel_id):
    store = data_store.get()

    if channel_id not in store['channels']['channel_id']:
        raise InputError(description="This channel does not exist!")

def check_if_message_too_long(message):
    if len(message) > 1000:
        raise InputError(description="Messag is too long")

def check_if_message_too_short(message):
    if len(message) < 1:
        raise InputError(description="Message is too short")

def check_if_message_id_exists_and_get_sender_id(message_id):
    store = data_store.get()
    for message in store['messages']:
        if message_id == message['message_id']:
            return message['u_id']
    raise InputError(description="Message does not exist")

def check_if_message_in_channel(message_id):
    store = data_store.get()
    for messages_group in store['channels']['messages']:
        if message_id in messages_group:
            return True
    return False


def get_dm_or_channel_id_of_message(message_id):
    # OWNER OF CHANNEL/DM CAN EDIT MESSAGE
    store = data_store.get()
    #Find where the message_id belongs in
    #Check channels first
    for messages_group in store['channels']['messages']:
        if message_id in messages_group:
            idx = store['channels']['messages'].index(messages_group)
            return store['channels']['channel_id'][idx], 'channel'

    for messages_group in store['dms']['messages']:
        if message_id in messages_group:
            idx = store['dms']['messages'].index(messages_group)
            return store['dms']['dm_id'][idx], 'dm'

    raise InputError(description="Message does not belong in any channel or dm!")

def check_if_user_is_owner_of_channel_or_sender(user_id, channel_id, sender_id):
    
    store = data_store.get()
    idx = store['channels']['channel_id'].index(channel_id)

    if user_id != sender_id or user_id not in store['channels']['owner_user_id'][idx]: #there are multiple owners, assume its a list
        raise AccessError(description="User is not the sender of the message or the user is not an owner of the channel")

def check_if_user_is_owner_of_dm_or_sender(user_id, dm_id, sender_id):
    
    store = data_store.get()
    idx = store['dms']['dm_id'].index(dm_id)

    if user_id != sender_id or user_id != store['dms']['owner_user_id'][idx]: #there is one owner for a dm
        raise AccessError(description="User is not the sender of the message or the user is not an owner of the DM")

def check_user_authority_in_channel(user_id, channel_id):
    store = data_store.get()
    idx = store['channels']['channel_id'].index(channel_id)

    if user_id not in store['channels']['all_members'][idx]:
        raise AccessError(description="User not a part of the channel members")

def check_user_authority_in_dm(user_id, dm_id):
    store = data_store.get()
    idx = store['dms']['dm_id'].index(dm_id)

    if user_id not in store['dms']['all_members'][idx]:
        raise AccessError(description="User not a part of the DM members")

# if __name__ == '__main__':
#     token = auth_register_v1("joe123@gmail.com", "password", "Joe", "Jim")['token']
#     token2 = auth_register_v1("joe1233@gmail.com", "password", "Marry", "Jim")['token']
#     channel_id = channels_create_v1(token, "Funland", True)['channel_id']
#     #print_store_debug()
#     message_id = message_send_v1(token, channel_id, "Yo")['message_id']
#     #print_store_debug()
#     message_remove_v1(token2, message_id)
#     #print_store_debug()