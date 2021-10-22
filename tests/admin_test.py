import pytest
import requests
import jwt

from src.admin import admin_user_remove_v1, admin_userpermission_change_v1
from src.auth import auth_register_v1
from src.other import clear_v1
from src.error import InputError, AccessError
from src.config import *
from src.auth_auth_helpers import SECRET

BASE_URL = url

def test_remove_admin():
    requests.delete(f'{BASE_URL}/clear/v1')
    user_info_reg_1 = {"email": "marryjoe@gmail.com", "password": "password", "name_first": "Marry", "name_last": "Joe"}
    user_info_reg_2 = {"email": "marryjane@gmail.com", "password": "passwordJ", "name_first": "Marry", "name_last": "Jane"}

    response_data_1 = requests.post(f'{BASE_URL}/auth/register/v2', json = user_info_reg_1)
    response_data_2 = requests.post(f'{BASE_URL}/auth/register/v2', json = user_info_reg_2)

    response_data_1 = response_data_1.json()
    response_data_2 = response_data_2.json()

    kick_data = {'token': response_data_2['token'], 'u_id': response_data_1['auth_user_id']}
    
    delete_data = requests.delete(f'{BASE_URL}/admin/user/remove/v1', json = kick_data)
    delete_data = delete_data.json()
    #print(delete_data)

    assert delete_data['code'] == 403



def test_change_permission():
    requests.delete(f'{BASE_URL}/clear/v1')
    user_info_reg_1 = {"email": "marryjoe@gmail.com", "password": "password", "name_first": "Marry", "name_last": "Joe"}
    user_info_reg_2 = {"email": "marryjane@gmail.com", "password": "passwordJ", "name_first": "Marry", "name_last": "Jane"}

    response_data_1 = requests.post(f'{BASE_URL}/auth/register/v2', json = user_info_reg_1)
    response_data_2 = requests.post(f'{BASE_URL}/auth/register/v2', json = user_info_reg_2)

    response_data_1 = response_data_1.json()
    response_data_2 = response_data_2.json()

    permission_change_data_1 = {'token': response_data_1['token'], 'u_id': response_data_2['auth_user_id'], 'permission_id': 1}
    permission_change_data_2 = {'token': response_data_2['token'], 'u_id': response_data_1['auth_user_id'], 'permission_id': 2}

    requests.post(f'{BASE_URL}/admin/userpermission/change/v1', json = permission_change_data_1)
    requests.post(f'{BASE_URL}/admin/userpermission/change/v1', json = permission_change_data_2)

    kick_data = {'token': response_data_1['token'], 'u_id': response_data_2['auth_user_id']}
    
    delete_data = requests.delete(f'{BASE_URL}/admin/user/remove/v1', json = kick_data)
    delete_data = delete_data.json()
    #print(delete_data)

    assert delete_data['code'] == 403

def test_admin_change_permission_pass():
    requests.delete(f'{BASE_URL}/clear/v1')
    user_info_reg_1 = {"email": "marryjoe@gmail.com", "password": "password", "name_first": "Marry", "name_last": "Joe"}
    user_info_reg_2 = {"email": "marryjane@gmail.com", "password": "passwordJ", "name_first": "Marry", "name_last": "Jane"}

    response_data_1 = requests.post(f'{BASE_URL}/auth/register/v2', json = user_info_reg_1)
    response_data_2 = requests.post(f'{BASE_URL}/auth/register/v2', json = user_info_reg_2)

    response_data_1 = response_data_1.json()
    response_data_2 = response_data_2.json()

    permission_change_data_1 = {'token': response_data_1['token'], 'u_id': response_data_2['auth_user_id'], 'permission_id': 1}

    requests.post(f'{BASE_URL}/admin/userpermission/change/v1', json = permission_change_data_1)

def test_kick_pass():
    requests.delete(f'{BASE_URL}/clear/v1')
    user_info_reg_1 = {"email": "marryjoe@gmail.com", "password": "password", "name_first": "Marry", "name_last": "Joe"}
    user_info_reg_2 = {"email": "marryjane@gmail.com", "password": "passwordJ", "name_first": "Marry", "name_last": "Jane"}

    response_data_1 = requests.post(f'{BASE_URL}/auth/register/v2', json = user_info_reg_1)
    response_data_2 = requests.post(f'{BASE_URL}/auth/register/v2', json = user_info_reg_2)

    response_data_1 = response_data_1.json()
    response_data_2 = response_data_2.json()

    kick_data = {'token': response_data_1['token'], 'u_id': response_data_2['auth_user_id']}
    requests.delete(f'{BASE_URL}/admin/user/remove/v1', json = kick_data)

    print(requests.delete(f'{BASE_URL}/admin/user/remove/v1', json = kick_data).json())

