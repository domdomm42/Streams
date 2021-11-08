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

    return joe_smith_data['token'], joes_funland_data['channel_id'], marry_mae_data['token']

@pytest.fixture
def setup_2(setup):

    joe_smith_token, joes_funland_channel_id, marry_mae_token = setup

    # Joe Smith sends a message to Private channel "Joe's Reading Club", saying "Hi everyone!"
    message_send_input = {"token": joe_smith_token, "channel_id": joes_funland_channel_id, "message": "Hi everyone!"}
    response = requests.post(f'{BASE_URL}/message/send/v1', json = message_send_input)

    return joe_smith_token, response.json()['message_id'], marry_mae_token, joes_funland_channel_id

@pytest.fixture
def setup_3():
    requests.delete(f'{BASE_URL}/clear/v1')

    # Create user Joe Smith
    user_info = {"email": "joe123@gmail.com", "password": "delicious23", "name_first": "Joe", "name_last": "Smith"}
    response = requests.post(f'{BASE_URL}/auth/register/v2', json = user_info)
    joe_smith_data = response.json()

    # Create user Marry Mae
    user_info = {"email": "marrymae@gmail.com", "password": "cats1010", "name_first": "Marry", "name_last": "Mae"}
    response = requests.post(f'{BASE_URL}/auth/register/v2', json = user_info)
    marry_mae_data = response.json()

    # Joe Smith creates a DM
    dm_info = {"token": joe_smith_data['token'], "u_ids": [0, 1]}
    response = requests.post(f'{BASE_URL}/dm/create/v1', json = dm_info)
    joe_marry_dm = response.json()

    return joe_smith_data['token'], marry_mae_data['token'], joe_marry_dm['dm_id']

@pytest.fixture
def setup_4(setup_3):

    joe_smith_token, marry_mae_token, joe_marry_dm_id = setup_3
    
    # Joe Smith sends a message to DM
    message_send_input = {"token": joe_smith_token, "dm_id": joe_marry_dm_id, "message": "Hi everyone!"}
    response = requests.post(f'{BASE_URL}/message/senddm/v1', json = message_send_input)
    message_id = response.json()['message_id']

    # Create user Daron Mike
    user_info = {"email": "joe12223@gmail.com", "password": "delicious23", "name_first": "Darron", "name_last": "Mike"}
    response = requests.post(f'{BASE_URL}/auth/register/v2', json = user_info)
    darron_mike_data = response.json()

    return joe_smith_token, marry_mae_token, joe_marry_dm_id, message_id, darron_mike_data['token']

'''
Testing message/senddm/v1 HTTP requests
'''
def test_send_valid_messages_dm(setup_3):

    joe_smith_token, marry_mae_token, joe_marry_dm_id = setup_3

    # Joe Smith sends a message to DM, saying "Hi everyone!"
    message_send_input = {"token": joe_smith_token, "dm_id": joe_marry_dm_id, "message": "Hi everyone!"}
    response = requests.post(f'{BASE_URL}/message/senddm/v1', json = message_send_input)
    assert response.json()['message_id'] == 0

    # Marry Mae sends a message to DM, saying "Please pick your favourite book, ready for Monday 2pm."
    message_send_input = {"token": marry_mae_token, "dm_id": joe_marry_dm_id, "message": "Please pick your favourite book, ready for Monday 2pm."}
    response = requests.post(f'{BASE_URL}/message/senddm/v1', json = message_send_input)
    assert response.json()['message_id'] == 1

def test_send_an_empty_message_dm(setup_3):

    joe_smith_token, marry_mae_token, joe_marry_dm_id = setup_3

    # Joe Smith sends an empty message to DM
    message_send_input = {"token": joe_smith_token, "dm_id": joe_marry_dm_id, "message": ""}
    response = requests.post(f'{BASE_URL}/message/senddm/v1', json = message_send_input)
    assert response.json()['code'] == INPUT_ERROR 

    # Marry Mae sends a message to DM, saying "Hi everyone!"
    message_send_input = {"token": marry_mae_token, "dm_id": joe_marry_dm_id, "message": "Please pick your favourite book, ready for Monday 2pm."}
    response = requests.post(f'{BASE_URL}/message/senddm/v1', json = message_send_input)
    assert response.json()['message_id'] == 0

