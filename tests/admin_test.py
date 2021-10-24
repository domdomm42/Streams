import pytest
import requests
from src.config import *

BASE_URL = url
ACCESS_ERROR = 403
INPUT_ERROR = 400

@pytest.fixture
def setup():
    requests.delete(f'{BASE_URL}/clear/v1')

    #Create User Marry Joe
    user_info = {'email': 'marryjoe123@gmail.com', 'password': 'password', 'name_first': 'Marry', 'name_last': 'Joe'}
    marryjoe_data = requests.post(f'{BASE_URL}/auth/register/v2', json = user_info).json()

    #Create User Marry Jane
    user_info = {"email": "marryjane@gmail.com", "password": "passwordJ", "name_first": "Marry", "name_last": "Jane"}
    marryjane_data = requests.post(f'{BASE_URL}/auth/register/v2', json = user_info).json()

    #Create user Marry
    user_info = {"email": "marry@gmail.com", "password": "passwordz", "name_first": "Marry", "name_last": "Tom"}
    marry_data = requests.post(f'{BASE_URL}/auth/register/v2', json = user_info).json()
 
    return marryjoe_data, marryjane_data, marry_data

def test_remove_admin(setup):
    # Register marryjoe and marry jane
    marryjoe_data, marryjane_data, _ = setup

    kick_data = {'token': marryjane_data['token'], 'u_id': marryjoe_data['auth_user_id']}
    
    # Remove marryjoe
    delete_data = requests.delete(f'{BASE_URL}/admin/user/remove/v1', json = kick_data)
    delete_data = delete_data.json()

    assert delete_data['code'] == ACCESS_ERROR

def test_change_permission(setup):
    marryjoe_data, marryjane_data, _ = setup

    permission_change_data_1 = {'token': marryjoe_data['token'], 'u_id': marryjane_data['auth_user_id'], 'permission_id': 1}
    permission_change_data_2 = {'token': marryjane_data['token'], 'u_id': marryjoe_data['auth_user_id'], 'permission_id': 2}

    # Promote Marry jane
    requests.post(f'{BASE_URL}/admin/userpermission/change/v1', json = permission_change_data_1)
    # Demote Marry Joe
    requests.post(f'{BASE_URL}/admin/userpermission/change/v1', json = permission_change_data_2)

    # Kick Marry Jane
    kick_data = {'token': marryjoe_data['token'], 'u_id': marryjane_data['auth_user_id']}
    
    delete_data = requests.delete(f'{BASE_URL}/admin/user/remove/v1', json = kick_data)
    delete_data = delete_data.json()

    assert delete_data['code'] == ACCESS_ERROR

def test_admin_change_permission_pass(setup):
    marryjoe_data, marryjane_data, _ = setup

    # Promote Marry Jane
    permission_change_data_1 = {'token': marryjoe_data['token'], 'u_id': marryjane_data['auth_user_id'], 'permission_id': 1}

    requests.post(f'{BASE_URL}/admin/userpermission/change/v1', json = permission_change_data_1)

def test_kick_pass(setup):
    marryjoe_data, marryjane_data, _ = setup

    # Kick Marry Jane
    kick_data = {'token': marryjoe_data['token'], 'u_id': marryjane_data['auth_user_id']}
    requests.delete(f'{BASE_URL}/admin/user/remove/v1', json = kick_data)

    print(requests.delete(f'{BASE_URL}/admin/user/remove/v1', json = kick_data).json())

def test_access_error1(setup):
    marryjoe_data, marryjane_data, _ = setup

    kick_data = {'token': marryjane_data['token'], 'u_id': marryjoe_data['auth_user_id']}

    # Remove Marry Joe
    response = requests.delete(f'{BASE_URL}/admin/user/remove/v1', json = kick_data)
    response = response.json()
    print(response)
    assert response['code'] == ACCESS_ERROR

def test_invalid_user(setup):
    marryjoe_data, marryjane_data, _ = setup

    kick_data = {'token': marryjoe_data['token'], 'u_id': marryjane_data['auth_user_id'] + 3}

    # Kick user with Invalid ID
    response = requests.delete(f'{BASE_URL}/admin/user/remove/v1', json = kick_data)
    response = response.json()
    print(response)
    assert response['code'] == INPUT_ERROR

