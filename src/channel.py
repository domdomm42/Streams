from src.data_store import data_store
from src.error import InputError, AccessError


def channel_invite_v1(auth_user_id, channel_id, u_id):
    store = data_store.get()

    # Check
    check_invalid_channel_id(channel_id)
    check_invalid_u_id(u_id, channel_id)

    check_member_u_id(channel_id, u_id)

    check_autorised_id(auth_user_id, channel_id)

    # Store
    store['channels']['all_members'][channel_id].append(u_id)

    data_store.set(store)
    return {

    }


def channel_details_v1(auth_user_id, channel_id):
    store = data_store.get()

    # check input
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
    owner_details.append({'u_id': owners, 'email': user_email,
                          'name_first': user_first_name, 'name_last': user_last_name, 'handle_str': user_handles})

    members_details = []

    for member_users_id in members:
        user_email = store['users']['emails'][member_users_id]
        user_first_name = store['users']['first_names'][member_users_id]
        user_last_name = store['users']['last_names'][member_users_id]
        user_handles = store['users']['user_handles'][member_users_id]
        members_details.append({'u_id': member_users_id, 'email': user_email,
                                'name_first': user_first_name, 'name_last': user_last_name, 'handle_str': user_handles})

    return {
        'name': name,
        'is_public': public,
        'owner_members': owner_details,
        'all_members': members_details

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
    store = data_store.get()
    check_channel_id(channel_id)
    check_exist_member(auth_user_id, channel_id)
    check_channel_status(channel_id, auth_user_id)

    store['channels']['all_members'][channel_id].append(auth_user_id)
    data_store.set(store)

    return {
    }


# check the channel id is valid
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


# check user is a member or not
def check_exist_member(auth_user_id, channel_id):
    store = data_store.get()

    for user in store['channels']['all_members'][channel_id]:

        if user == auth_user_id:
            raise InputError('You are a member already!')

    pass


# check the channel status(private or not)
def check_channel_status(channel_id, auth_user_id):
    store = data_store.get()
    if store['channels']['is_public'][channel_id] == True:
        pass
    else:
        raise AccessError('This is private channel, permission denied!')
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
    if u_id >= len(store['users']['user_handles']):
        raise InputError('This user does not exist!')


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
def check_autorised_id(auth_user_id, channel_id):
    store = data_store.get()

    for user in store['channels']['all_members'][channel_id]:
        if user == auth_user_id:
            return

    raise AccessError('Permission denied!')