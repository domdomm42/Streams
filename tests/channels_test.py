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

    requests.delete(f'{BASE_URL}/clear/v1')

    # Create user Joe Smith
    user_info = {'email': 'joe123@gmail.com', 'password': 'password', 'name_first': 'Joe', 'name_last': 'Smith'}
    joe_token = requests.post(f'{BASE_URL}/auth/register/v2', json = user_info).json()['token']

    # Joe Smith creates a Private channel called 'Joe'
    channel_info = {'token': joe_token, 'name': 'Joe', 'is_public': False}
    requests.post(f'{BASE_URL}/channels/create/v2', json = channel_info).json()['channel_id']

    # Create user Marry Joe
    user_info = {'email': 'marryjoe222@gmail.com', 'password': 'passwordM', 'name_first': 'Marry', 'name_last': 'Joe'}
    marry_token = requests.post(f'{BASE_URL}/auth/register/v2', json = user_info).json()['token']

    # Marry Joe creates a Public channel called 'Marry'
    channel_info = {'token': marry_token, 'name': 'Marry', 'is_public': True}
    marry_channel_id = requests.post(f'{BASE_URL}/channels/create/v2', json = channel_info).json()['channel_id']

    # Marry Joe creates Private channel called 'Second_Marry'
    channel_info = {'token': marry_token, 'name': 'Second_Marry', 'is_public': True}
    requests.post(f'{BASE_URL}/channels/create/v2', json = channel_info).json()['channel_id']

    # Joe Smith joins channel 'Marry'
    channel_join_info = {'token': joe_token, 'channel_id': marry_channel_id}
    requests.post(f'{BASE_URL}/channel/join/v2', json = channel_join_info)

    # Joe Smith creates Public channel called 'Second_Joe'
    channel_info = {'token': joe_token, 'name': 'Second_Joe', 'is_public': True}
    second_joe_channel_id = requests.post(f'{BASE_URL}/channels/create/v2', json = channel_info).json()['channel_id']   
    
    # Marry Joe joins channel 'Second_Joe'
    channel_join_info = {'token': marry_token, 'channel_id': second_joe_channel_id}
    requests.post(f'{BASE_URL}/channel/join/v2', json = channel_join_info)

    # Create user Sam Smith
    user_info = {'email': 'sam123@gmail.com', 'password': 'passwordJ', 'name_first': 'Marry', 'name_last': 'Joe'}
    sam_token = requests.post(f'{BASE_URL}/auth/register/v2', json = user_info).json()['token']

    # Sam Smith creates Public called called 'Sam'
    channel_info = {'token': sam_token, 'name': 'Sam', 'is_public': True}
    requests.post(f'{BASE_URL}/channels/create/v2', json = channel_info)

    return {'token': marry_token}


# Simple Listing tests to return all channels created
def test_all_channels(setup):
    
    marry_token = setup
    response = requests.get(f'{BASE_URL}/channels/listall/v2', params = marry_token).json()
    assert response == {
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
    marry_token = setup
    response = requests.get(f'{BASE_URL}/channels/list/v2', params = marry_token).json()
    assert response == {
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

    requests.delete(f'{BASE_URL}/clear/v1')

    user_info = {'email': 'joe123@gmail.com', 'password': 'password', 'name_first': 'Joe', 'name_last': 'Smith'}
    joe_token = {'token': requests.post(f'{BASE_URL}/auth/register/v2', json = user_info).json()['token']}

    response = requests.get(f'{BASE_URL}/channels/list/v2', params = joe_token).json()
    assert response == {'channels': []}

    response = requests.get(f'{BASE_URL}/channels/listall/v2', params = joe_token).json()
    assert response == {'channels': []}

def test_invalid_token():
    requests.delete(f'{BASE_URL}/clear/v1')

    info = {'token': '-1'}
    response = requests.get(f'{BASE_URL}/channels/list/v2', params = info).json()
    assert response['code'] == 403

# Testing Invalid names for channel creation
def test_empty_name1():

    requests.delete(f'{BASE_URL}/clear/v1')

    user_info = {"email": "marryjoe222@gmail.com", "password": "password", "name_first": "Marry", "name_last": "Joe"}
    response = requests.post(f'{BASE_URL}/auth/register/v2', json = user_info)
    token = response.json()['token']
    channel_creation_name = {"token": token, "name": "", "is_public": True}

    response_create = requests.post(f'{BASE_URL}/channels/create/v2', json = channel_creation_name)
    response_create_data = response_create.json()
    assert response_create_data['code'] == 400







        