def test_send_a_long_message_dm(setup_3):

    joe_smith_token, marry_mae_token, joe_marry_dm_id = setup_3

    # Joe Smith sends a very long message to DM (>1000 characters)
    message_send_input = {"token": joe_smith_token, "dm_id": joe_marry_dm_id, "message": "1"*1001}
    response = requests.post(f'{BASE_URL}/message/senddm/v1', json = message_send_input)
    assert response.json()['code'] == INPUT_ERROR 

    # Marry Mae sends a message to DM, saying "Hi everyone!"
    message_send_input = {"token": marry_mae_token, "dm_id": joe_marry_dm_id, "message": "Please pick your favourite book, ready for Monday 2pm."}
    response = requests.post(f'{BASE_URL}/message/senddm/v1', json = message_send_input)
    assert response.json()['message_id'] == 0

def test_send_invalid_dm_id(setup_3):

    joe_smith_token, marry_mae_token, joe_marry_dm_id = setup_3

    # Joe Smith sends a message to a DM which does not exist
    message_send_input = {"token": joe_smith_token, "dm_id": 300, "message": "Hi everyone!"}
    response = requests.post(f'{BASE_URL}/message/senddm/v1', json = message_send_input)
    assert response.json()['code'] == INPUT_ERROR 

    # Marry Mae sends a message to DM, saying "Please pick your favourite book, ready for Monday 2pm."
    message_send_input = {"token": marry_mae_token, "dm_id": joe_marry_dm_id, "message": "Please pick your favourite book, ready for Monday 2pm."}
    response = requests.post(f'{BASE_URL}/message/senddm/v1', json = message_send_input)
    assert response.json()['message_id'] == 0

def test_unauthorised_user_send_message_dm(setup_4):

    _, _, joe_marry_dm_id, _, darron_token = setup_4

    # Darron, who is not part of the DM, sends a message saying "Please pick your favourite book, ready for Monday 2pm."
    message_send_input = {"token": darron_token, "dm_id": joe_marry_dm_id, "message": "Please pick your favourite book, ready for Monday 2pm."}
    response = requests.post(f'{BASE_URL}/message/senddm/v1', json = message_send_input)
    assert response.json()['code'] == ACCESS_ERROR

'''
Testing message/send/v1 HTTP requests
'''

def test_send_valid_messages(setup):

    joe_smith_token, joes_funland_channel_id, _ = setup

    # Joe Smith sends a message to Private channel "Joe's Reading Club", saying "Hi everyone!"
    message_send_input = {"token": joe_smith_token, "channel_id": joes_funland_channel_id, "message": "Hi everyone!"}
    response = requests.post(f'{BASE_URL}/message/send/v1', json = message_send_input)
    assert response.json()['message_id'] == 0

    # Joe Smith sends a message to Private channel "Joe's Reading Club", saying "Please pick your favourite book, ready for Monday 2pm."
    message_send_input = {"token": joe_smith_token, "channel_id": joes_funland_channel_id, "message": "Please pick your favourite book, ready for Monday 2pm."}
    response = requests.post(f'{BASE_URL}/message/send/v1', json = message_send_input)
    assert response.json()['message_id'] == 1

