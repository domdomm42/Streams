import pytest
import requests
from src.config import *
from src.users import *

BASE_URL = url
INPUT_ERROR = 400

@pytest.fixture
def setup():
    
    requests.delete(f'{BASE_URL}/clear/v1')
    
    # register for joe
    user_joe_info_reg = {"email": "joe123@gmail.com", "password": "password", "name_first": "Joe", "name_last": "Smith"}
    user_joe_info_login = {"email": "joe123@gmail.com", "password": "password"}
    requests.post(f'{BASE_URL}/auth/register/v2', json=user_joe_info_reg)
    
    # register for marry
    user_marry_info_reg = {"email": "marryjoe222@gmail.com", "password": "passwordM", "name_first": "Marry",
                           "name_last": "Joe"}
    user_marry_info_login = {"email": "marryjoe222@gmail.com", "password": "passwordM"}
    requests.post(f'{BASE_URL}/auth/register/v2', json=user_marry_info_reg)
    
    # log them in
    response_log_joe = requests.post(f'{BASE_URL}/auth/login/v2', json=user_joe_info_login)
    response_log_marry = requests.post(f'{BASE_URL}/auth/login/v2', json=user_marry_info_login)
    response_log_joe = response_log_joe.json()
    response_log_marry = response_log_marry.json()
    return response_log_joe, response_log_marry

# Test for user all and user profile

# Test invalid u id
def test_user_u_id_invalid(setup):
    
    # Load data from setup
    response_log_joe, _ = setup

    # Input invalid u id "100"
    user_profile_info = {"token": response_log_joe['token'], "u_id": 100}

    response = requests.get(f'{BASE_URL}user/profile/v1', params=user_profile_info)
    response_data = response.json()
    
    # Raise InputError, u id does not refer to a valid user
    assert response_data['code'] == INPUT_ERROR

# Test valid u id
def test_valid_u_id(setup):
    
    # Load data from setup
    response_log_joe, _ = setup
    
    # Input valid u id
    user_profile_info = {"token": response_log_joe['token'], "u_id": 0}
    response = requests.get(f'{BASE_URL}user/profile/v1', params=user_profile_info)
    response_data = response.json()
    
    # Match the corresponding data
    assert response_data['user'] == [{
        'email': 'joe123@gmail.com',
        'first_name': 'Joe',
        'last_name': 'Smith',
        'handle_str': 'joesmith',
        'user_id': 0,
    }]

# Test valid user all
def test_user_all_output(setup):
    
    # Load data from setup
    response_log_joe, _ = setup
    user_all_info = {"token": response_log_joe["token"]}
    response = requests.get(f'{BASE_URL}users/all/v1', params=user_all_info)
    response_data = response.json()
    print(response_data)
        
    # Match the corresponding data
    assert response_data == {
        'users':
        [
            {'email': 'joe123@gmail.com',
            'handle_str': 'joesmith',
            'name_first': 'Joe',
            'name_last': 'Smith',
            'u_id': 0},
            {'email': 'marryjoe222@gmail.com',
            'handle_str': 'marryjoe',
            'name_first': 'Marry',
            'name_last': 'Joe',
            'u_id': 1},

        ]
    }

# Test valid user profile
def test_user_profile_output(setup):
    
    # Load data from setup
    response_log_joe, _ = setup

    user_profile_info = {"token": response_log_joe['token'], "u_id": 1}

    response = requests.get(f'{BASE_URL}user/profile/v1', params=user_profile_info)
    response_data = response.json()
    
    # Match the corresponding data
    assert response_data['user'] == [{
        'email': 'marryjoe222@gmail.com',
        'first_name': 'Marry',
        'last_name': 'Joe',
        'handle_str': 'marryjoe',
        'user_id': 1}]

# Test for name

# Test invalid short first name
def test_user_name_first_too_short(setup):
    
    # Load data from setup
    response_log_joe, _ = setup

    # Last name is valid, last name out of range (1-50 characters)
    setname_info = {"token": response_log_joe["token"], "first_names": "", "last_names": "a"}
    response = requests.put(f'{BASE_URL}user/profile/setname/v1', json=setname_info)
    response_data = response.json()

    # Raise InputError, length of first name is not between 1 and 50
    assert response_data['code'] == INPUT_ERROR

