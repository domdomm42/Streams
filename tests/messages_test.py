import pytest
import requests

from src.config import *
from src.other import print_store_debug
BASE_URL = url
INPUT_ERROR = 400
ACCESS_ERROR = 403

'''
the member has to be part of the channel



'''


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

    print_store_debug()

    return joe_smith_data, joes_funland_data, marry_mae_data

def setup_2():

    joe_smith_token = setup()[0]['token']
    joes_funland_channel_id = setup()[1]['channel_id']
    marry_mae_token = setup()[2]['token']

    message_send_input = {"token": joe_smith_token, "channel_id": joes_funland_channel_id, "message": "Hi everyone!"}
    response = requests.post(f'{BASE_URL}/message/send/v1', json = message_send_input)

    return joe_smith_token, response.json()['message_id'], marry_mae_token, joes_funland_channel_id

# Test Sending Valid Messages
def test_send_valid_messages():


    values = setup()

    joe_smith_token = values[0]['token']
    joes_funland_channel_id = values[1]['channel_id']
    #marry_mae_token = setup()[2]['token']

    message_send_input = {"token": joe_smith_token, "channel_id": joes_funland_channel_id, "message": "Hi everyone!"}
    response = requests.post(f'{BASE_URL}/message/send/v1', json = message_send_input)

    assert response.json()['message_id'] == 0

    message_send_input = {"token": joe_smith_token, "channel_id": joes_funland_channel_id, "message": "Please pick your favourite book, ready for Monday 2pm."}
    response = requests.post(f'{BASE_URL}/message/send/v1', json = message_send_input)
    assert response.json()['message_id'] == 1

def test_send_an_empty_message():

    values = setup()

    joe_smith_token = values[0]['token']
    joes_funland_channel_id = values[1]['channel_id']
    #marry_mae_token = setup()[2]['token']

    message_send_input = {"token": joe_smith_token, "channel_id": joes_funland_channel_id, "message": ""}
    response = requests.post(f'{BASE_URL}/message/send/v1', json = message_send_input)
    assert response.json()['code'] == INPUT_ERROR 

    message_send_input = {"token": joe_smith_token, "channel_id": joes_funland_channel_id, "message": "Hi everyone!"}
    response = requests.post(f'{BASE_URL}/message/send/v1', json = message_send_input)
    assert response.json()['message_id'] == 0

def test_send_a_long_message():

    joe_smith_token = setup()[0]['token']
    joes_funland_channel_id = setup()[1]['channel_id']
    #marry_mae_token = setup()[2]['token']

    message_send_input = {"token": joe_smith_token, "channel_id": joes_funland_channel_id, "message": "2"*1001}
    response = requests.post(f'{BASE_URL}/message/send/v1', json = message_send_input)
    assert response.json()['code'] == INPUT_ERROR 

    message_send_input = {"token": joe_smith_token, "channel_id": joes_funland_channel_id, "message": "Hi everyone!"}
    response = requests.post(f'{BASE_URL}/message/send/v1', json = message_send_input)
    assert response.json()['message_id'] == 0

def test_invalid_channel_message_send():

    joe_smith_token = setup()[0]['token']
    joes_funland_channel_id = setup()[1]['channel_id']
    #marry_mae_token = setup()[2]['token']

    message_send_input = {"token": joe_smith_token, "channel_id": 300, "message": "Hi everyone!"}
    response = requests.post(f'{BASE_URL}/message/send/v1', json = message_send_input)
    assert response.json()['code'] == INPUT_ERROR 

    message_send_input = {"token": joe_smith_token, "channel_id": joes_funland_channel_id, "message": "Hi everyone!"}
    response = requests.post(f'{BASE_URL}/message/send/v1', json = message_send_input)
    assert response.json()['message_id'] == 0

def test_unauthorised_message_send():

    joe_smith_token = setup()[0]['token']
    joes_funland_channel_id = setup()[1]['channel_id']
    marry_mae_token = setup()[2]['token']

    message_send_input = {"token": marry_mae_token, "channel_id": joes_funland_channel_id, "message": "I'm a hacker"}
    response = requests.post(f'{BASE_URL}/message/send/v1', json = message_send_input)
    assert response.json()['code'] == ACCESS_ERROR 

    message_send_input = {"token": joe_smith_token, "channel_id": joes_funland_channel_id, "message": "Hi everyone!"}
    response = requests.post(f'{BASE_URL}/message/send/v1', json = message_send_input)
    assert response.json()['message_id'] == 0

def test_unauthorised_message_send_and_long_message():

    #joe_smith_token = setup()[0]['token']
    joes_funland_channel_id = setup()[1]['channel_id']
    marry_mae_token = setup()[2]['token']

    message_send_input = {"token": marry_mae_token, "channel_id": joes_funland_channel_id, "message": "Hi everyone!"*5000}
    response = requests.post(f'{BASE_URL}/message/send/v1', json = message_send_input)
    assert response.json()['code'] == ACCESS_ERROR 

def test_unauthorised_message_send_and_empty_message():

    #joe_smith_token = setup()[0]['token']
    joes_funland_channel_id = setup()[1]['channel_id']
    marry_mae_token = setup()[2]['token']

    message_send_input = {"token": marry_mae_token, "channel_id": joes_funland_channel_id, "message": ""}
    response = requests.post(f'{BASE_URL}/message/send/v1', json = message_send_input)
    assert response.json()['code'] == ACCESS_ERROR 