def test_access_error1():
    requests.delete(f'{BASE_URL}/clear/v1')
    user_info_reg_1 = {"email": "marryjoe@gmail.com", "password": "password", "name_first": "Marry", "name_last": "Joe"}
    user_info_reg_2 = {"email": "marryjane@gmail.com", "password": "passwordJ", "name_first": "Marry", "name_last": "Jane"}

    response_data_1 = requests.post(f'{BASE_URL}/auth/register/v2', json = user_info_reg_1)
    response_data_2 = requests.post(f'{BASE_URL}/auth/register/v2', json = user_info_reg_2)

    response_data_1 = response_data_1.json()
    response_data_2 = response_data_2.json()

    kick_data = {'token': response_data_2['token'], 'u_id': response_data_1['auth_user_id']}
    response = requests.delete(f'{BASE_URL}/admin/user/remove/v1', json = kick_data)
    response = response.json()
    print(response)
    assert response['code'] == 403


def test_invalid_user():
    requests.delete(f'{BASE_URL}/clear/v1')
    user_info_reg_1 = {"email": "marryjoe@gmail.com", "password": "password", "name_first": "Marry", "name_last": "Joe"}
    user_info_reg_2 = {"email": "marryjane@gmail.com", "password": "passwordJ", "name_first": "Marry", "name_last": "Jane"}

    response_data_1 = requests.post(f'{BASE_URL}/auth/register/v2', json = user_info_reg_1)
    response_data_2 = requests.post(f'{BASE_URL}/auth/register/v2', json = user_info_reg_2)

    response_data_1 = response_data_1.json()
    response_data_2 = response_data_2.json()

    kick_data = {'token': response_data_1['token'], 'u_id': response_data_2['auth_user_id'] + 3}
    response = requests.delete(f'{BASE_URL}/admin/user/remove/v1', json = kick_data)
    response = response.json()
    print(response)
    assert response['code'] == 400


def test_wrong_permission_ID():
    requests.delete(f'{BASE_URL}/clear/v1')
    user_info_reg_1 = {"email": "marryjoe@gmail.com", "password": "password", "name_first": "Marry", "name_last": "Joe"}
    user_info_reg_2 = {"email": "marryjane@gmail.com", "password": "passwordJ", "name_first": "Marry", "name_last": "Jane"}

    response_data_1 = requests.post(f'{BASE_URL}/auth/register/v2', json = user_info_reg_1)
    response_data_2 = requests.post(f'{BASE_URL}/auth/register/v2', json = user_info_reg_2)

    response_data_1 = response_data_1.json()
    response_data_2 = response_data_2.json()

    permission_change_data_1 = {'token': response_data_1['token'], 'u_id': response_data_2['auth_user_id'], 'permission_id': 3}

    data = requests.post(f'{BASE_URL}/admin/userpermission/change/v1', json = permission_change_data_1)
    data = data.json()
    assert data['code'] == 400

def test_non_existent_user_id():
    requests.delete(f'{BASE_URL}/clear/v1')
    user_info_reg_1 = {"email": "marryjoe@gmail.com", "password": "password", "name_first": "Marry", "name_last": "Joe"}
    user_info_reg_2 = {"email": "marryjane@gmail.com", "password": "passwordJ", "name_first": "Marry", "name_last": "Jane"}

    response_data_1 = requests.post(f'{BASE_URL}/auth/register/v2', json = user_info_reg_1)
    response_data_2 = requests.post(f'{BASE_URL}/auth/register/v2', json = user_info_reg_2)

    response_data_1 = response_data_1.json()
    response_data_2 = response_data_2.json()

    permission_change_data_1 = {'token': response_data_1['token'], 'u_id': 10, 'permission_id': 1}

    data = requests.post(f'{BASE_URL}/admin/userpermission/change/v1', json = permission_change_data_1)
    data = data.json()
    assert data['code'] == 400