# Test invalid short last name
def test_user_name_last_too_short(setup):
    
    # Load data from setup
    response_log_joe, _ = setup

    # First name is valid, last name out of range (1-50 characters)
    setname_info = {"token": response_log_joe["token"], "first_names": "a", "last_names": ""}
    response = requests.put(f'{BASE_URL}user/profile/setname/v1', json=setname_info)
    response_data = response.json()
    
    # Raise InputError, length of last name is not between 1 and 50    
    assert response_data['code'] == INPUT_ERROR

# Test invalid long first name
def test_user_name_first_too_long(setup):
    
    # Load data from setup
    response_log_joe, _ = setup
    
    # Last name is valid, first name out of range (1-50 characters)
    setname_info = {"token": response_log_joe["token"],
                    "first_names": "abcdefghijklmnopqrstuvwxyz1531abcdefghijklmnopqrstuvwxyz", "last_names": "a"}
    response = requests.put(f'{BASE_URL}user/profile/setname/v1', json=setname_info)
    response_data = response.json()
    
    # Raise InputError, length of first name is not between 1 and 50
    assert response_data['code'] == INPUT_ERROR

# Test invalid long last name
def test_user_name_last_too_long(setup):
    
    # Load data from setup
    response_log_joe, _ = setup  
    
    # First name is valid, last name out of range (1-50 characters)
    setname_info = {"token": response_log_joe["token"], "first_names": 'a',
                    "last_names": "abcdefghijklmnopqrstuvwxyz1531abcdefghijklmnopqrstuvwxyz"}
    response = requests.put(f'{BASE_URL}user/profile/setname/v1', json=setname_info)
    response_data = response.json()

    # Raise InputError, length of last name is not between 1 and 50
    assert response_data['code'] == INPUT_ERROR

# Test name duplications
def test_user_name_duplication(setup):
   
    # Load data from setup
    response_log_joe, response_log_marry = setup
    
    # Two same names "a" "Smith",  there are no restrictions
    setname_info1 = {"token": response_log_joe["token"], "first_names": "a", "last_names": "Smith"}
    setname_info2 = {"token": response_log_marry["token"], "first_names": "a", "last_names": "Smith"}

    requests.put(f'{BASE_URL}user/profile/setname/v1', json=setname_info1)
    response = requests.put(f'{BASE_URL}user/profile/setname/v1', json=setname_info2)

    response_data = response.json()
    assert response_data == {}

# Test for valid first and last names
def test_valid_name(setup):
    
    # Load data from setup
    response_log_joe, _ = setup
    
    # Input valid first name "a" and valid last "b"
    setname_info = {"token": response_log_joe['token'], "first_names": "a", "last_names": "b"}
    requests.put(f'{BASE_URL}user/profile/setname/v1', json=setname_info)
    user_profile_info = {"token": response_log_joe['token'], "u_id": 0}
    response = requests.get(f'{BASE_URL}user/profile/v1', params=user_profile_info)
    response_data = response.json()
    
    # Match the corresponding data
    assert response_data['user'] == [{
        'email': 'joe123@gmail.com',
        'first_name': 'a',
        'last_name': 'b',
        'handle_str': 'joesmith',
        'user_id': 0,
    }]

# Test for email

#Test email duplication
def test_user_email_duplication(setup):
    
    # Load data from setup
    response_log_joe, response_log_marry = setup
    
    # Input two same emails
    setemail_info1 = {"token": response_log_joe["token"], "emails": "kobebryant24881@gmail.com"}
    setemail_info2 = {"token": response_log_marry["token"], "emails": "kobebryant24881@gmail.com"}

    requests.put(f'{BASE_URL}user/profile/setemail/v1', json=setemail_info1)
    response = requests.put(f'{BASE_URL}user/profile/setemail/v1', json=setemail_info2)

    response_data = response.json()
    
    # Raise InputError, email is already being used by others
    assert response_data['code'] == INPUT_ERROR

