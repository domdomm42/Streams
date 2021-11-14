import pytest
import requests
from datetime import datetime, timezone
import time

from src.config import *
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


# @pytest.fixture
# def setup_2(setup):

#     joe_smith_token, joes_funland_channel_id, marry_mae_token = setup

#     # Joe Smith sends a message to Private channel "Joe's Reading Club", saying "Hi everyone!"
#     message_send_input = {"token": joe_smith_token, "channel_id": joes_funland_channel_id, "message": "Hi everyone!"}
#     response = requests.post(f'{BASE_URL}/message/send/v1', json = message_send_input)

#     return joe_smith_token, response.json()['message_id'], marry_mae_token, joes_funland_channel_id

def test_simple_standup(setup):

    joe_smith_data, joes_funland_data, marry_mae_data = setup

    channel_invite_info = {'token': joe_smith_data['token'], 'channel_id': joes_funland_data['channel_id'], 'u_id': marry_mae_data['auth_user_id']}
    requests.post(f'{BASE_URL}/channel/invite/v2', json = channel_invite_info)

    standup_start_info = {'token': joe_smith_data['token'], 'channel_id': joes_funland_data['channel_id'], 'length': 3}
    response = requests.post(f'{BASE_URL}/standup/start/v1', json = standup_start_info)

    assert response.status_code == 200

def test_standup_finish_sametime(setup):
    joe_smith_data, joes_funland_data, marry_mae_data = setup

    channel_invite_info = {'token': joe_smith_data['token'], 'channel_id': joes_funland_data['channel_id'], 'u_id': marry_mae_data['auth_user_id']}
    requests.post(f'{BASE_URL}/channel/invite/v2', json = channel_invite_info)

    standup_start_info = {'token': joe_smith_data['token'], 'channel_id': joes_funland_data['channel_id'], 'length': 3}
    requests.post(f'{BASE_URL}/standup/start/v1', json = standup_start_info)

    standup_message_info = {'token': joe_smith_data['token'], 'channel_id': joes_funland_data['channel_id'], 'message': 'hello world this is joe'}
    response = requests.post(f'{BASE_URL}/standup/send/v1', json = standup_message_info)

    time.sleep(3)
    assert response.status_code == 200

def test_negative_time_length(setup):
    joe_smith_data, joes_funland_data, marry_mae_data = setup

    channel_invite_info = {'token': joe_smith_data['token'], 'channel_id': joes_funland_data['channel_id'], 'u_id': marry_mae_data['auth_user_id']}
    requests.post(f'{BASE_URL}/channel/invite/v2', json = channel_invite_info)

    standup_start_info = {'token': joe_smith_data['token'], 'channel_id': joes_funland_data['channel_id'], 'length': -3}
    response = requests.post(f'{BASE_URL}/standup/start/v1', json = standup_start_info)
    response = response.json()

    assert response['code'] == INPUT_ERROR

    
def test_simple_standup_invalidchannel(setup):

    joe_smith_data, joes_funland_data, marry_mae_data = setup

    channel_invite_info = {'token': joe_smith_data['token'], 'channel_id': joes_funland_data['channel_id'], 'u_id': marry_mae_data['auth_user_id']}
    requests.post(f'{BASE_URL}/channel/invite/v2', json = channel_invite_info)

    standup_start_info = {'token': joe_smith_data['token'], 'channel_id': joes_funland_data['channel_id'] + 100, 'length': 3}
    response = requests.post(f'{BASE_URL}/standup/start/v1', json = standup_start_info)
    response = response.json()

    assert response['code'] == INPUT_ERROR

def test_simple_not_in_channel(setup):

    joe_smith_data, joes_funland_data, marry_mae_data = setup

    user_info = {'email': 'marryjoe123@gmail.com', 'password': 'password', 'name_first': 'Marry', 'name_last': 'Joe'}
    marryjoe_data = requests.post(f'{BASE_URL}/auth/register/v2', json = user_info).json()

    channel_invite_info = {'token': joe_smith_data['token'], 'channel_id': joes_funland_data['channel_id'], 'u_id': marry_mae_data['auth_user_id']}
    requests.post(f'{BASE_URL}/channel/invite/v2', json = channel_invite_info)

    standup_start_info = {'token': marryjoe_data['token'], 'channel_id': joes_funland_data['channel_id'], 'length': 3}
    response = requests.post(f'{BASE_URL}/standup/start/v1', json = standup_start_info)
    response = response.json()

    assert response['code'] == ACCESS_ERROR

