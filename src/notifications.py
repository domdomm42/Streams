from src.data_store import data_store
from src.error import InputError, AccessError
from src.auth_auth_helpers import check_and_get_user_id

def notifications_get_v1(token):

    user_id = check_and_get_user_id(token)
    
    store = data_store.get()
    notifications = store['users']['notifications'][user_id][-1:-21:-1]

    return {'notifications': notifications}

# DON'T ALERT USER IF THEY ARE NOT IN THE CHANNEL
# Assumes that the sender of the message is the owner of the token
def tag_users_in_channel_message(sender_id, message, channel_id):

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

# DON'T ALERT USER IF THEY ARE NOT IN THE DM
def tag_users_in_dm_message(sender_id, message, dm_id):

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

if __name__ == '__main__':
    list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
    print(list[-1:-21:-1])