def test_send_an_empty_message(setup):

    joe_smith_token, joes_funland_channel_id, _ = setup

    # Joe Smith sends an empty message to Private channel "Joe's Reading Club"
    message_send_input = {"token": joe_smith_token, "channel_id": joes_funland_channel_id, "message": ""}
    response = requests.post(f'{BASE_URL}/message/send/v1', json = message_send_input)
    assert response.json()['code'] == INPUT_ERROR 

    # Joe Smith sends a message to Private channel "Joe's Reading Club", saying "Hi everyone!"
    message_send_input = {"token": joe_smith_token, "channel_id": joes_funland_channel_id, "message": "Hi everyone!"}
    response = requests.post(f'{BASE_URL}/message/send/v1', json = message_send_input)
    assert response.json()['message_id'] == 0

def test_send_a_long_message(setup):

    joe_smith_token, joes_funland_channel_id, _ = setup

    # Joe Smith sends an long message (>1000 characters) to Private channel "Joe's Reading Club"
    message_send_input = {"token": joe_smith_token, "channel_id": joes_funland_channel_id, "message": "2"*1001}
    response = requests.post(f'{BASE_URL}/message/send/v1', json = message_send_input)
    assert response.json()['code'] == INPUT_ERROR 

    # Joe Smith sends a message to Private channel "Joe's Reading Club", saying "Hi everyone!"
    message_send_input = {"token": joe_smith_token, "channel_id": joes_funland_channel_id, "message": "Hi everyone!"}
    response = requests.post(f'{BASE_URL}/message/send/v1', json = message_send_input)
    assert response.json()['message_id'] == 0

def test_invalid_channel_message_send(setup):

    joe_smith_token, joes_funland_channel_id, _ = setup

    # Joe Smith sends a message to a channel that does not exist
    message_send_input = {"token": joe_smith_token, "channel_id": 300, "message": "Hi everyone!"}
    response = requests.post(f'{BASE_URL}/message/send/v1', json = message_send_input)
    assert response.json()['code'] == INPUT_ERROR 

    # Joe Smith sends a message to Private channel "Joe's Reading Club", saying "Hi everyone!"
    message_send_input = {"token": joe_smith_token, "channel_id": joes_funland_channel_id, "message": "Hi everyone!"}
    response = requests.post(f'{BASE_URL}/message/send/v1', json = message_send_input)
    assert response.json()['message_id'] == 0

def test_unauthorised_message_send(setup):

    joe_smith_token, joes_funland_channel_id, marry_mae_token = setup

    # Marry Mae attempts to send a message to channel she is not a part of
    message_send_input = {"token": marry_mae_token, "channel_id": joes_funland_channel_id, "message": "I'm a hacker"}
    response = requests.post(f'{BASE_URL}/message/send/v1', json = message_send_input)
    assert response.json()['code'] == ACCESS_ERROR 

    # Joe Smith sends a message to Private channel "Joe's Reading Club", saying "Hi everyone!"
    message_send_input = {"token": joe_smith_token, "channel_id": joes_funland_channel_id, "message": "Hi everyone!"}
    response = requests.post(f'{BASE_URL}/message/send/v1', json = message_send_input)
    assert response.json()['message_id'] == 0

def test_unauthorised_message_send_and_long_message(setup):

    _, joes_funland_channel_id, marry_mae_token = setup

    # Marry Mae attempts to send a long message (>1000 characters) to channel she is not a part of
    message_send_input = {"token": marry_mae_token, "channel_id": joes_funland_channel_id, "message": "Hi everyone!"*5000}
    response = requests.post(f'{BASE_URL}/message/send/v1', json = message_send_input)
    assert response.json()['code'] == ACCESS_ERROR 

def test_unauthorised_message_send_and_empty_message(setup):

    _, joes_funland_channel_id, marry_mae_token = setup

    # Marry Mae attempts to send an empty message to channel she is not a part of
    message_send_input = {"token": marry_mae_token, "channel_id": joes_funland_channel_id, "message": ""}
    response = requests.post(f'{BASE_URL}/message/send/v1', json = message_send_input)
    assert response.json()['code'] == ACCESS_ERROR 

