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
    owners = store['channels']['owner_user_id'][channel_id]
    
    
    members = store['channels']['all_members'][channel_id]
    
    owner_details = []
    
    
    user_email = store['users']['emails'][owners]
    user_first_name = store['users']['first_names'][owners]
    user_last_name = store['users']['last_names'][owners]
    user_handles = store['users']['user_handles'][owners]
    owner_details.append({'u_id' : owners, 'email' : user_email, 
    'name_first' : user_first_name, 'name_last' : user_last_name, 'handle_str' : user_handles})

    members_details = []


    for member_users_id in members:
        user_email = store['users']['emails'][member_users_id]
        user_first_name = store['users']['first_names'][member_users_id]
        user_last_name = store['users']['last_names'][member_users_id]
        user_handles = store['users']['user_handles'][member_users_id]
        members_details.append({'u_id' : member_users_id, 'email' : user_email, 
        'name_first' : user_first_name, 'name_last' : user_last_name, 'handle_str' : user_handles})




    return {
        'name': name,
        'is_public': public,
        'owner_members': owner_details,
        'all_members' : members_details

        
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
            return
            
        i += 1
    raise InputError('Invalid input')

def check_authority(auth_user_id, channel_id):
    store = data_store.get()
   
    
    for user in store['channels']['all_members'][channel_id]:
        if user == auth_user_id:
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

