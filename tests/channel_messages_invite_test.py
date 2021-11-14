import pytest
import requests
from src.config import *
from datetime import datetime, timezone

BASE_URL = url
INPUT_ERROR = 400
ACCESS_ERROR = 403

@pytest.fixture
def setup():
    requests.delete(f'{BASE_URL}/clear/v1')

    # Create user Joe Smith
    user_info = {"email": "joe123@gmail.com", "password": "delicious23", "name_first": "Joe", "name_last": "Smith"}
    response = requests.post(f'{BASE_URL}/auth/register/v2', json = user_info)
    joe_smith_data = response.json()

    # Joe Smith creates a Private channel named "Joe's Reading Club"
    channel_info = {"token": joe_smith_data['token'], "name": "Joe's Reading Club", "is_public": False}
    response = requests.post(f'{BASE_URL}/channels/create/v2', json = channel_info)
    joes_funland_data = response.json()

    # Create user Marry Mae
    user_info = {"email": "marrymae@gmail.com", "password": "cats1010", "name_first": "Marry", "name_last": "Mae"}
    response = requests.post(f'{BASE_URL}/auth/register/v2', json = user_info)
    marry_mae_data = response.json()

    return joe_smith_data, joes_funland_data, marry_mae_data

def test_invalid_token(setup):

    # Marry Mae logs out, which invalidates her token
    joe_smith_data, joes_funland_data, marry_mae_data = setup
    user_info_logout = {'token': marry_mae_data['token']} 
    requests.post(f'{BASE_URL}/auth/logout/v1', json = user_info_logout)

    # Attempt to use invalidated token to invite users
    channel_invite_info = {'token': marry_mae_data['token'], 'channel_id': joes_funland_data['channel_id'], 'u_id': joe_smith_data['auth_user_id']}
    response = requests.post(f'{BASE_URL}/channel/invite/v2', json = channel_invite_info).json()
    assert response['code'] == ACCESS_ERROR

def test_invalid_channel(setup):

    joe_smith_data, _, marry_mae_data = setup

    # Joe Smith attempts to invite to a channel that does not exist
    channel_invite_info = {'token': joe_smith_data['token'], 'channel_id': 10, 'u_id': marry_mae_data['auth_user_id']}
    response = requests.post(f'{BASE_URL}/channel/invite/v2', json = channel_invite_info)
    response_data = response.json()
    assert response_data['code'] == INPUT_ERROR

def test_invalid_u_id(setup):

    joe_smith_data, joes_funland_data, _ = setup

    # Joe Smith attempts to invite a user that does not exist
    channel_invite_info = {'token': joe_smith_data['token'], 'channel_id': joes_funland_data['channel_id'], 'u_id': 20}
    response = requests.post(f'{BASE_URL}/channel/invite/v2', json = channel_invite_info)
    response_data = response.json()
    assert response_data['code'] == INPUT_ERROR

def test_u_id_already_channel_member(setup):

    joe_smith_data, joes_funland_data, marry_mae_data = setup

    # Joe Smith attempts to invite a user who is already a part of the channel
    channel_invite_info = {'token': joe_smith_data['token'], 'channel_id': joes_funland_data['channel_id'], 'u_id': marry_mae_data['auth_user_id']}
    requests.post(f'{BASE_URL}/channel/invite/v2', json = channel_invite_info)
    response = requests.post(f'{BASE_URL}/channel/invite/v2', json = channel_invite_info)
    response_data = response.json()
    assert response_data['code'] == INPUT_ERROR

def test_auth_user_not_apart_of_channel(setup):

    joe_smith_data, joes_funland_data, marry_mae_data = setup

    # Marry Mae attempts to invite a user into a channel that she is not a part of
    channel_invite_info = {'token': marry_mae_data['token'], 'channel_id': joes_funland_data['channel_id'], 'u_id': joe_smith_data['auth_user_id']}
    response = requests.post(f'{BASE_URL}/channel/invite/v2', json = channel_invite_info)
    response_data = response.json()
    assert response_data['code'] == ACCESS_ERROR

def test_send_valid_messages(setup):

    joe_smith_data, joes_funland_data, _ = setup

    joe_smith_token = joe_smith_data['token']
    joes_funland_channel_id = joes_funland_data['channel_id']

    # Joe sends a message to his channel, saying "Hi everyone!"
    message_send_input = {"token": joe_smith_token, "channel_id": joes_funland_channel_id, "message": "Hi everyone!"}
    requests.post(f'{BASE_URL}/message/send/v1', json = message_send_input)
    message_0_time = int(datetime.now(timezone.utc).timestamp())

    # Joe sends another message to his channel, saying "Please pick your favourite book, ready for Monday 2pm."
    message_send_input = {"token": joe_smith_token, "channel_id": joes_funland_channel_id, "message": "Please pick your favourite book, ready for Monday 2pm."}
    requests.post(f'{BASE_URL}/message/send/v1', json = message_send_input)
    message_1_time = int(datetime.now(timezone.utc).timestamp())

    # Joe wants to view all the channel's messages
    channel_messages_input = {'token': joe_smith_token, 'channel_id': joes_funland_channel_id, 'start': 0}
    response = requests.get(f'{BASE_URL}/channel/messages/v2', params = channel_messages_input).json()
    
    assert response == {
        'messages': [
            {
                'message_id': 1, 
                'u_id': 0, 
                'message': 'Please pick your favourite book, ready for Monday 2pm.', 
                'time_created': message_1_time,
                'reacts': [
                    {
                        'react_id': 1,
                        'u_ids': [],
                        'is_this_user_reacted': False
                    }
                ],
                'is_pinned': False
            }, 
            {
                'message_id': 0, 
                'u_id': 0, 
                'message': 'Hi everyone!', 
                'time_created': message_0_time,
                'reacts': [
                    {
                        'react_id': 1,
                        'u_ids': [],
                        'is_this_user_reacted': False
                    }
                ],
                'is_pinned': False                
            }
        ], 
            'start': 0, 
            'end': -1
    }

def test_invalid_start(setup):

    joe_smith_data, joes_funland_data, _ = setup

    joe_smith_token = joe_smith_data['token']
    joes_funland_channel_id = joes_funland_data['channel_id']

    # Joe sends a message to his channel, saying "Hi everyone!"
    message_send_input = {"token": joe_smith_token, "channel_id": joes_funland_channel_id, "message": "Hi everyone!"}
    requests.post(f'{BASE_URL}/message/send/v1', json = message_send_input)

    # Joe sends another message to his channel, saying "Please pick your favourite book, ready for Monday 2pm."
    message_send_input = {"token": joe_smith_token, "channel_id": joes_funland_channel_id, "message": "Please pick your favourite book, ready for Monday 2pm."}
    requests.post(f'{BASE_URL}/message/send/v1', json = message_send_input)

    # Joe attempts to view messages starting at an index greater than the number of messages in the channel
    channel_messages_input = {'token': joe_smith_token, 'channel_id': joes_funland_channel_id, 'start': 20}
    response = requests.get(f'{BASE_URL}/channel/messages/v2', params = channel_messages_input).json()
    assert response['code'] == INPUT_ERROR