def test_unauthorised_message_send_and_invalid_channel(setup):

    _, _, marry_mae_token = setup

    # Marry Mae attempts to send a message to channel that does not exist
    message_send_input = {"token": marry_mae_token, "channel_id": 300, "message": "Hello everyone!"}
    response = requests.post(f'{BASE_URL}/message/send/v1', json = message_send_input)
    assert response.json()['code'] == INPUT_ERROR 

'''
Testing message/edit/v1 HTTP requests
'''

def test_edit_invalid_message_dm(setup_4):
    
    joe_smith_token, _, _, _, _ = setup_4
    
    # Joe Smith attempts to edit a message that does not exist
    message_edit_input = {"token": joe_smith_token, "message_id": 5, "message": "Hi!"}
    response = requests.put(f'{BASE_URL}/message/edit/v1', json = message_edit_input)
    assert response.json()['code'] == INPUT_ERROR

def test_edit_valid_message_dm(setup_4):
    
    joe_smith_token, _, _, message_id, _ = setup_4
    
    # Joe Smith successfully edits a message that does not exist
    message_edit_input = {"token": joe_smith_token, "message_id": message_id, "message": "Hi!"}
    response = requests.put(f'{BASE_URL}/message/edit/v1', json = message_edit_input)
    assert response.status_code in [200, 201]

def test_edit_long_message_dm(setup_4):
    
    joe_smith_token, _, _, message_id, _ = setup_4
    
    # Joe Smith attempts to edit a valid message with a very long message (>1000 characters)
    message_edit_input = {"token": joe_smith_token, "message_id": message_id, "message": "Hi!"*1000}
    response = requests.put(f'{BASE_URL}/message/edit/v1', json = message_edit_input)
    assert response.json()['code'] == INPUT_ERROR

def test_edit_empty_message_dm(setup_4):
    
    joe_smith_token, _, _, message_id, _ = setup_4
    
    # Joe Smith attempts to edit an empty message, causing the message to be deleted
    message_edit_input = {"token": joe_smith_token, "message_id": message_id, "message": ""}
    response = requests.put(f'{BASE_URL}/message/edit/v1', json = message_edit_input)

    # Joe Smith attempts to re-edit the message which is not possible
    message_edit_input = {"token": joe_smith_token, "message_id": message_id, "message": "Hi"}
    response = requests.put(f'{BASE_URL}/message/edit/v1', json = message_edit_input)
    assert response.json()['code'] == INPUT_ERROR

def test_unauthorised_user_edit_message_dm(setup_4):

    _, _, _, message_id, darron_mike_token = setup_4

    # Darron attempts to edit a message she did not send and is not the owner of the DM
    message_edit_input = {"token": darron_mike_token, "message_id": message_id, "message": "I'm a hacker!"} 
    response = requests.put(f'{BASE_URL}/message/edit/v1', json = message_edit_input)   
    assert response.json()['code'] == ACCESS_ERROR

def test_owner_editing_any_message_dm(setup_4):

    joe_smith_token, marry_mae_token, joe_marry_dm_id, _, _ = setup_4

    # Marry sends a message to DM
    message_send_input = {"token": marry_mae_token, "dm_id": joe_marry_dm_id, "message": "Hello everyone, I'm Mrry!"}
    response = requests.post(f'{BASE_URL}/message/senddm/v1', json = message_send_input)
    marrys_message_id = response.json()['message_id']

    # Joe, the owner, successfully edits Marry's message
    message_edit_input = {"token": joe_smith_token, "message_id": marrys_message_id, "message": "Hello everyone, I'm Marry!"} 
    response = requests.put(f'{BASE_URL}/message/edit/v1', json = message_edit_input)
    assert response.status_code in [200, 201]

def test_edit_invalid_message(setup_2):
    
    joe_smith_token, _, _, _ = setup_2
    
    # Joe Smith attempts to edit a message that does not exist
    message_edit_input = {"token": joe_smith_token, "message_id": 3, "message": "Hi!"}
    response = requests.put(f'{BASE_URL}/message/edit/v1', json = message_edit_input)
    assert response.json()['code'] == INPUT_ERROR