# Test two similar email, one lowercase the other uppercase
def test_user_email_duplication_invalid_capital(setup):
    
    # Load data from setup
    response_log_joe, response_log_marry = setup
    
    # One lowercase the other uppercase
    setemail_info1 = {"token": response_log_joe["token"], "emails": "aaa@gmail.com"}
    setemail_info2 = {"token": response_log_marry["token"], "emails": "AAA@gmail.com"}

    requests.put(f'{BASE_URL}user/profile/setemail/v1', json=setemail_info1)
    response = requests.put(f'{BASE_URL}user/profile/setemail/v1', json=setemail_info2)

    response_data = response.json()
    assert response_data == {}

# Test invalid email
def test_user_email_invalid(setup):
    
    # Load data from setup
    response_log_joe, _ = setup
    
    # Input "abcde" is invalid 
    setemail_info = {"token": response_log_joe["token"], "emails": "abcde"}
    response = requests.put(f'{BASE_URL}user/profile/setemail/v1', json=setemail_info)
    response_data = response.json()
    
    # Raise InputError, email is not valid
    assert response_data['code'] == INPUT_ERROR

# Test valid user email
def test_valid_email(setup):

    # Load data from setup
    response_log_joe, _ = setup
    setemail_info = {"token": response_log_joe['token'], "emails": "joe123@gmail.com"}
    requests.put(f'{BASE_URL}user/profile/setemail/v1', json=setemail_info)
    user_profile_info = {"token": response_log_joe['token'], "u_id": 0}
    response = requests.get(f'{BASE_URL}user/profile/v1', params=user_profile_info)
    response_data = response.json()
    
    # Match the corresponding data
    assert response_data['user'] == [{
        'email': 'joe123@gmail.com',
        'first_name': 'Joe',
        'last_name': 'Smith',
        'handle_str': 'joesmith',
        'user_id': 0,
    }]

# Test for handle

# Test invalid short handle
def test_user_handle_too_short(setup):
    
    # Load data from setup
    response_log_joe, _ = setup
    
    
    # Input invalid short handle 'a', out of range (3-20)
    sethandle_info = {"token": response_log_joe['token'], "handle_str": "a"}
    response = requests.put(f'{BASE_URL}user/profile/sethandle/v1', json=sethandle_info)
    response_data = response.json()
    
    # Raise InputError, length of handle_str is not between 3 and 20
    assert response_data['code'] == INPUT_ERROR

# Test invalid long handle
def test_user_handle_too_long(setup):
    
    # Load data from setup
    response_log_joe, _ = setup
    

    # Input invalid long handle 'longlonglonglonglonglong', out of range (3-20)
    sethandle_info = {"token": response_log_joe['token'], "handle_str": "longlonglonglonglonglong"}
    response = requests.put(f'{BASE_URL}user/profile/sethandle/v1', json=sethandle_info)
    response_data = response.json()
    
    # Raise InputError, length of handle_str is not between 3 and 20    
    assert response_data['code'] == INPUT_ERROR

# Test not alphanumeric handle
def test_user_handle_contains_not_alnum(setup):
    
    # Load data from setup
    response_log_joe, _ = setup
    
    # Input invalid not alphanumeric handle 'my_name!'
    sethandle_info = {"token": response_log_joe['token'], "handle_str": "my_name!"}
    response = requests.put(f'{BASE_URL}user/profile/sethandle/v1', json=sethandle_info)
    response_data = response.json()

    # Raise InputError, handle_str contains characters that are not alphanumeric
    assert response_data['code'] == INPUT_ERROR

# Test handle duplication
def test_user_handle_duplicate(setup):
    
    # Load data from setup
    response_log_joe, response_log_marry = setup

    # Input two same handles
    sethandle_info_joe = {"token": response_log_joe['token'], "handle_str": "KobeBryant"}
    requests.put(f'{BASE_URL}user/profile/sethandle/v1', json=sethandle_info_joe)
    sethandle_info_marry = {"token": response_log_marry['token'], "handle_str": "KobeBryant"}
    response = requests.put(f'{BASE_URL}user/profile/sethandle/v1', json=sethandle_info_marry)
    response_data = response.json()
    
    # Raise InputError, the handle is already being used by others
    assert response_data['code'] == INPUT_ERROR

