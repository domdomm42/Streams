from src.admin import admin_user_remove_v1, admin_userpermission_change_v1
import jwt
import requests
from src.error import InputError, AccessError
from src.config import *
from src.auth_auth_helpers import SECRET

BASE_URL = url

def test_remove_admin():
    requests.delete(f'{BASE_URL}/clear/v1')
    user_info_reg_1 = {"email": "marryjoe@gmail.com", "password": "password", "name_first": "Marry", "name_last": "Joe"}
    user_info_reg_2 = {"email": "marryjane@gmail.com", "password": "passwordJ", "name_first": "Marry", "name_last": "Jane"}

    response_data_1 = requests.post(f'{BASE_URL}/auth/register/v2', json = user_info_reg_1)
    response_data_2 = requests.post(f'{BASE_URL}/auth/register/v2', json = user_info_reg_1)

    response_data_1 = response_data_1.json()
    response_data_2 = response_data_2.json()

    user_2_data = response_data_2.json()

    user_2_data = {"token": response_data_1['token'], "user_id": response_data_2['auth_user_id'], "permission_id": 1} 

    requests.post(f'{BASE_URL}admin/userpermission/change/v1', json = user_2_data)


    kick_data = {'token': response_data_2['token'], 'user_id': response_data_1['user_id']}
    requests.post(f'{BASE_URL}admin_user_remove_v1', json = kick_data)

    kick_data = {'token': response_data_2['token'], 'user_id': response_data_2}

    # return_value = return_value.json()
    # assert return_value['code'] == 403