def test_edit_valid_message(setup_2):
    
    joe_smith_token, message_id, _, _ = setup_2

    # Joe Smith edits a message he has sent
    message_edit_input = {"token": joe_smith_token, "message_id": message_id, "message": "Hi!"}
    response = requests.put(f'{BASE_URL}/message/edit/v1', json = message_edit_input)
    assert response.status_code in [200, 201]

def test_edit_long_message(setup_2):
    
    joe_smith_token, message_id, _, _ = setup_2

    # Joe Smith edits a valid message into a very long (>1000 characters) message
    message_edit_input = {"token": joe_smith_token, "message_id": message_id, "message": "Hi!"*1000}
    response = requests.put(f'{BASE_URL}/message/edit/v1', json = message_edit_input)
    assert response.json()['code'] == INPUT_ERROR

def test_edit_empty_message(setup_2):
    
    joe_smith_token, message_id, _, _ = setup_2

    # Joe Smith edits a valid message into an empty message
    message_edit_input = {"token": joe_smith_token, "message_id": message_id, "message": ""}
    response = requests.put(f'{BASE_URL}/message/edit/v1', json = message_edit_input)
    assert response.status_code in [200, 201]

    # Empty message causes the message to be deleted
    # Joe Smith attempts to re-edit the message, but since it has been deleted, the message does not exist
    message_edit_input = {"token": joe_smith_token, "message_id": message_id, "message": "Hi"}
    response = requests.put(f'{BASE_URL}/message/edit/v1', json = message_edit_input)
    assert response.json()['code'] == INPUT_ERROR

def test_unauthorised_user_edit_message(setup_2):

    _, message_id, marry_mae_token, _ = setup_2

    # Marry Mae attempts to edit a message she did not send and is not the owner of the DM
    message_edit_input = {"token": marry_mae_token, "message_id": message_id, "message": "I'm a hacker!"} 
    response = requests.put(f'{BASE_URL}/message/edit/v1', json = message_edit_input)
    assert response.json()['code'] == ACCESS_ERROR

def test_owner_editing_any_message(setup_2):

    joe_smith_token, _, marry_mae_token, joes_funland_channel_id = setup_2

    # Invite Marry to Joe's Private channel
    invite_input = {"token": joe_smith_token, "channel_id": joes_funland_channel_id, "u_id": 1}
    response = requests.post(f'{BASE_URL}/channel/invite/v2', json = invite_input)
    assert response.status_code in [200, 201]

    # Marry sends a message to Joe's Private channel
    message_send_input = {"token": marry_mae_token, "channel_id": joes_funland_channel_id, "message": "Hello everyone, I'm Mrry!"}
    response = requests.post(f'{BASE_URL}/message/send/v1', json = message_send_input)
    marrys_message_id = response.json()['message_id']

    # Joe, the owner, successfully edits Marry's message
    message_edit_input = {"token": joe_smith_token, "message_id": marrys_message_id, "message": "Hello everyone, I'm Marry!"} 
    response = requests.put(f'{BASE_URL}/message/edit/v1', json = message_edit_input)
    assert response.status_code in [200, 201]

def test_global_owner_edit_any_message(setup_2):

    joe_smith_token, message_id, marry_mae_token, _ = setup_2

    # Joe Smith makes Marry Mae a Global Owner
    permission_change_data_1 = {'token': joe_smith_token, 'u_id': 1, 'permission_id': 1}
    response = requests.post(f'{BASE_URL}/admin/userpermission/change/v1', json = permission_change_data_1)
    assert response.status_code in [200, 201]

    # Marry Mae edits Joe's message
    message_edit_input = {"token": marry_mae_token, "message_id": message_id, "message": "Hacked!"} 
    response = requests.put(f'{BASE_URL}/message/edit/v1', json = message_edit_input)
    assert response.status_code in [200, 201]

