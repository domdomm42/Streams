from src.data_store import data_store
from src.error import InputError, AccessError
from src.auth_auth_helpers import check_and_get_user_id
from src.message import message_send_v1
from src.channels import channels_create_v1
from src.auth import auth_register_v1


def channel_invite_v1(token, channel_id, u_id):
    """
        Given a user with ID u_id to join a channel with ID channel_id.
        
        Arguments:
            auth_user_id (integer)    - use to identify users
            channel_id (integer)    - use to identify channels
                    u_id(integer)       - use to identify users

        Exceptions:

            InputError('Invalid input')  - Occurs when channel_id does
            not refer to a valid channel.

            AccessError('Permission denied!') - Occurs when channel_id
            is valid and the authorised user is not a member of the channel

        Return Value: {}
    """
    auth_user_id = check_and_get_user_id(token)

    store = data_store.get()

    check_invalid_channel_id(channel_id)
    check_autorised_id(auth_user_id, channel_id)
    check_invalid_u_id(u_id)
    check_member_u_id(channel_id, u_id)
    

    store['channels']['all_members'][channel_id].append(u_id)

    data_store.set(store)
    return {
    }


def channel_details_v1(token, channel_id):
    """
    Given a channel with ID channel_id that the authorised 
    user is a member of, provide basic details about the channel.
    
    Methods: GET

    Arguments:
        token(string)   - use to identify users
        channel_id (integer)    - use to identify channels
      
    Exceptions:
        400 Error:
            InputError('Invalid input')  - Occurs when channel_id does 
            not refer to a valid channel.
        403 Error:
            AccessError('Permission denied!') - Occurs when channel_id 
            is valid and the authorised user is not a member of the channel
      
    Return Value:
        Returns dictionary:
                {
                    name (string)
                    is_public (boolean)
                    owner_member :
                    {
                        emails (string)
                        first_name (string)
                        last_name (string)
                        user_handles (string)

                    }
                    all_members :
                    {
                        emails (string)
                        first_name (string)
                        last_name (string)
                        user_handles (string)

                    }
    
                }
        on member of this channel access this channel's details
        """
    store = data_store.get()
    user_id = check_and_get_user_id(token)
    #channel_id does not refer to a valid channel
    check_channel_id(channel_id)
    #channel_id is valid and the authorised user is not a member of the channel
    check_authority(user_id, channel_id)

    name = store['channels']['channel_name'][channel_id]
    public = store['channels']['is_public'][channel_id]
    owners = store['channels']['owner_user_id'][channel_id]

    members = store['channels']['all_members'][channel_id]

    owner_details = []
    for owner_member_id in owners:
        user_email = store['users']['emails'][owner_member_id]
        user_first_name = store['users']['first_names'][owner_member_id]
        user_last_name = store['users']['last_names'][owner_member_id]
        user_handles = store['users']['user_handles'][owner_member_id]
        owner_details.append({'u_id': owner_member_id, 'email': user_email,
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

def channel_messages_v1(token, channel_id, start):
    """
        Given a channel with channel_id that the authorised user is a member of ,
        return up to 50 messages between index of  start and end.

        Arguments:
            auth_user_id (integer)    - use to identify users
            channel_id (integer)    - use to identify channels
                    start(integer)       - use to identify the index of new messages

        Exceptions:

            InputError('Invalid input')  - Occurs when channel_id does
            not refer to a valid channel.

            AccessError('Permission denied!') - Occurs when channel_id
            is valid and the authorised user is not a member of the channel

        Return Value: {
            message,
            start,
            end
        }
        """
    
    auth_user_id = check_and_get_user_id(token)

    check_invalid_channel_id(channel_id)
    check_invalid_start(channel_id, start)
    check_autorised_id(auth_user_id, channel_id)

    store = data_store.get()
    messages = []

    end = start + 50
    # get the 50 messages
    for idx in range(start, start + 51):
        try: 
            idx = store['channels']['messages'][channel_id][-1 - idx]
        except IndexError:
            end = -1
            break

        messages.append(get_message(idx))


    return {
        'messages': messages,
        'start': start,
        'end': end,
    }


def channel_join_v1(token, channel_id):
    """
    Given a channel_id of a channel that the authorised user can join,
    adds them to that channel.

    Method: POST

    Arguments:
        token(string)           - use to identify users
        channel_id (integer)    - use to identify channels
         ...

    Exceptions:
        400 Error:
            InputError('Invalid input')  - Occurs when channel_id does
            not refer to a valid channel.
        
            InputError('You are a member already!')  - Occurs when
            the authorised user is already a member of the channel.
        403 Error:
            AccessError('This is private channel, permission denied!') - Occurs when
            channel_id refers to a channel that is private and the authorised user
            is not already a channel member and is not a global owner.
            
    Return Value:
         This function return empty dictionary.
    """
    store = data_store.get()
    user_id = check_and_get_user_id(token)
    #check channel_id does not refer to a valid channel
    check_channel_id(channel_id)
    # check the authorised user is already a member of the channel
    check_exist_member(user_id, channel_id)
    #check channel_id refers to a channel that is private and the authorised user is not already a channel member and is not a global owner
    check_channel_status(channel_id, user_id)

    store['channels']['all_members'][channel_id].append(user_id)
    data_store.set(store)

    return {
    }

def channel_leave_v1(token, channel_id):
    '''
    Given a channel with ID channel_id that the authorised user is a member of, 
    remove them as a member of the channel. Their messages should remain in the channel. 
    If the only channel owner leaves, the channel will remain.

    Methods: POST
    Arguments:
        token(string)           - use to identify users
        channel_id (integer)    - use to identify channels

    Exceptions:
        400 Error:
            InputError('Invalid input')  - Occurs when channel_id does
            not refer to a valid channel.
        403 Error:
            AccessError('Permission denied!') - Occurs when channel_id
            is valid and the authorised user is not a member of the channel
    Return value:
        return {}

    '''
    store = data_store.get()
    user_id = check_and_get_user_id(token)
    check_channel_id(channel_id)
    check_authority(user_id, channel_id)
    store['channels']['all_members'][channel_id].remove(user_id)
    if user_id in store['channels']['owner_user_id'][channel_id]:
        store['channels']['owner_user_id'][channel_id].remove(user_id)
    data_store.set(store)
    return {

    }

def channel_addowner_v1(token, channel_id, u_id ):
    '''
    Make user with user id u_id an owner of the channel.

    Methods: POST
    Arguments:
        token(string)           - use to identify users
        channel_id (integer)    - use to identify channels
        u_id(integer)           - use to identify users
    
    Exceptions:
        400 Error:
            InputError - channel_id does not refer to a valid channel
                         u_id does not refer to a valid user
                         u_id refers to a user who is not a member of the channel
                         u_id refers to a user who is already an owner of the channel
        403 Error:
            AccessError - channel_id is valid and the authorised user does not have owner permissions in the channel

    Return value:
        return {}      

    '''


    user_id = check_and_get_user_id(token)
    #check channel_id does not refer to a valid channe
    check_channel_id(channel_id)
    #check u_id does not refer to a valid user
    check_invalid_u_id(user_id)
    check_invalid_u_id(u_id)
    #check u_id refers to a user who is not a member of the channel
    check_members(u_id, channel_id)
    #check u_id refers to a user who is already an owner of the channel
    check_owner(channel_id, u_id)
    #check channel_id is valid and the authorised user does not have owner permissions in the channel
    check_owner_permission(channel_id, user_id)

    store = data_store.get()
    store['channels']['owner_user_id'][channel_id].append(u_id)
    
    data_store.set(store)
    return {

    }


def channel_removeowner_v1(token, channel_id, u_id):

    '''
    Remove user with user id u_id as an owner of the channel.

    Methods: POST
    Arguments:
        token(string)           - use to identify users
        channel_id (integer)    - use to identify channels
        u_id(integer)           - use to identify users
    
    Exceptions:
        400 Error:
            InputError - hannel_id does not refer to a valid channel
                         u_id does not refer to a valid user
                         u_id refers to a user who is not an owner of the channel
                         u_id refers to a user who is currently the only owner of the channel 
        403 Error:
            AccessError - channel_id is valid and the authorised user does not have owner permissions in the channel

    Return value:
        return {}    
    '''

    store = data_store.get()
    user_id = check_and_get_user_id(token)
    #channel_id does not refer to a valid channel
    check_channel_id(channel_id)
    #u_id does not refer to a valid user
    check_invalid_u_id(user_id)
    check_invalid_u_id(u_id)
    #u_id refers to a user who is not an owner of the channel
    check_not_owner(u_id, channel_id)
    #check owner permssion
    check_owner_permission(channel_id, user_id)
    #check last owner
    if store['channels']['owner_user_id'][channel_id][-1] == store['channels']['owner_user_id'][channel_id][0]:
        raise InputError(description='User is last owner of this channel')

    
    store['channels']['owner_user_id'][channel_id].remove(u_id)
    
    data_store.set(store)
    return {

    }


def check_owner(channel_id, u_id):
    '''
    check user is owner or not
    '''
    store = data_store.get()
    if u_id in store['channels']['owner_user_id'][channel_id]:
        raise InputError(description='User is an owner already')
    else:
        pass

def check_owner_permission(channel_id, user_id):
    '''
    check user is owner or not
    '''
    store = data_store.get()
    if user_id in store['channels']['owner_user_id'][channel_id]:
        pass
    else:
        raise AccessError(description='Permission denied')

def check_not_owner(u_id, channel_id):
    '''
    check user is owner or not
    '''
    store = data_store.get()
    if u_id in store['channels']['owner_user_id'][channel_id]:
        pass
    else:
        raise InputError(description='User is not an owner')


# check the channel id is valid
def check_channel_id(channel_id):
    '''
    check the channel is valid or not
    '''
    store = data_store.get()
    i = 0

    if int(channel_id) < 0 :
        raise AccessError(description='Invalid Id')
    for _ in store['channels']['channel_name']:


        if i == channel_id:
            return

        i += 1
    raise InputError(description='Invalid input')


def check_authority(auth_user_id, channel_id):
    '''
    check user is member or not
    '''
    store = data_store.get()

    for user in store['channels']['all_members'][channel_id]:
        if user == auth_user_id:
            return

    raise AccessError(description='Permission denied!')

def check_members(auth_user_id, channel_id):
    '''
    check user is member or not
    '''
    store = data_store.get()

    for user in store['channels']['all_members'][channel_id]:
        if user == auth_user_id:
            return

    raise InputError(description='User is not in channel')


# check user is a member or not
def check_exist_member(auth_user_id, channel_id):
    '''
    check user is member or not
    '''
    store = data_store.get()

    for user in store['channels']['all_members'][channel_id]:

        if user == auth_user_id:
            raise InputError(description='You are a member already!')

    pass


# check the channel status(private or not)
def check_channel_status(channel_id, auth_user_id):

    '''
    check channel join status
    '''

    store = data_store.get()
    if store['channels']['is_public'][channel_id] == True:
        pass
    else:
        if auth_user_id not in store['channels']['all_members'][channel_id] and store['users']['is_global_owner'][auth_user_id] == False:
            raise AccessError(description="User is not authorised to join channel")

    # elif store['channels']['is_public'][channel_id] == False:
    #     i = 0
    #     for _ in store['users']['is_global_owner']:
    #         if i == auth_user_id and store['users']['is_global_owner'][i] == True:
    #             return
    #         i = i + 1
        
        
        
        #raise AccessError('This is private channel, permission denied!')


# InputError
# Check invalid channel_id
def check_invalid_channel_id(channel_id):
    '''
    This function checks whether the given channel_id is valid

    Arguments:
        channel_id(int) 

    Exceptions:
        InputError - Raised when the given channel ID does not exist
    Return Value:
        No return value
    ''' 

    store = data_store.get()
    if channel_id not in store['channels']['channel_id']:
        raise InputError(description='Channel ID does not exist')


# Check invalid u_id
def check_invalid_u_id(u_id):
    '''
    This function checks whether the given u_id is valid

    Arguments:
        u_id(int) - user_id

    Exceptions:
        InputError - Raised when user is not in database(user don't exist)
    Return Value:
        No return value
    ''' 


    store = data_store.get()
    if int(u_id) >= len(store['users']['user_handles']):
        raise InputError(description='This user does not exist!')


# Check member u_id
def check_member_u_id(channel_id, u_id):
    '''
    This function checks whether the start is of the message is valid, it cannot be greater than the total
    number of messages in the channel

    Arguments:
        channel_id(int) 
        u_id(int) - user_id

    Exceptions:
        InputError - Raised when user is already apart of the channel
    Return Value:
        No return value
    ''' 

    store = data_store.get()

    if u_id in store['channels']['all_members'][channel_id]:
        raise InputError('User already apart of channel')
    else:
        pass


# Check start
def check_invalid_start(channel_id, start):
    '''
    This function checks whether the start is of the message is valid, it cannot be greater than the total
    number of messages in the channel

    Arguments:
        channel_id(int) 
        start(int) - start of message

    Exceptions:
        InputError - Raised when start is greater than total number of messages in the chanel
    Return Value:
        No return value
    ''' 

    store = data_store.get()
    no_msgs_in_channel = len(store['channels']['messages'][channel_id])
    if start >= no_msgs_in_channel:
        raise InputError(description='Start is greater than the total number of messages in the channel')


# AccessError
# Check authorised
def check_autorised_id(auth_user_id, channel_id):
    '''
    Checks if user is in the channel

    Arguments:
        auth_user_id - id of the user
        channel_id   - id of the channel you want data from

    Exceptions:
        Access Error: Raised when user is not in the channel
    Return Value:
        No Return Value
    ''' 

    store = data_store.get()

    if auth_user_id not in store['channels']['all_members'][channel_id]:
        raise AccessError(description='Permission denied!')
    
def get_message(message_id):
    '''
    This function takes message_id and returns the message associated with message_id

    Arguments:
        message_id(int) - id of message you want to access

    Exceptions:
        No given exceptions
    Return Value:
       msg - message associated with message_id
    ''' 

    store = data_store.get()
    for msg in store['messages']:
        if msg['message_id'] == message_id:
            return msg

# if __name__ == '__main__':
#     token = auth_register_v1('abc1531@gmail.com', 'password', 'abc', '123')['token']
#     channel_id = channels_create_v1(token, 'abc', True)['channel_id']
#     for i in range(0, 75):
#         message_send_v1(token, channel_id, "Hello" + str(i))

#     print(channel_messages_v1(token, channel_id, 40))