# Test similar handle, one lowercase the other uppcase
def test_user_handle_duplicate_capital(setup):
    
    # Load data from setup
    response_log_joe, response_log_marry = setup

    # Two handles, one lowercase, the other uppcase
    sethandle_info_joe = {"token": response_log_joe['token'], "handle_str": "aaa"}
    requests.put(f'{BASE_URL}user/profile/sethandle/v1', json=sethandle_info_joe)
    sethandle_info_marry = {"token": response_log_marry['token'], "handle_str": "AAA"}
    response = requests.put(f'{BASE_URL}user/profile/sethandle/v1', json=sethandle_info_marry)
    response_data = response.json()
    assert response_data == {}

# Test valid handle
def test_valid_handle(setup):
    
    # Load data from setup
    response_log_joe, _ = setup
    
    # Input valid user handle
    sethandle_info = {"token": response_log_joe['token'], "handle_str": "KobeBryant"}
    requests.put(f'{BASE_URL}user/profile/sethandle/v1', json=sethandle_info)
    user_profile_info = {"token": response_log_joe['token'], "u_id": 0}
    response = requests.get(f'{BASE_URL}user/profile/v1', params=user_profile_info)
    response_data = response.json()
    
    # Match the corresponding data
    assert response_data['user'] == [{
        'email': 'joe123@gmail.com',
        'first_name': 'Joe',
        'last_name': 'Smith',
        'handle_str': 'KobeBryant',
        'user_id': 0,
    }]
    
    requests.delete(f'{BASE_URL}/clear/v1')


def test_successful_users_all():
    requests.delete(f'{BASE_URL}/clear/v1')
    user_woody_reg = {"email": "sheriff.woody@andysroom.com", "password": "qazwsx!!", "name_first": "sheriff", "name_last": "woody"}
    user_buzz_reg = {"email": "buzz.lightyear@starcommand.com", "password": "qazwsx@@", "name_first":  "buzz", "name_last": "lightyear"}
    user_woody_log_info = {"email": "sheriff.woody@andysroom.com", "password": "qazwsx!!"}

    requests.post(f'{BASE_URL}/auth/register/v2', json=user_woody_reg)
    requests.post(f'{BASE_URL}/auth/register/v2', json=user_buzz_reg)
    user_woody = requests.post(f'{BASE_URL}/auth/login/v2', json=user_woody_log_info)
    user_woody = user_woody.json()
    user_all_info = {"token": user_woody["token"]}
    response = requests.get(f'{BASE_URL}users/all/v1', params=user_all_info)
    
    response_data = response.json() 
    assert response_data == {
        'users': [{'email': 'sheriff.woody@andysroom.com',
            'handle_str': 'sheriffwoody',
            'name_first': 'sheriff',
            'name_last': 'woody',
            'u_id': 0},
            {'email': 'buzz.lightyear@starcommand.com',
            'handle_str': 'buzzlightyear',
            'name_first': 'buzz',
            'name_last':'lightyear',
            'u_id': 1}]
    }






def test_upload_invalid_http(setup):
    response_log_joe, _ = setup
    photo_info = {
        "token": response_log_joe['token'],
        "img_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSdq7PHvMwR6eqzZsCnjd-b7On4Z0BeWGNmpQ&usqp=CAU",
        "x_start": 9, 
        "y_start": 9, 
        "x_end": 99, 
        "y_end": 99 
    }
   
    response = requests.post(f'{BASE_URL}user/profile/uploadphoto/v1', json=photo_info)
    response_data = response.json()
    assert response_data['code'] == 400

def test_upload_invalid_start_end_x(setup):
    response_log_joe, _ = setup
    photo_info = {
        "token": response_log_joe['token'],
        "img_url": "http://cgi.cse.unsw.edu.au/~jas/home/pics/jas.jpg",
        "x_start": 39, 
        "y_start": 10, 
        "x_end": 1, 
        "y_end": 100 
    }


    response = requests.post(f'{BASE_URL}user/profile/uploadphoto/v1', json=photo_info)
    response_data = response.json()
    assert response_data['code'] == 400


def test_upload_invalid_start_end_y(setup):
    response_log_joe, _ = setup
    photo_info = {
        "token": response_log_joe['token'],
        "img_url": "http://cgi.cse.unsw.edu.au/~jas/home/pics/jas.jpg",
        "x_start": 9, 
        "y_start": 39, 
        "x_end": 19, 
        "y_end": 9 
    }


    
   
    response = requests.post(f'{BASE_URL}user/profile/uploadphoto/v1', json=photo_info)
    response_data = response.json()
    assert response_data['code'] == 400