'''
Testing message/remove/v1 HTTP requests
'''

def test_remove_invalid_twice(setup_2):

    joe_smith_token, message_id, _, _ = setup_2

    # Joe Smith successfully deletes a message
    message_delete_input = {"token": joe_smith_token, "message_id": message_id}
    response = requests.delete(f'{BASE_URL}/message/remove/v1', json = message_delete_input)
    assert response.status_code in [200, 201]

    # Joe Smith reattempts to delete the same message
    message_delete_input = {"token": joe_smith_token, "message_id": message_id}
    response = requests.delete(f'{BASE_URL}/message/remove/v1', json = message_delete_input)
    assert response.json()['code'] == INPUT_ERROR

def test_unauthorised_user_delete_message(setup_2):

    _, message_id, marry_mae_token, _ = setup_2

    # Marry Mae attempts to delete a message she did not send, and is not the owner of the channel which the message belongs to
    message_delete_input = {"token": marry_mae_token, "message_id": message_id, "message": "I'm a hacker!"} 
    response = requests.delete(f'{BASE_URL}/message/remove/v1', json = message_delete_input)
    assert response.json()['code'] == ACCESS_ERROR

def test_owner_removing_any_message(setup_2):

    joe_smith_token, _, marry_mae_token, joes_funland_channel_id = setup_2

    # Invite Marry to Joe's Private channel
    invite_input = {"token": joe_smith_token, "channel_id": joes_funland_channel_id, "u_id": 1}
    response = requests.post(f'{BASE_URL}/channel/invite/v2', json = invite_input)
    assert response.status_code in [200, 201]

    # Marry send's a message to the channel
    message_send_input = {"token": marry_mae_token, "channel_id": joes_funland_channel_id, "message": "Hello everyone, I'm Mrry!"}
    response = requests.post(f'{BASE_URL}/message/send/v1', json = message_send_input)
    marrys_message_id = response.json()['message_id']

    # Joe, the owner, successfully deletes Marry's message
    message_delete_input = {"token": joe_smith_token, "message_id": marrys_message_id} 
    response = requests.delete(f'{BASE_URL}/message/remove/v1', json = message_delete_input)    
    assert response.status_code in [200, 201]

def test_global_owner_remove_any_message(setup_2):

    joe_smith_token, message_id, marry_mae_token, _ = setup_2

    # Joe Smith makes Marry Mae a Global Owner
    permission_change_data_1 = {'token': joe_smith_token, 'u_id': 1, 'permission_id': 1}
    response = requests.post(f'{BASE_URL}/admin/userpermission/change/v1', json = permission_change_data_1)
    assert response.status_code in [200, 201]

    # Marry Mae deletes Joe's message
    message_delete_input = {"token": marry_mae_token, "message_id": message_id} 
    response = requests.delete(f'{BASE_URL}/message/remove/v1', json = message_delete_input)
    assert response.status_code in [200, 201]

'''
Testing message/sendlater/v1 HTTP requests
'''

