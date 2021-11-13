import pytest
import requests
from datetime import datetime, timezone
import time

from src.config import *
BASE_URL = url
INPUT_ERROR = 400
ACCESS_ERROR = 403

# @pytest.fixture
# def setup():
#     requests.delete(f'{BASE_URL}/clear/v1')

#     # Create user Joe Smith
#     user_info1 = {"email": "joe123@gmail.com", "password": "delicious23", "name_first": "Joe", "name_last": "Smith"}
#     response1 = requests.post(f'{BASE_URL}/auth/register/v2', json = user_info1)
#     joe_smith_data = response.json()

#     # Joe Smith creates a Private channel named "Joe's Reading Club"
#     channel_info = {"token": joe_smith_data['token'], "name": "Joe's Reading Club", "is_public": False}
#     response = requests.post(f'{BASE_URL}/channels/create/v2', json = channel_info)
#     joes_funland_data = response.json()

#     # Create user Marry Mae
#     user_info2 = {"email": "marrymae@gmail.com", "password": "cats1010", "name_first": "Marry", "name_last": "Mae"}
#     response2 = requests.post(f'{BASE_URL}/auth/register/v2', json = user_info2)
#     marry_mae_data = response.json()

#     # Joe invites marry into channel
#     invite_info1 = {"token": joe_smith_data["token"],"channel_id": joes_funland_data["channel_id"] , "u_id": marry_mae_data["auth_user_id"]
#     response3 = requests.post(f'{BASE_URL}/channel/invite/v2', json = invite_info1)
#     invite_data = response3.json()

#     # Standup data
#     standup_info = {"token": joe_smith_data['token'], "channel_id": joes_funland_data["channel_id"], "length": 20}
#     response_standup = requests.post(f'{BASE_URL}/channel/invite/v2', json = standup_info)
#     standup_data = response_standup.json()


#     return joe_smith_data['token'], joes_funland_data['channel_id'], marry_mae_data['token']

# @pytest.fixture
# def setup_2(setup):

#     joe_smith_token, joes_funland_channel_id, marry_mae_token = setup

#     # Joe Smith sends a message to Private channel "Joe's Reading Club", saying "Hi everyone!"
#     message_send_input = {"token": joe_smith_token, "channel_id": joes_funland_channel_id, "message": "Hi everyone!"}
#     response = requests.post(f'{BASE_URL}/message/send/v1', json = message_send_input)

#     return joe_smith_token, response.json()['message_id'], marry_mae_token, joes_funland_channel_id

def test_simple_standup():
    requests.delete(f'{BASE_URL}/clear/v1')

    # Create user Joe Smith
    user_info1 = {"email": "joe123@gmail.com", "password": "delicious23", "name_first": "Joe", "name_last": "Smith"}
    response1 = requests.post(f'{BASE_URL}/auth/register/v2', json = user_info1)
    joe_smith_data = response1.json()

    # Joe Smith creates a Private channel named "Joe's Reading Club"
    channel_info = {"token": joe_smith_data['token'], "name": "Joe's Reading Club", "is_public": False}
    response2 = requests.post(f'{BASE_URL}/channels/create/v2', json = channel_info)
    joes_funland_data = response2.json()

    # Create user Marry Mae
    user_info2 = {"email": "marrymae@gmail.com", "password": "cats1010", "name_first": "Marry", "name_last": "Mae"}
    response3 = requests.post(f'{BASE_URL}/auth/register/v2', json = user_info2)
    marry_mae_data = response3.json()

    # Joe invites marry into channel
    invite_info1 = {"token": joe_smith_data["token"], "channel_id": joes_funland_data["channel_id"], "u_id": marry_mae_data["auth_user_id"]}
    response4 = requests.post(f'{BASE_URL}/channel/invite/v2', json = invite_info1)
    invite_data = response4.json()

    # Standup data
    standup_info = {"token": joe_smith_data['token'], "channel_id": joes_funland_data["channel_id"], "length": 20}
    response_standup = requests.post(f'{BASE_URL}/channel/invite/v2', json = standup_info)
    # standup_data = response_standup.json()

    assert response_standup.status_code == 200


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
