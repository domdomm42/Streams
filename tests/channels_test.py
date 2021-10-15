import pytest
import requests

from src.config import *
from src.other import clear_v1
from src.error import InputError, AccessError
from src.auth import auth_login_v1, auth_register_v1
from src.channels import channels_list_v1, channels_listall_v1, channels_create_v1
from src.channel import channel_join_v1, channel_messages_v1, channel_join_v1, channel_details_v1

BASE_URL = url


''' 
Channels testing documentation
Setup creates the background for each channel list test by registering,
logging, and creating a channel for each user. A private channel for 
user Marry (channel 1, 2, 3) and a public channel for user Joe (channel 0, 1, 3).  
'''

@pytest.fixture
def setup():
    clear_v1()

    login_joe = auth_register_v1('joe123@gmail.com', 'password', 'Joe', 'Smith').get('auth_user_id')
    channels_create_v1(login_joe, 'Joe', False).get('channel_id')

    login_marry = auth_register_v1('marryjoe222@gmail.com', 'passwordM', 'Marry', 'Joe').get('auth_user_id')
    channel_marry = channels_create_v1(login_marry, 'Marry', True).get('channel_id')

    channels_create_v1(login_marry, 'Second_Marry', False).get('channel_id')
    channel_join_v1(login_joe, channel_marry)

    channel_second_joe = channels_create_v1(login_joe, 'Second_Joe', True).get('channel_id')
    channel_join_v1(login_marry, channel_second_joe)

    login_sam = auth_register_v1('sam123@gmail.com', 'passwordJ', 'Sam', 'Smith').get('auth_user_id')
    channels_create_v1(login_sam, 'Sam', True).get('channel_id')
    
    return login_marry

# Simple Listing tests to return all channels created
def test_all_channels(setup):
    assert channels_listall_v1(setup) == {
        'channels': [
        	{
        		'channel_id': 0,
        		'name': 'Joe',
        	},
            {
                'channel_id': 1,
                'name': 'Marry'
            },
            {
                'channel_id': 2,
                'name': 'Second_Marry'
            },
            {
                'channel_id': 3,
        		'name': 'Second_Joe'
            },
            {
                'channel_id': 4,
        		'name': 'Sam'
            }
        ]
    }

# Simple listing tests to return all channels that the given id is a part of
def test_mary_channels(setup):
     assert channels_list_v1(setup) == {
        'channels': [
        	{
        		'channel_id': 1,
        		'name': 'Marry',
        	},
            {   
                'channel_id': 2,
        		'name': 'Second_Marry',
            },
            {
                'channel_id': 3,
        		'name': 'Second_Joe'
            }
        ]
    }

# Test if empty channels in data_store return an empty list inside 
# channels dictionary
def test_empty_channels():
    clear_v1()
    assert channels_list_v1(0) == {'channels': []}
    assert channels_listall_v1(0) == {'channels': []}
    assert channels_list_v1(4) == {'channels': []}
    assert channels_listall_v1(4) == {'channels': []}

# Testing Invalid names for channel creation
def test_empty_name1():
    requests.delete(f'{BASE_URL}/clear/v1')

    channel_creation_name = {"token": "1", "name": "", "is_public": True}

    response_create = requests.post(f'{BASE_URL}/channels/create/v2', json = channel_creation_name)
    response_create_data = response_create.json()
    assert response_create_data['code'] == 400


def test_long_name1():
    requests.delete(f'{BASE_URL}/clear/v1')

    channel_creation_name = {"token": "1", "name": "bigbigbigbigbigbigbigbig", "is_public": True}

    response_create = requests.post(f'{BASE_URL}/channels/create/v2', json = channel_creation_name)
    response_create_data = response_create.json()
    assert response_create_data['code'] == 400


def test_empty_name2():
    requests.delete(f'{BASE_URL}/clear/v1')

    channel_creation_name = {"token": "1", "name": "", "is_public": False}

    response_create = requests.post(f'{BASE_URL}/channels/create/v2', json = channel_creation_name)
    response_create_data = response_create.json()
    assert response_create_data['code'] == 400

def test_long_name2():
    requests.delete(f'{BASE_URL}/clear/v1')

    channel_creation_name = {"token": "1", "name": "bigbigbigbigbigbigbigbig", "is_public": False}

    response_create = requests.post(f'{BASE_URL}/channels/create/v2', json = channel_creation_name)
    response_create_data = response_create.json()
    assert response_create_data['code'] == 400

# # Testing simple channel creation
# def test_new_channel():
#     requests.delete(f'{BASE_URL}/clear/v1')

#     auth_user_id_reg = {"email": "dommm@gmail.com", "password": "limoudom123", "name_first": "oudom", "name_last": "lim"}
#     response_auth_user_id = requests.post(f'{BASE_URL}/auth/register/v2', json = auth_user_id_reg)

#     auth_user_id_info = response_auth_user_id.json()

#     channel_creation_name = {"token": auth_user_id_info["token"], "name": "domserver", "is_public": False}
#     response_create = requests.post(f'{BASE_URL}/channels/create/v2', json = channel_creation_name)

#     response_create_data = response_create.json()
#     assert response_create_data["channel_id"] == 0

    

# Testing Invalid user_ID for channel_create_v1
def test_invalid_id_channel_create_negative():
    requests.delete(f'{BASE_URL}/clear/v1')

    channel_creation_name = {"token": "-1", "name": "bigboy", "is_public": True}

    response_create = requests.post(f'{BASE_URL}/channels/create/v2', json = channel_creation_name)
    response_create_data = response_create.json()
    assert response_create_data['code'] == 403


def test_invalid_id_channel_create_over():
    requests.delete(f'{BASE_URL}/clear/v1')

    channel_creation_name = {"token": "3", "name": "bigboy", "is_public": True}

    response_create = requests.post(f'{BASE_URL}/channels/create/v2', json = channel_creation_name)
    response_create_data = response_create.json()
    assert response_create_data['code'] == 403





        