def test_sendlater_valid_messages(setup):

    joe_smith_token, joes_funland_channel_id, _ = setup

    # Joe Smith sends a message to Private channel "Joe's Reading Club", saying "Hi everyone!"
    message_send_input = {"token": joe_smith_token, "channel_id": joes_funland_channel_id, "message": "Hi everyone!"}
    response = requests.post(f'{BASE_URL}/message/send/v1', json = message_send_input)
    assert response.json()['message_id'] == 0

    message_later_time = int(datetime.now(timezone.utc).timestamp()) + 2
    # Joe Smith sends a message to Private channel "Joe's Reading Club", saying "Please pick your favourite book, ready for Monday 2pm."
    message_sendlater_input = {"token": joe_smith_token, "channel_id": joes_funland_channel_id, "message": "This message is sent later", 'time_sent': message_later_time}
    response = requests.post(f'{BASE_URL}/message/sendlater/v1', json = message_sendlater_input)
    assert response.json()['message_id'] == 1

    # Joe Smith sends another message to Private channel "Joe's Reading Club", saying "This message is sent now"}
    message_sendlater_input = {"token": joe_smith_token, "channel_id": joes_funland_channel_id, "message": "This message is sent now"}
    response = requests.post(f'{BASE_URL}/message/send/v1', json = message_sendlater_input)
    assert response.json()['message_id'] == 2

    time.sleep(3)

    # Joe wants to view all the channel's messages
    channel_messages_input = {'token': joe_smith_token, 'channel_id': joes_funland_channel_id, 'start': 0}
    response = requests.get(f'{BASE_URL}/channel/messages/v2', params = channel_messages_input).json()
    
    assert response['messages'][0]['message_id'] == 1
    assert response['messages'][1]['message_id'] == 2
    assert response['messages'][2]['message_id'] == 0

def test_sendlater_past_time(setup):

    joe_smith_token, joes_funland_channel_id, _ = setup

    # Joe Smith sends a message for later but the time is in the past
    message_send_input = {"token": joe_smith_token, "channel_id": joes_funland_channel_id, "message": "Hi there", "time_sent": int(datetime.now(timezone.utc).timestamp()) - 1}
    response = requests.post(f'{BASE_URL}/message/sendlater/v1', json = message_send_input)
    assert response.json()['code'] == INPUT_ERROR 

def test_sendlater_a_long_message(setup):

    joe_smith_token, joes_funland_channel_id, _ = setup

    # Joe Smith sends an long message (>1000 characters) to Private channel "Joe's Reading Club"
    message_send_input = {"token": joe_smith_token, "channel_id": joes_funland_channel_id, "message": "2"*1001, "time_sent": int(datetime.now(timezone.utc).timestamp()) + 1}
    response = requests.post(f'{BASE_URL}/message/sendlater/v1', json = message_send_input)
    assert response.json()['code'] == INPUT_ERROR 

def test_invalid_channel_message_sendlater(setup):

    joe_smith_token, _, _ = setup

    # Joe Smith sends a message to a channel that does not exist
    message_send_input = {"token": joe_smith_token, "channel_id": 300, "message": "Hi everyone!", "time_sent": int(datetime.now(timezone.utc).timestamp()) + 1}
    response = requests.post(f'{BASE_URL}/message/sendlater/v1', json = message_send_input)
    assert response.json()['code'] == INPUT_ERROR 

def test_unauthorised_message_sendlater(setup):

    _, joes_funland_channel_id, marry_mae_token = setup

    # Marry Mae attempts to send a message to channel she is not a part of
    message_send_input = {"token": marry_mae_token, "channel_id": joes_funland_channel_id, "message": "I'm a hacker", "time_sent": int(datetime.now(timezone.utc).timestamp()) + 1}
    response = requests.post(f'{BASE_URL}/message/sendlater/v1', json = message_send_input)
    assert response.json()['code'] == ACCESS_ERROR 

def test_unauthorised_message_sendlater_and_long_message(setup):

    _, joes_funland_channel_id, marry_mae_token = setup

    # Marry Mae attempts to send a long message (>1000 characters) to channel she is not a part of
    message_send_input = {"token": marry_mae_token, "channel_id": joes_funland_channel_id, "message": "Hi everyone!"*5000, "time_sent": int(datetime.now(timezone.utc).timestamp()) + 1}
    response = requests.post(f'{BASE_URL}/message/sendlater/v1', json = message_send_input)
    assert response.json()['code'] == ACCESS_ERROR 

