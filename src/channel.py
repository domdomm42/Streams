import pytest
#from data_store import data_store
from src.data_store import data_store
from src.error import InputError, AccessError

def channel_invite_v1(auth_user_id, channel_id, u_id):
    store = data_store.get()
    # Check
    check_invalid_channel_id(channel_id)
    check_invalid_u_id(u_id,channel_id)

    check_member_u_id(channel_id, u_id)

    check_autorised_id(auth_user_id,channel_id)

    # Store

    store['channels']['all_members'][channel_id].append(u_id)


    data_store.set(store)
    return {

    }


# store['channels']['channel_id']['name'],
#
#
# all_members.append(auth_user_id)

def channel_details_v1(auth_user_id, channel_id):
    return {
        'name': 'Hayden',
        'owner_members': [
            {
                'u_id': 1,
                'email': 'example@gmail.com',
                'name_first': 'Hayden',
                'name_last': 'Jacobs',
                'handle_str': 'haydenjacobs',
            }
        ],
        'all_members': [
            {
                'u_id': 1,
                'email': 'example@gmail.com',
                'name_first': 'Hayden',
                'name_last': 'Jacobs',
                #'handle_str': 'haydenjacobs', store = data_store.get()
    }
    ],
    }

def channel_messages_v1(auth_user_id, channel_id, start):

    store = data_store.get()
    # Check
    check_invalid_channel_id(channel_id)
    check_invalid_start(channel_id, start)

    check_autorised_id(auth_user_id,channel_id)

    #list_message = [1,2,3,4]


    # Loop
    messages_list = []
    place = start
    # store['channels']['messages'].append[list_message]
    # for message in store['channels']['messages'][channel_id]:
    #     messages_list.append(message)
    #     place += 1
    #     if place == 50:
    #         break
    # if place < 50:
    #     place = -1

    return {
        'messages': messages_list,
        'start': start,
        'end': place
    }

def channel_join_v1(auth_user_id, channel_id):
        return {
        }

# InputError
# Check invalid channel_id
def check_invalid_channel_id(channel_id):
    
    store = data_store.get()
    i = 0
    
    for items in store['channels']['channel_name']:
        
        if i == channel_id:
            return
            
        i += 1
    raise InputError('Invalid channel id')

    
    

# Check invalid u_id
def check_invalid_u_id(u_id, channel_id):
	
    store = data_store.get()

    if u_id not in store['channels']['all_members'][channel_id]:
            
        raise InputError('User not apart of the channel')

# Check member u_id
def check_member_u_id(channel_id, u_id):
    
    store = data_store.get()

    if u_id in store['channels']['all_members'][channel_id]:
        raise InputError('User not apart of channel')
    else:
        pass
 



# Check start
def check_invalid_start(channel_id, start):
    
    store = data_store.get()
    
    
    # if start <= len(store['channels']['messages'][channel_id]):
    #     pass

    cnt = 0
    for item in store['channels']['all_members'][channel_id]:
        
        if start == cnt:
            return
        cnt += 1

    raise AccessError('Permission dinined!')

# AccessError
# Check authorised
def check_autorised_id(auth_user_id,channel_id):
    store = data_store.get()
   
    
    for user in store['channels']['all_members'][channel_id]:
        if user == auth_user_id:
            return
            
    
    raise AccessError('Permission denied!')