def test_upload_out_of_ranges_x(setup):
    response_log_joe, _ = setup
    
    # 159 * 200
    photo_info = {
        "token": response_log_joe['token'],
        "img_url": "http://cgi.cse.unsw.edu.au/~jas/home/pics/jas.jpg",
        "x_start": 1, 
        "y_start": 1, 
        "x_end": 999, 
        "y_end": 99
    }
    response = requests.post(f'{BASE_URL}user/profile/uploadphoto/v1', json=photo_info)
    response_data = response.json()
    assert response_data['code'] == 400



def test_upload_out_of_ranges_y(setup):
    response_log_joe, _ = setup
    
    # 159 * 200
    photo_info = {
        "token": response_log_joe['token'],
        "img_url": "http://cgi.cse.unsw.edu.au/~jas/home/pics/jas.jpg",
        "x_start": 1, 
        "y_start": 1, 
        "x_end": 99, 
        "y_end": 999
    }
    response = requests.post(f'{BASE_URL}user/profile/uploadphoto/v1', json=photo_info)
    response_data = response.json()
    assert response_data['code'] == 400

def test_upload_not_jpg(setup):
    response_log_joe, _ = setup
    
    # 159 * 200
    photo_info = {
        "token": response_log_joe['token'],
        "img_url": "http://www.cse.unsw.edu.au/~richardb/index_files/RichardBuckland-200.png",
        "x_start": 10, 
        "y_start": 10, 
        "x_end": 90, 
        "y_end": 90
    }
    response = requests.post(f'{BASE_URL}user/profile/uploadphoto/v1', json=photo_info)
    response_data = response.json()
    assert response_data['code'] == 400


# def test_upload_valid(setup):
#     response_log_joe, _ = setup
    
#     # 100 * 100
#     photo_info = {
#         "token": response_log_joe['token'],
#         "img_url": "http://cgi.cse.unsw.edu.au/~jas/home/pics/jas.jpg",
#         "x_start": 10, 
#         "y_start": 10, 
#         "x_end": 90, 
#         "y_end": 90
#     }
#     response = requests.post(f'{BASE_URL}user/profile/uploadphoto/v1', json=photo_info)
#     response_data = response.json()

#     assert response_data == {}







# def test_user_stats(setup):
#     response_log_joe, _ = setup
#     user_all_info = {"token": response_log_joe["token"]}
#     response = requests.get(f'{BASE_URL}user/stats/v1', params=user_all_info)
#     store = data_store.get()

#     u_id = check_and_get_user_id(response_log_joe["token"])
    
#     channels_joined = store['users']['channels_joined'][u_id]
#     dms_joined = store['users']['dms_joined'][u_id]
#     messages_sent = store['users']['message_sent'][u_id]
    
    
#     if (num_channels + num_dms + num_messages) > 0:
#         involvement_rate = (num_channel_joined + num_dm_joined + num_messages_sent)/(num_channels + num_dms + num_messages)

#     if involvement_rate > 1:
#         involvement_rate = 1

#     user_stats = {
#         'channels_joined': channels_joined,
#         'dms_joined': dms_joined,
#         'messages_sent': messages_sent,
#         'involvement_rate': involvement_rate
#     }
    
    
    
    
    
    
    
#     response_data = response.json()
#     assert response_data == {'user_stats': user_stats}

# def test_users_stats(setup):
#     response_log_joe, _ = setup
#     response = requests.get(f'{BASE_URL}users/stats/v1', params=response_log_joe['token'])
#     response_data = response.json()
#     user_profile_info = {"token": response_log_joe['token'], "u_id": 0}

#     store = data_store.get()
#     #u_id = check_and_get_user_id(token)
#     #utilization_rate = active_user/num_user
#     channels_exist = store['channels_exist']
#     dms_exist = store['dms_exist']
#     messages_exist = store['messages_exist']

#     assert response_data == {
#         'channels_exist': channels_exist,
#         'dms_exist': dms_exist,
#         'messages_exist': messages_exist,
#         'utilization_rate': utilization_rate
#     }