def test_unauthorised_message_send_and_invalid_channel():

    #joe_smith_token = setup()[0]['token']
    #joes_funland_channel_id = setup()[1]['channel_id']
    marry_mae_token = setup()[2]['token']

    message_send_input = {"token": marry_mae_token, "channel_id": 300, "message": "Hello everyone!"}
    response = requests.post(f'{BASE_URL}/message/send/v1', json = message_send_input)
    assert response.json()['code'] == INPUT_ERROR 

###################
# TESTING EDIT MESSAGE

def test_edit_long_message():
    
    joe_smith_token = setup_2()[0]
    message_id = setup_2()[1]

    message_edit_input = {"token": joe_smith_token, "message_id": message_id, "message": "Hi!"*1000}
    response = requests.put(f'{BASE_URL}/message/edit/v1', json = message_edit_input)
    assert response.json()['code'] == INPUT_ERROR

def test_edit_empty_message():
    
    joe_smith_token = setup_2()[0]
    message_id = setup_2()[1]

    message_edit_input = {"token": joe_smith_token, "message_id": message_id, "message": ""}
    response = requests.put(f'{BASE_URL}/message/edit/v1', json = message_edit_input)

    # Empty message causes the message to be deleted, which raises 
    message_edit_input = {"token": joe_smith_token, "message_id": message_id, "message": "Hi"}
    response = requests.put(f'{BASE_URL}/message/edit/v1', json = message_edit_input)
    assert response.json()['code'] == INPUT_ERROR

def test_unauthorised_user_edit_message():

    #joe_smith_token = setup_2()[0]
    message_id = setup_2()[1]
    marry_mae_token = setup_2()[2]

    message_edit_input = {"token": marry_mae_token, "message_id": message_id, "message": "I'm a hacker!"} 
    response = requests.put(f'{BASE_URL}/message/edit/v1', json = message_edit_input)
    assert response.json()['code'] == ACCESS_ERROR

# ## the owners can edit any message even if they don't send it

# def test_owner_editing_any_message(setup_2):

#     joe_smith_token = setup_2()[0]
#     #message_id = setup_2()[1]
#     marry_mae_token = setup_2[2]
#     joes_funland_data = setup_2[3]

#     # Invite Marry to Joe's Private channel
#     invite_input = {"token": joe_smith_token, "channel_id": joes_funland_data, "u_id": 1}
#     response = requests.post(f'{BASE_URL}/channel/invite/v2', json = invite_input)

#     # Marry send's a message to the channel
#     message_send_input = {"token": marry_mae_token, "channel_id": joes_funland_data, "message": "Hello everyone, I'm Mrry!"}
#     response = requests.post(f'{BASE_URL}/message/send/v1', json = message_send_input)

#     marrys_message_id = response.json()['message_id']

#     # Joe, the owner, edits Marry's message
#     message_edit_input = {"token": joe_smith_token, "message_id": marrys_message_id, "message": "Hello everyone, I'm Marry!"} 
#     response = requests.put(f'{BASE_URL}/message/edit/v1', json = message_edit_input)    

#     # MAYBE TRY TO CHECK!??

# #################
# # REMOVING MESSAGE

# def test_remove_invalid_twice(setup_2):

#     joe_smith_token = setup_2()[0]
#     message_id = setup_2()[1]

#     message_delete_input = {"token": joe_smith_token, "message_id": message_id}
#     response = requests.delete(f'{BASE_URL}/message/remove/v1', json = message_delete_input)

#     # Empty message causes the message to be deleted, which raises 
#     message_delete_input = {"token": joe_smith_token, "message_id": message_id}
#     response = requests.delete(f'{BASE_URL}/message/remove/v1', json = message_delete_input)
#     assert response.json()['code'] == INPUT_ERROR

# def test_unauthorised_user_delete_message(setup_2):

#     #joe_smith_token = setup_2()[0]
#     message_id = setup_2()[1]
#     marry_mae_token = setup_2[2]

#     message_delete_input = {"token": marry_mae_token, "message_id": message_id, "message": "I'm a hacker!"} 
#     response = requests.put(f'{BASE_URL}/message/delete/v1', json = message_delete_input)
#     assert response.json()['code'] == ACCESS_ERROR

# ## the owners can edit any message even if they don't send it

# def test_owner_editing_any_message(setup_2):

#     joe_smith_token = setup_2()[0]
#     #message_id = setup_2()[1]
#     marry_mae_token = setup_2[2]
#     joes_funland_data = setup_2[3]

#     # Invite Marry to Joe's Private channel
#     invite_input = {"token": joe_smith_token, "channel_id": joes_funland_data, "u_id": 1}
#     response = requests.post(f'{BASE_URL}/channel/invite/v2', json = invite_input)

#     # Marry send's a message to the channel
#     message_send_input = {"token": marry_mae_token, "channel_id": joes_funland_data, "message": "Hello everyone, I'm Mrry!"}
#     response = requests.post(f'{BASE_URL}/message/delete/v1', json = message_send_input)

#     marrys_message_id = response.json()['message_id']

#     # Joe, the owner, deletes Marry's message
#     message_delete_input = {"token": joe_smith_token, "message_id": marrys_message_id, "message": "Hello everyone, I'm Marry!"} 
#     response = requests.put(f'{BASE_URL}/message/edit/v1', json = message_delete_input)    