def test_wrong_permission_ID(setup):
    marryjoe_data, marryjane_data, _ = setup

    permission_change_data_1 = {'token': marryjoe_data['token'], 'u_id': marryjane_data['auth_user_id'], 'permission_id': 3}

    # Change Marry Jane's permission to an invalid one
    data = requests.post(f'{BASE_URL}/admin/userpermission/change/v1', json = permission_change_data_1)
    data = data.json()
    assert data['code'] == INPUT_ERROR

def test_non_existent_user_id(setup):
    marryjoe_data, _, _ = setup

    permission_change_data_1 = {'token': marryjoe_data['token'], 'u_id': 10, 'permission_id': 1}

    # Change permision of a non-existent user
    data = requests.post(f'{BASE_URL}/admin/userpermission/change/v1', json = permission_change_data_1)
    data = data.json()
    assert data['code'] == INPUT_ERROR

def test_uid_only_global_owner(setup):
    marryjoe_data, marryjane_data, _ = setup

    permission_change_data_1 = {'token': marryjane_data['token'], 'u_id': marryjoe_data['auth_user_id'], 'permission_id': 2}

    # Attempt to change Permission of Marry Joe
    data = requests.post(f'{BASE_URL}/admin/userpermission/change/v1', json = permission_change_data_1)
    data = data.json()
    assert data['code'] == INPUT_ERROR

def test_auth_not_global_owner(setup):
    marryjoe_data, marryjane_data, marry_data = setup

    permission_change_data_1 = {'token': marryjoe_data['token'], 'u_id': marryjane_data['auth_user_id'], 'permission_id': 1}
    requests.post(f'{BASE_URL}/admin/userpermission/change/v1', json = permission_change_data_1)

    # Marry Tries to demote a user but she is not global owner
    permission_change_data_2 = {'token': marry_data['token'], 'u_id': marryjane_data['auth_user_id'], 'permission_id': 2}
    data = requests.post(f'{BASE_URL}/admin/userpermission/change/v1', json = permission_change_data_2).json()

    assert data['code'] == ACCESS_ERROR

def test_messages(setup):
    marryjoe_data, marryjane_data, _ = setup


    # Create a channel called domchannel
    channel_create_reg = {'token': marryjoe_data['token'], 'name': 'domchannel', 'is_public': True}
    channel_create_data = requests.post(f'{BASE_URL}/channels/create/v2', json = channel_create_reg)
    channel_create_data = channel_create_data.json()

    # Invite marry jane
    channel_inv_reg = {'token': marryjoe_data['token'], 'channel_id': channel_create_data['channel_id'], 'u_id': marryjane_data['auth_user_id']}
    channel_inv_data = requests.post(f'{BASE_URL}/channel/invite/v2', json = channel_inv_reg)
    channel_inv_data = channel_inv_data.json()

    # Marry jane sends message to channel
    message_send_reg = {'token': marryjane_data['token'], 'channel_id': channel_create_data['channel_id'], 'message': 'HelloWorld'}
    message_send_data = requests.post(f'{BASE_URL}/message/send/v1', json = message_send_reg)
    message_send_data = message_send_data.json()

    # Marry Joe sends message to channel
    message_send_reg = {'token': marryjoe_data['token'], 'channel_id': channel_create_data['channel_id'], 'message': 'HelloWorld'}
    message_send_data = requests.post(f'{BASE_URL}/message/send/v1', json = message_send_reg)
    message_send_data = message_send_data.json()

    # Marry Joe kicks out Marry Jane
    kick_data = {'token': marryjoe_data['token'], 'u_id': marryjane_data['auth_user_id']}
    response = requests.delete(f'{BASE_URL}/admin/user/remove/v1', json = kick_data)
    response = response.json()

def test_only_one_global_owner(setup):
    marryjoe_data, _, _ = setup

    kick_data = {'token': marryjoe_data['token'], 'u_id': marryjoe_data['auth_user_id']}

    # Marry Joe tries to kick herself
    response = requests.delete(f'{BASE_URL}/admin/user/remove/v1', json = kick_data)
    response = response.json()
    assert response['code'] == INPUT_ERROR






    



 

    


    






