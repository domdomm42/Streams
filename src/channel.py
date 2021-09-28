from src.data_store import data_store
from src.error import InputError, AccessError




def channel_invite_v1(auth_user_id, channel_id, u_id):
    return {
    }

def channel_details_v1(auth_user_id, channel_id):
    store = data_store.get()

    #check input
    check_channel_id(channel_id)
    check_authority(auth_user_id, channel_id)
    name = store['channels']['channel_name'][channel_id]
    public = store['channels']['is_public'][channel_id]
    owners = store['chaneels']['owner_user_id'][channel_id]
    members = store['channels']['all_members'][channels_id]
    
    return {name, public, owners, members
    
        
    }

def channel_messages_v1(auth_user_id, channel_id, start):
    return {
        'messages': [
            {
                'message_id': 1,
                'u_id': 1,
                'message': 'Hello world',
                'time_created': 1582426789,
            }
        ],
        'start': 0,
        'end': 50,
    }

def channel_join_v1(auth_user_id, channel_id):
    store = data_store.get()
    check_channel_id(channel_id)
    check_exist_member(auth_user_id, channel_id)
    check_channel_status(channel_id, auth_user_id)
    
    store['channels']['all_members'][channel_id].append(auth_user_id)
    data_store.set(store)

    return {
    }

#check the channel id is valid
def check_channel_id(channel_id):
    store = data_store.get()
    i = 0
    for element in store['channels']['channel_name']:
        if i == channel_id:
            pass
            return
        i += 1
    raise InputError('Invalid input')

def check_authority(auth_user_id, channel_id):
    store = data_store.get()
    for user in store['channels']['all_members'][channel_id]:
        if user == auth_user_id:
            pass
            return
    
    raise AccessError('Permission denied!')
            

#check user is a member or not
def check_exist_member(auth_user_id, channel_id):
    store = data_store.get()
    for user in store['channels']['all_members'][channel_id]:  
        if user == auth_user_id:
            raise InputError('You are a member already!')
        
    pass

#check the channel status(private or not)
def check_channel_status(channel_id, auth_user_id):
    store = data_store.get()
    if store['channels']['is_public'][channel_id] == True:
        pass
    else:
        raise AccessError('This is private channel, permission denied!')
        
    

