from src.data_store import data_store
from src.error import InputError
from src.auth_auth_helpers import check_and_get_user_id
from src.auth import auth_register_v1
from src.channels import channels_create_v1
from src.message import message_send_v1
import re
import urllib.request
from PIL import Image
from src.config import *


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
            user_profile_pic = store['users']['profile_img_url'][user_id]
            users.append({'u_id': user_id, 'email': user_email, 
                            'name_first': user_name_first, 
                            'name_last': user_name_last, 
                            'handle_str': user_handle_str, 
                            'profile_img_url': user_profile_pic})

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
    u_id = store['users']['user_id'][u_id]
    user_email = store['users']['emails'][u_id]
    user_name_first = store['users']['first_names'][u_id]
    user_name_last = store['users']['last_names'][u_id]
    user_handle_str = store['users']['user_handles'][u_id]
    user_profile_pic = store['users']['profile_img_url'][u_id]
    user = {'u_id': u_id, 'email': user_email, 
                            'name_first': user_name_first, 
                            'name_last': user_name_last, 
                            'handle_str': user_handle_str,
                            'profile_img_url': user_profile_pic}

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












# IT3

# Deal with the user's photo, upload, crop and save
def user_profile_uploadphoto_v1(token, img_url, x_start, y_start, x_end, y_end):
    
    '''
    Given a URL of an image on the internet.
    Crops the image within bounds (x_start, y_start) and (x_end, y_end). 
    Position (0,0) is the top left. 
    The URL needs to be a non-https URL (it should just have "http://" in the URL.)
    '''
    

    # check valid token
    u_id = check_and_get_user_id(token)
    store = data_store.get()

    # check the url is start with https://
    http_check(img_url)

    # check photo type
    check_type(img_url)
    
    # imageDown
    # Save the im in temporary folder undre scr called 'static'
    urllib.request.urlretrieve(img_url, 'src/static/tmp.jpg')

    

    
    im = Image.open('src/static/tmp.jpg')
    
    # Get the width and height of the im
    width, height = im.size
    
    
    
    # check the start and end is valid
    if x_start >= x_end or y_start >= y_end or x_start >= width or x_end > width or y_start >= height or y_end > height:
        raise InputError(description='Invalid Size')

    # check the min of x/y start/end
    if x_start < 0 or x_end <= 0 or y_start < 0 or y_end <= 0:
        raise InputError(description='Invalid Size')


    im = im.crop((x_start, y_start, x_end, y_end))

    # Crop the im
    crop_image(x_start, y_start, x_end, y_end)


    # Save the im in temporary folder undre scr called 'static'
    im.save(f'src/static/{u_id}.jpg')


    # store im into profile_img_url
    store['users']['profile_img_url'][u_id] = f'http://localhost:{port}/src/static/{u_id}.jpg'


    # Store the data
    data_store.set(store)



    return {}



# Show the stat of the current user
def user_stats_v1(token):
    

    '''
    Fetches the required statistics about this user's use of UNSW Streams.
    return with Dictionary of shape {
        channels_joined: [{num_channels_joined, time_stamp}],
        dms_joined: [{num_dms_joined, time_stamp}], 
        messages_sent: [{num_messages_sent, time_stamp}], 
        involvement_rate 
    }
    
    '''
    
    # Get the u_id from token
    u_id = check_and_get_user_id(token)

    store = data_store.get()


    # return the dict of user_stats
    user_stats = {
        'channels_joined': store['users']['channels_user_data'][u_id],
        'dms_joined': store['users']['dms_user_data'][u_id],
        'messages_sent': store['users']['messages_sent_user_data'][u_id],
        'involvement_rate': store['users']['involvement_rate'][u_id]
    }

    return {'user_stats': user_stats}
    

# Show the stats of all users
def users_stats_v1(token):
    
    '''
    Fetches the required statistics about the use(all users) of UNSW Streams.
    return with Dictionary of shape {
        channels_exist: [{num_channels_exist, time_stamp}], 
        dms_exist: [{num_dms_exist, time_stamp}], 
        messages_exist: [{num_messages_exist, time_stamp}], 
        utilization_rate 
    }
    '''

    
    # Get the u_id from token
    check_and_get_user_id(token)

    store = data_store.get()

    # return the dict of workspace_stats
    workspace_stats = {
        'channels_exist': store['workspace_stat_channels'],
        'dms_exist': store['workspace_stat_dms'],
        'messages_exist': store['workspace_stat_messages'],
        'utilization_rate': store['utilization_rate']
    }

    
    return {'workspace_stats': workspace_stats}




######Helper Function##########


# Check if the url is valid
def http_check(img_url):
    r = re.match("http://", img_url)
    if r == None:
        raise InputError(description='Invalid Url')


# Check if the type is not jpg/jpeg
def check_type(img_url):
    resp = urllib.request.urlopen(img_url)
    img = Image.open(resp)
    if img.format != 'JPEG':
        raise InputError(description='Invalid Type')




# Crop the image from the static folder
def crop_image(x_start, y_start, x_end, y_end):
    
    # unnecessary img_url?

    im = Image.open('src/static/tmp.jpg')

    cropped = im.crop((x_start, y_start, x_end, y_end))

    cropped.save('src/static/{u_id}.jpg')

    return 'src/static/{u_id}.jpg'


#########################

# IT2

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
        raise InputError(description='This email is already registered!')


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

if __name__ == '__main__':
    token = auth_register_v1("jimjoe@gmail.com", "password", "Jim", "Joe")['token']
    print(users_stats_v1(token))
    channels_create_v1(token, 'Jim', False)
    print(users_stats_v1(token))
    message_send_v1(token, 0, "Hi there!")
    print(users_stats_v1(token))
    










