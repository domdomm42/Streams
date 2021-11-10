from src.data_store import data_store
from src.error import InputError, AccessError
from src.auth_auth_helpers import check_and_get_user_id
from src.message import check_if_message_id_exists_and_get_sender_id
from datetime import datetime, timezone
import re
import urllib.request
import sys
from PIL import Image


def user_profile_sethandle_v1(token, handle_str):
    '''
    Update the authorised user's handle (i.e. display name)

    Arguments:
        token(string)   - use to identify users
        handle_str(string)  - the name user want to replace

    Exceptions:
        400 Error:
            InputError('Invalid input') - length of handle_str is not between 3 and 20 characters inclusive
                                        - handle_str contains characters that are not alphanumeric
                                        - the handle is already used by another user
    
    Return value:
        return {}
    '''
    user_id = check_and_get_user_id(token)
    
    check_len(handle_str)
    check_alphanumeric(handle_str)
    check_duplicate(handle_str)

    store = data_store.get()

    store['users']['user_handles'][user_id] = handle_str
    
    data_store.set(store)
    return {}


def user_all_v1(token):
    '''
    Returns a list of all users and their associated details.

    Arguments:
        token(string)   - use to identify users

    Exceptions:
        No given exception
    Return value:
        return {users} - Returns a list of all users and their details
    '''
    

    store = data_store.get()
    user_id = check_and_get_user_id(token)
    
    users = []
    for user_id in store['users']['user_id']:
        if store['users']['removed_user'][user_id] == False:
            
            user_email = store['users']['emails'][user_id]
            user_name_first = store['users']['first_names'][user_id]
            user_name_last = store['users']['last_names'][user_id]
            user_handle_str = store['users']['user_handles'][user_id]
            users.append({'u_id': user_id, 'email': user_email, 
                            'name_first': user_name_first, 
                            'name_last': user_name_last, 
                            'handle_str': user_handle_str})

    data_store.set(store)

    return {'users': users}


# List of all valid users
def user_profile_v1(token, u_id):
    
    '''
    Returns information on the user_id, email, first name, last name and handle

    Arguments:
        token(string)   - use to identify users
        u_id            - user id

    Exceptions:
        InputError - Raised when u_id does not refer to a valid user
    Return value:
        return {users} - Returns a list of all users and their details
    '''

    store = data_store.get()
    _ = check_and_get_user_id(token)
    
    check_invalid_u_id(u_id)
    user = []
    u_id = store['users']['user_id'][u_id]
    user_email = store['users']['emails'][u_id]
    user_name_first = store['users']['first_names'][u_id]
    user_name_last = store['users']['last_names'][u_id]
    user_handle_str = store['users']['user_handles'][u_id]
    user.append({'user_id': u_id, 'email': user_email, 
                            'first_name': user_name_first, 
                            'last_name': user_name_last, 
                            'handle_str': user_handle_str})

    return {'user': user}


# Update name
def user_profile_setname_v1(token, name_first, name_last):
    '''
    Update an authorised users first and last name

    Arguments:
        token(string)   - use to identify users
        name_first      - string
        name_last       - string

    Exceptions:
        InputError - length of name_first is not between 1 and 50 characters inclusive
                   - length of name_last is not between 1 and 50 characters inclusive

    Return value:
        return {}
    '''
    
    user_id = check_and_get_user_id(token)
    check_name_first_len(name_first)
    check_name_last_len(name_last)

    store = data_store.get()

    store['users']['first_names'][user_id] = name_first
    store['users']['last_names'][user_id] = name_last

    data_store.set(store)

    return {}


# Update email
def user_profile_setemail_v1(token, email):
    '''
    Update the authorised user's email address

    Arguments:
        token(string)   - use to identify users
        email           - string

    Exceptions:
        InputError - email entered is not a valid email
                   - email address is already being used by another user

    Return value:
        return {}
    '''
    

    user_id = check_and_get_user_id(token)
    check_invalid_emails(email)

    store = data_store.get()

    store['users']['emails'][user_id] = email

    data_store.set(store)

    return {}

#def user_profile_uploadphoto_v1(token, img_url, x_start, y_start, x_end, y_end ):
#    #check valid token
#    u_id = check_and_get_user_id(token)
#    
#    #check the url is start with https://
#    http_check(img_url)
#    #check photo type
#    check_type(img_url)
#    imageDown(img_url, u_id)
#    #check the start and end is valid
#    check_valid_startend(img_url, x_start, y_start, x_end, y_end, u_id)
#    
#    
#    
#    crop_image(img_url, x_start, y_start, x_end, y_end, u_id)
#    serve_image()
#    return {}
#
def user_stats_v1(token):
    #check valid token
    u_id = check_and_get_user_id(token)



    store = data_store.get()
    num_channel_joined = 0
    num_dm_joined = 0
    num_messages_sent = 0
    num_channels = len(store['channels']['channel_id'])
    num_dms = len(store['dms']['dm_id'])
    num_messages = len(store['messages'])
    for channel_id in store['channels']['channel_id']:
        if u_id in store['channels']['all_members'][channel_id]:
            num_channel_joined = num_channel_joined + 1
    for dm_id in store['dms']['dm_id']:
        if u_id in store['dms']['all_members'][dm_id]:
            num_dm_joined = num_dm_joined + 1
    for message in store['messages']:
        if check_if_message_id_exists_and_get_sender_id(message['message_id']) == u_id:
            num_messages_sent = num_messages_sent + 1 
    time_stamp = datetime.now().replace(tzinfo=timezone.utc).timestamp()
    channels_joined = store['users']['channels_joined'][u_id]
    dms_joined = store['users']['dms_joined'][u_id]
    messages_sent = store['users']['message_sent'][u_id]
    channel_new_stat = {'num_channels_joined': num_channel_joined, 'time_stamp': time_stamp}
    dms_new_stat = {'num_dms_joined': num_dm_joined, 'time_stamp': time_stamp}
    messages_new_stat = {'num_messages_sent': num_messages_sent, 'time_stamp': time_stamp}
    channels_joined.append(channel_new_stat)
    dms_joined.append(dms_new_stat)
    messages_sent.append(messages_new_stat)
    if (num_channels + num_dms + num_messages) > 0:
        involvement_rate = (num_channel_joined + num_dm_joined + num_messages_sent)/(num_channels + num_dms + num_messages)

    if involvement_rate > 1:
        involvement_rate = 1
    
    user_stats = {
        'channels_joined': channels_joined,
        'dms_joined': dms_joined,
        'messages_sent': messages_sent,
        'involvement_rate': involvement_rate
    }





    return {'user_stats': user_stats}