def test_unauthorised_message_sendlater_and_invalid_channel(setup):

    _, _, marry_mae_token = setup

    # Marry Mae attempts to send a message to channel that does not exist
    message_send_input = {"token": marry_mae_token, "channel_id": 300, "message": "Hello everyone!", "time_sent": int(datetime.now(timezone.utc).timestamp()) + 1}
    response = requests.post(f'{BASE_URL}/message/send/v1', json = message_send_input)
    assert response.json()['code'] == INPUT_ERROR

'''
Testing message/sendlaterdm/v1 HTTP requests
'''

def test_sendlaterdm_valid_messages(setup_3):

    joe_smith_token, marry_mae_token, joe_marry_dm_id = setup_3

    # Joe Smith sends a message to DM, saying "Hi everyone!"
    message_send_input = {"token": joe_smith_token, "dm_id": joe_marry_dm_id, "message": "Hi everyone!"}
    response = requests.post(f'{BASE_URL}/message/senddm/v1', json = message_send_input)
    assert response.json()['message_id'] == 0
    
    message_later_time = int(datetime.now(timezone.utc).timestamp()) + 2
    # Marry Mae sends a message to DM, saying "Please pick your favourite book, ready for Monday 2pm."
    message_send_input = {"token": marry_mae_token, "dm_id": joe_marry_dm_id, "message": "Please pick your favourite book, ready for Monday 2pm.", 'time_sent': message_later_time}
    response = requests.post(f'{BASE_URL}/message/sendlaterdm/v1', json = message_send_input)
    assert response.json()['message_id'] == 1

    # Joe Smith sends a message to DM, saying "This message is sent now"
    message_send_input = {"token": joe_smith_token, "dm_id": joe_marry_dm_id, "message": "This message is sent now"}
    response = requests.post(f'{BASE_URL}/message/senddm/v1', json = message_send_input)
    
    assert response.json()['message_id'] == 2

    time.sleep(3)

    dm_messages_input = {'token': joe_smith_token, 'dm_id': joe_marry_dm_id, 'start': 0}
    response = requests.get(f'{BASE_URL}/dm/messages/v1', params = dm_messages_input).json()

    assert response['messages'][0]['message_id'] == 1
    assert response['messages'][1]['message_id'] == 2
    assert response['messages'][2]['message_id'] == 0
   
def test_sendlater_a_long_message_dm(setup_3):

    joe_smith_token, _, joe_marry_dm_id = setup_3

    # Joe Smith sends a very long message to DM (>1000 characters)
    message_sendlater_input = {"token": joe_smith_token, "dm_id": joe_marry_dm_id, "message": "1"*1001, "time_sent": int(datetime.now(timezone.utc).timestamp()) + 1}
    response = requests.post(f'{BASE_URL}/message/sendlaterdm/v1', json = message_sendlater_input)
    assert response.json()['code'] == INPUT_ERROR 


def test_sendlater_invalid_dm_id(setup_3):

    joe_smith_token, _, _ = setup_3

    # Joe Smith sends a message to a DM which does not exist
    message_sendlater_input = {"token": joe_smith_token, "dm_id": 300, "message": "Hi everyone!", "time_sent": int(datetime.now(timezone.utc).timestamp()) + 1}
    response = requests.post(f'{BASE_URL}/message/sendlaterdm/v1', json = message_sendlater_input)
    assert response.json()['code'] == INPUT_ERROR 

def test_unauthorised_user_sendlater_message_dm(setup_4):

    _, _, joe_marry_dm_id, _, darron_token = setup_4

    # Darron, who is not part of the DM, sends a message saying "Please pick your favourite book, ready for Monday 2pm."
    message_sendlater_input = {"token": darron_token, "dm_id": joe_marry_dm_id, "message": "Please pick your favourite book, ready for Monday 2pm.", "time_sent": int(datetime.now(timezone.utc).timestamp()) + 1}
    response = requests.post(f'{BASE_URL}/message/sendlaterdm/v1', json = message_sendlater_input)
    assert response.json()['code'] == ACCESS_ERROR
