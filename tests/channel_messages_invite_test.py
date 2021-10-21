import pytest
import requests

from src.config import *
from src.other import print_store_debug
from datetime import datetime, timezone

BASE_URL = url
INPUT_ERROR = 400
ACCESS_ERROR = 403

'''
the member has to be part of the channel



'''

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

def test_invalid_channel(setup):

    joe_smith_data, _, marry_mae_data = setup
    channel_invite_info = {'token': joe_smith_data['token'], 'channel_id': 10, 'u_id': marry_mae_data['token']}
    response = requests.post(f'{BASE_URL}/channel/invite/v2', json = channel_invite_info)
    response_data = response.json()
    assert response_data['code'] == 400

def test_invalid_u_id(setup):

    joe_smith_data, joes_funland_data, _ = setup
    channel_invite_info = {'token': joe_smith_data['token'], 'channel_id': joes_funland_data['channel_id'], 'u_id': 20}
    response = requests.post(f'{BASE_URL}/channel/invite/v2', json = channel_invite_info)
    response_data = response.json()
    assert response_data['code'] == 400

def test_u_id_already_channel_member(setup):

    joe_smith_data, joes_funland_data, marry_mae_data = setup
    channel_invite_info = {'token': joe_smith_data['token'], 'channel_id': joes_funland_data['channel_id'], 'u_id': marry_mae_data['auth_user_id']}
    requests.post(f'{BASE_URL}/channel/invite/v2', json = channel_invite_info)
    response = requests.post(f'{BASE_URL}/channel/invite/v2', json = channel_invite_info)
    response_data = response.json()
    assert response_data['code'] == 400

def test_auth_user_not_apart_of_channel(setup):

    joe_smith_data, joes_funland_data, marry_mae_data = setup
    channel_invite_info = {'token': marry_mae_data['token'], 'channel_id': joes_funland_data['channel_id'], 'u_id': joe_smith_data['auth_user_id']}
    response = requests.post(f'{BASE_URL}/channel/invite/v2', json = channel_invite_info)
    response_data = response.json()
    print(response_data)
    assert response_data['code'] == 403

def test_send_valid_messages(setup):

    joe_smith_data, joes_funland_data, _ = setup

    joe_smith_token = joe_smith_data['token']
    joes_funland_channel_id = joes_funland_data['channel_id']
    #marry_mae_token = setup()[2]['token']

    message_send_input = {"token": joe_smith_token, "channel_id": joes_funland_channel_id, "message": "Hi everyone!"}
    requests.post(f'{BASE_URL}/message/send/v1', json = message_send_input)
    message_0_time = datetime.now().replace(tzinfo=timezone.utc).timestamp()

    message_send_input = {"token": joe_smith_token, "channel_id": joes_funland_channel_id, "message": "Please pick your favourite book, ready for Monday 2pm."}
    requests.post(f'{BASE_URL}/message/send/v1', json = message_send_input)
    message_1_time = datetime.now().replace(tzinfo=timezone.utc).timestamp()

    channel_messages_input = {'token': joe_smith_token, 'channel_id': joes_funland_channel_id, 'start': 0}
    response = requests.get(f'{BASE_URL}/channel/messages/v2', json = channel_messages_input).json()

    response['messages'][0]['time_created'] = int(response['messages'][0]['time_created'])
    response['messages'][1]['time_created'] = int(response['messages'][1]['time_created'])

    assert response == {
        'messages': [
            {
                'message_id': 1, 
                'u_id': 0, 
                'message': 'Please pick your favourite book, ready for Monday 2pm.', 
                'time_created': int(message_1_time)
            }, 
            {
                'message_id': 0, 
                'u_id': 0, 
                'message': 'Hi everyone!', 
                'time_created': int(message_0_time)
            }
        ], 
            'start': 0, 
            'end': -1
    }