def test_start_active_again(setup):
    joe_smith_data, joes_funland_data, marry_mae_data = setup

    channel_invite_info = {'token': joe_smith_data['token'], 'channel_id': joes_funland_data['channel_id'], 'u_id': marry_mae_data['auth_user_id']}
    requests.post(f'{BASE_URL}/channel/invite/v2', json = channel_invite_info)

    standup_start_info = {'token': joe_smith_data['token'], 'channel_id': joes_funland_data['channel_id'], 'length': 3}
    requests.post(f'{BASE_URL}/standup/start/v1', json = standup_start_info)
    response = requests.post(f'{BASE_URL}/standup/start/v1', json = standup_start_info)

    {'token': joe_smith_data['token'], 'channel_id': joes_funland_data['channel_id']}
    response = requests.get(f'{BASE_URL}/standup/active/v1', params = standup_start_info)
    
    assert response.status_code == 200

def test_start_inactive(setup):
    joe_smith_data, joes_funland_data, _ = setup

    {'token': joe_smith_data['token'], 'channel_id': joes_funland_data['channel_id']}
    standup_start_info = {'token': joe_smith_data['token'], 'channel_id': joes_funland_data['channel_id'], 'length': 3}
    response = requests.get(f'{BASE_URL}/standup/active/v1', params = standup_start_info)

    assert response.status_code == 200
    


def test_standup_send(setup):
    joe_smith_data, joes_funland_data, marry_mae_data = setup

    channel_invite_info = {'token': joe_smith_data['token'], 'channel_id': joes_funland_data['channel_id'], 'u_id': marry_mae_data['auth_user_id']}
    requests.post(f'{BASE_URL}/channel/invite/v2', json = channel_invite_info)

    standup_start_info = {'token': joe_smith_data['token'], 'channel_id': joes_funland_data['channel_id'], 'length': 3}
    requests.post(f'{BASE_URL}/standup/start/v1', json = standup_start_info)

    standup_message_info = {'token': joe_smith_data['token'], 'channel_id': joes_funland_data['channel_id'], 'message': 'hello world this is joe'}
    response = requests.post(f'{BASE_URL}/standup/send/v1', json = standup_message_info)

    assert response.status_code == 200


def test_standup_send_invalid_cid(setup):
    joe_smith_data, joes_funland_data, marry_mae_data = setup

    channel_invite_info = {'token': joe_smith_data['token'], 'channel_id': joes_funland_data['channel_id'], 'u_id': marry_mae_data['auth_user_id']}
    requests.post(f'{BASE_URL}/channel/invite/v2', json = channel_invite_info)

    standup_start_info = {'token': joe_smith_data['token'], 'channel_id': joes_funland_data['channel_id'], 'length': 3}
    requests.post(f'{BASE_URL}/standup/start/v1', json = standup_start_info)

    standup_message_info = {'token': joe_smith_data['token'], 'channel_id': joes_funland_data['channel_id'] + 2, 'message': 'hello world this is joe'}
    response = requests.post(f'{BASE_URL}/standup/send/v1', json = standup_message_info)
    response = response.json()

    assert response['code'] == INPUT_ERROR

def test_standup_send_long_message(setup):
    joe_smith_data, joes_funland_data, marry_mae_data = setup

    channel_invite_info = {'token': joe_smith_data['token'], 'channel_id': joes_funland_data['channel_id'], 'u_id': marry_mae_data['auth_user_id']}
    requests.post(f'{BASE_URL}/channel/invite/v2', json = channel_invite_info)

    standup_start_info = {'token': joe_smith_data['token'], 'channel_id': joes_funland_data['channel_id'], 'length': 3}
    requests.post(f'{BASE_URL}/standup/start/v1', json = standup_start_info)

    standup_message_info = {'token': joe_smith_data['token'], 'channel_id': joes_funland_data['channel_id'], 'message': 'j' * 1001}
    response = requests.post(f'{BASE_URL}/standup/send/v1', json = standup_message_info)
    response = response.json()

    assert response['code'] == INPUT_ERROR

    
def test_standup_send_inactive(setup):
    joe_smith_data, joes_funland_data, marry_mae_data = setup

    channel_invite_info = {'token': joe_smith_data['token'], 'channel_id': joes_funland_data['channel_id'], 'u_id': marry_mae_data['auth_user_id']}
    requests.post(f'{BASE_URL}/channel/invite/v2', json = channel_invite_info)

    standup_message_info = {'token': joe_smith_data['token'], 'channel_id': joes_funland_data['channel_id'], 'message': 'jk rowling'}
    response = requests.post(f'{BASE_URL}/standup/send/v1', json = standup_message_info)
    response = response.json()

    assert response['code'] == INPUT_ERROR