def test_uid_only_global_owner():
    requests.delete(f'{BASE_URL}/clear/v1')
    user_info_reg_1 = {"email": "marryjoe@gmail.com", "password": "password", "name_first": "Marry", "name_last": "Joe"}
    user_info_reg_2 = {"email": "marryjane@gmail.com", "password": "passwordJ", "name_first": "Marry", "name_last": "Jane"}

    response_data_1 = requests.post(f'{BASE_URL}/auth/register/v2', json = user_info_reg_1)
    response_data_2 = requests.post(f'{BASE_URL}/auth/register/v2', json = user_info_reg_2)

    response_data_1 = response_data_1.json()
    response_data_2 = response_data_2.json()

    permission_change_data_1 = {'token': response_data_2['token'], 'u_id': response_data_1['auth_user_id'], 'permission_id': 2}

    data = requests.post(f'{BASE_URL}/admin/userpermission/change/v1', json = permission_change_data_1)
    data = data.json()
    assert data['code'] == 400

def test_auth_not_global_owner():
    requests.delete(f'{BASE_URL}/clear/v1')
    user_info_reg_1 = {"email": "marryjoe@gmail.com", "password": "password", "name_first": "Marry", "name_last": "Joe"}
    user_info_reg_2 = {"email": "marryjane@gmail.com", "password": "passwordJ", "name_first": "Marry", "name_last": "Jane"}
    user_info_reg_3 = {"email": "marry@gmail.com", "password": "passwordz", "name_first": "Marry", "name_last": "Tom"}


    response_data_1 = requests.post(f'{BASE_URL}/auth/register/v2', json = user_info_reg_1)
    response_data_2 = requests.post(f'{BASE_URL}/auth/register/v2', json = user_info_reg_2)
    response_data_3 = requests.post(f'{BASE_URL}/auth/register/v2', json = user_info_reg_3)

    response_data_1 = response_data_1.json()
    response_data_2 = response_data_2.json()
    response_data_3 = response_data_3.json()

    permission_change_data_1 = {'token': response_data_1['token'], 'u_id': response_data_2['auth_user_id'], 'permission_id': 1}
    requests.post(f'{BASE_URL}/admin/userpermission/change/v1', json = permission_change_data_1)

    permission_change_data_2 = {'token': response_data_3['token'], 'u_id': response_data_2['auth_user_id'], 'permission_id': 2}
    data = requests.post(f'{BASE_URL}/admin/userpermission/change/v1', json = permission_change_data_2).json()

    assert data['code'] == 403

def test_messages():
    requests.delete(f'{BASE_URL}/clear/v1')
    user_info_reg_1 = {"email": "marryjoe@gmail.com", "password": "password", "name_first": "Marry", "name_last": "Joe"}
    user_info_reg_2 = {"email": "marryjane@gmail.com", "password": "passwordJ", "name_first": "Marry", "name_last": "Jane"}

    response_data_1 = requests.post(f'{BASE_URL}/auth/register/v2', json = user_info_reg_1)
    response_data_2 = requests.post(f'{BASE_URL}/auth/register/v2', json = user_info_reg_2)

    response_data_1 = response_data_1.json()
    response_data_2 = response_data_2.json()


    channel_create_reg = {'token': response_data_1['token'], 'name': 'domchannel', 'is_public': True}
    channel_create_data = requests.post(f'{BASE_URL}/channels/create/v2', json = channel_create_reg)
    channel_create_data = channel_create_data.json()

    channel_inv_reg = {'token': response_data_1['token'], 'channel_id': channel_create_data['channel_id'], 'u_id': response_data_2['auth_user_id']}
    channel_inv_data = requests.post(f'{BASE_URL}/channel/invite/v2', json = channel_inv_reg)
    channel_inv_data = channel_inv_data.json()

    
    message_send_reg = {'token': response_data_2['token'], 'channel_id': channel_create_data['channel_id'], 'message': 'HelloWorld'}
    message_send_data = requests.post(f'{BASE_URL}/message/send/v1', json = message_send_reg)
    message_send_data = message_send_data.json()

    kick_data = {'token': response_data_1['token'], 'u_id': response_data_2['auth_user_id']}
    response = requests.delete(f'{BASE_URL}/admin/user/remove/v1', json = kick_data)
    response = response.json()










    



 

    


    






