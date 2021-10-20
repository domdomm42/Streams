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
    print(delete_data)

    assert delete_data['code'] == 400



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

    response_data_permissions_1 = requests.post(f'{BASE_URL}/admin/userpermission/change/v1', json = permission_change_data_1)
    response_data_permissions_2 = requests.post(f'{BASE_URL}/admin/userpermission/change/v1', json = permission_change_data_2)

    kick_data = {'token': response_data_1['token'], 'u_id': response_data_2['auth_user_id']}
    
    delete_data = requests.delete(f'{BASE_URL}/admin/user/remove/v1', json = kick_data)
    delete_data = delete_data.json()
    print(delete_data)

    assert delete_data['code'] == 400