def test_standup_invalid_user(setup):
    joe_smith_data, joes_funland_data, marry_mae_data = setup

    channel_invite_info = {'token': joe_smith_data['token'], 'channel_id': joes_funland_data['channel_id'], 'u_id': marry_mae_data['auth_user_id']}
    requests.post(f'{BASE_URL}/channel/invite/v2', json = channel_invite_info)

    standup_start_info = {'token': joe_smith_data['token'], 'channel_id': joes_funland_data['channel_id'], 'length': 3}
    requests.post(f'{BASE_URL}/standup/start/v1', json = standup_start_info)

    standup_message_info = {'token': joe_smith_data['token'] + 's', 'channel_id': joes_funland_data['channel_id'], 'message': 'jk rowling'}
    response = requests.post(f'{BASE_URL}/standup/send/v1', json = standup_message_info)
    response = response.json()

    assert response['code'] == ACCESS_ERROR










# def test_send_valid_messages(setup):

#     joe_smith_token, joes_funland_channel_id, _ = setup

#     # Joe Smith sends a message to Private channel "Joe's Reading Club", saying "Hi everyone!"
#     message_send_input = {"token": joe_smith_token, "channel_id": joes_funland_channel_id, "message": "Hi everyone!"}
#     response = requests.post(f'{BASE_URL}/message/send/v1', json = message_send_input)
#     assert response.json()['message_id'] == 0

#     # Joe Smith sends a message to Private channel "Joe's Reading Club", saying "Please pick your favourite book, ready for Monday 2pm."
#     message_send_input = {"token": joe_smith_token, "channel_id": joes_funland_channel_id, "message": "Please pick your favourite book, ready for Monday 2pm."}
#     response = requests.post(f'{BASE_URL}/message/send/v1', json = message_send_input)
#     assert response.json()['message_id'] == 1

# def test_send_an_empty_message(setup):

#     joe_smith_token, joes_funland_channel_id, _ = setup

#     # Joe Smith sends an empty message to Private channel "Joe's Reading Club"
#     message_send_input = {"token": joe_smith_token, "channel_id": joes_funland_channel_id, "message": ""}
#     response = requests.post(f'{BASE_URL}/message/send/v1', json = message_send_input)
#     assert response.json()['code'] == INPUT_ERROR 

#     # Joe Smith sends a message to Private channel "Joe's Reading Club", saying "Hi everyone!"
#     message_send_input = {"token": joe_smith_token, "channel_id": joes_funland_channel_id, "message": "Hi everyone!"}
#     response = requests.post(f'{BASE_URL}/message/send/v1', json = message_send_input)
#     assert response.json()['message_id'] == 0

# def test_send_a_long_message(setup):

#     joe_smith_token, joes_funland_channel_id, _ = setup

#     # Joe Smith sends an long message (>1000 characters) to Private channel "Joe's Reading Club"
#     message_send_input = {"token": joe_smith_token, "channel_id": joes_funland_channel_id, "message": "2"*1001}
#     response = requests.post(f'{BASE_URL}/message/send/v1', json = message_send_input)
#     assert response.json()['code'] == INPUT_ERROR 

#     # Joe Smith sends a message to Private channel "Joe's Reading Club", saying "Hi everyone!"
#     message_send_input = {"token": joe_smith_token, "channel_id": joes_funland_channel_id, "message": "Hi everyone!"}
#     response = requests.post(f'{BASE_URL}/message/send/v1', json = message_send_input)
#     assert response.json()['message_id'] == 0

# def test_invalid_channel_message_send(setup):

#     joe_smith_token, joes_funland_channel_id, _ = setup

#     # Joe Smith sends a message to a channel that does not exist
#     message_send_input = {"token": joe_smith_token, "channel_id": 300, "message": "Hi everyone!"}
#     response = requests.post(f'{BASE_URL}/message/send/v1', json = message_send_input)
#     assert response.json()['code'] == INPUT_ERROR 

#     # Joe Smith sends a message to Private channel "Joe's Reading Club", saying "Hi everyone!"
#     message_send_input = {"token": joe_smith_token, "channel_id": joes_funland_channel_id, "message": "Hi everyone!"}
#     response = requests.post(f'{BASE_URL}/message/send/v1', json = message_send_input)
#     assert response.json()['message_id'] == 0