def users_stats_v1(token):
    u_id = check_and_get_user_id(token)
    store = data_store.get()
    num_channels_exist = len(store['channels']['channel_id'])
    num_dms_exist = len(store['dms']['dm_id'])
    num_messages_exist = len(store['messages'])
    
    user_list = []
    for user_id in store['users']['user_id']:
        for channel_id in store['channels']['channel_id']:
            if user_id in store['channels']['all_members'][channel_id]:
                user_list.append(user_id)
        for dm_id in store['dms']['dm_id']:
            if user_id in store['dms']['dm_id'][dm_id]:
                user_list.append(user_id)
    
    user_list.set()
    time_stamp = datetime.now().replace(tzinfo=timezone.utc).timestamp()
    active_user = len(user_list)
    num_user = len(store['users']['user_id'])
    utilization_rate = active_user/num_user
    channels_exist = store['channels_exist']
    dms_exist = store['dms_exist']
    messages_exist = store['messages_exist']
    channel_new_stat = {'num_channels_exist': num_channels_exist, 'time_stamp': time_stamp}
    dms_new_stat = {'num_dms_exist': num_dms_exist, 'time_stamp': time_stamp}
    messages_new_stat = {'num_messages_sent': num_messages_exist, 'time_stamp': time_stamp}
    channels_exist.append(channel_new_stat)
    dms_exist.append(dms_new_stat)
    messages_exist.append(messages_new_stat)
    workspace_stats = {
        'channels_exist': channels_exist,
        'dms_exist': dms_exist,
        'messages_exist': messages_exist,
        'utilization_rate': utilization_rate
    }


    return {'workspace_stats': workspace_stats}


#
#
#
#
#
#
#
#
#
#
#
#
#
#
######Helper Function##########    
#
#
#
#def http_check(img_url):
#    r = re.match("http://", img_url)
#    if r == None:
#        raise InputError(description='Invalid Url')
#
#def check_valid_startend(img_url, x_start, y_start, x_end, y_end, u_id):
#    im = Image.open(f'image/{u_id}.jpg')
#    width, height = im.size
#    if x_start > x_end or y_start > y_end or x_start > width or x_end > width or y_start > height or y_end > height:
#        raise InputError(description='Invalid Size')
#
#
#
#
#
##
#def check_type(img_url):
#    resp = request.urlopen(img_url)
#    img = Image.open(resp)
#    if img.format != 'JPEG':
#        raise InputError(description='Invalid Type')
##
#def imageDown(img_url):
#    urllib.request.urlretrieve(img_url, image/u_id.jpg)
##
#def crop_image(img_url, x_start, y_start, x_end, y_end):
#    im = Image.open(f'image/{u_id}.jpg')
#    cropped = im.crop((x_start, y_start, x_end, y_end))
#    cropped.save(f'image/{u_id}.jpg')
#
#
#def serve_image():









def check_len(handle_str):
    '''
    check the handle is length correct
    it return InputError if it is invalid
    '''
    if len(handle_str) < 3 or len(handle_str) > 20:
        raise InputError(description='Invalid User Name')
    
def check_alphanumeric(handle_str):
    '''
    check teh handle is only contain number and char
    it takes handle and return Input Error if it is invalid
    '''
    if handle_str.isalnum() == False:
        raise InputError(description='Invalid User Name')

def check_duplicate(handle_str):
    '''
    check handle is been used or not
    if it is , return InputError
    '''
    store = data_store.get()
    for name in store['users']['user_handles']:
        if name == handle_str:
            raise InputError(description='This name has been used!')

def check_name_first_len(first_name):
    '''
    Checks length of first name

    Arguments:
        first_name           - string

    Exceptions:
        InputError - Invalid User name

    Return value:
        No Return Value
    '''
    if len(first_name) < 1 or len(first_name) > 50:
        raise InputError(description='Invalid First Name')

def check_name_last_len(last_name):
    '''
    Checks length of first name

    Arguments:
        first_name           - string

    Exceptions:
        InputError - Invalid User name

    Return value:
        No Return Value
    '''
    if len(last_name) < 1 or len(last_name) > 50:
        raise InputError(description='Invalid Last Name')

def check_invalid_emails(email):
    '''
    Check for validity of emails

    Arguments:
        email(string)

    Exceptions:
        InputError - email already registered
    Return value:
        No return value
    '''

    store = data_store.get()
    regex = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$'

    if re.fullmatch(regex, email) and email not in store['users']['emails']:
        pass
    else:
        raise InputError(description = 'This email is already registered!')

def check_invalid_u_id(u_id):
    '''
    Check for validity of user_id

    Arguments:
        u_id(strings)

    Exceptions:
        InputError - user_id does not exist
    Return value:
        No return value
    '''
    store = data_store.get()
    if u_id not in store['users']['user_id']:
        raise InputError(description='This user does not exist!')













