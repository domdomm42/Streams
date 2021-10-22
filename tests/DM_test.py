import pytest
import requests
import jwt
from src.auth import auth_login_v1, auth_register_v1
from src.error import InputError, AccessError
from src.other import clear_v1
from src.config import *
from src.auth_auth_helpers import SECRET
from src.DM_functions import dm_create_v1, dm_list_v1, dm_remove_v1, dm_leave_v1, dm_messages_v1, dm_details_v1

import datetime
BASE_URL = url

@pytest.fixture
def setup():
    requests.delete(f'{BASE_URL}/clear/v1')

    #Create User Joe
    user_info = {'email': 'joe123@gmail.com', 'password': 'password', 'name_first': 'Joe', 'name_last': 'Smith'}
    joe_token = {'token': requests.post(f'{BASE_URL}/auth/register/v2', json = user_info).json()['token']}
    #Create User Marry
    user_info = {'email': 'marry123@gmail.com', 'password': 'password', 'name_first': 'Marry', 'name_last': 'Smith'}
    marry_token = {'token': requests.post(f'{BASE_URL}/auth/register/v2', json = user_info).json()['token']}
    #Create user Sam
    user_info = {'email': 'sam123@gmail.com', 'password': 'password', 'name_first': 'Sam', 'name_last': 'Smith'}
    sam_token = {'token': requests.post(f'{BASE_URL}/auth/register/v2', json = user_info).json()['token']}

    # Create a DM by Joe
    dm1_info = {'token': joe_token['token'], 'u_ids': [1]}
    dm1_id = {'dm_id': requests.post(f'{BASE_URL}/dm/create/v1', json = dm1_info).json()['dm_id']}

    return dm1_id['dm_id'], joe_token['token'], marry_token['token'], sam_token['token']


'''
INVALIDITY TESTS FOR DM_CREATE
'''

def test_dm_create_invalid_token():
    requests.delete(f'{BASE_URL}/clear/v1')

    u_ids = [0, 1, 2]
    dm_creation = {"token": '-1', "u_ids": u_ids}
    response_create = requests.post(f'{BASE_URL}/dm/create/v1', json = dm_creation)
    response_create_data = response_create.json()
    assert response_create_data['code'] == 403

def test_dm_create_invalid_list():
    requests.delete(f'{BASE_URL}/clear/v1')
    user_info = {'email': 'joe123@gmail.com', 'password': 'password', 'name_first': 'Joe', 'name_last': 'Smith'}
    joe_token = {'token': requests.post(f'{BASE_URL}/auth/register/v2', json = user_info).json()['token']}

    u_ids = [0, 1, 2]
    dm_creation = {"token": joe_token['token'], "u_ids": u_ids}
    response_create = requests.post(f'{BASE_URL}/dm/create/v1', json = dm_creation)
    response_create_data = response_create.json()
    assert response_create_data['code'] == 400

'''
INVALIDITY TESTS FOR DM_LIST
'''

def test_dm_list_invalid_token():
    requests.delete(f'{BASE_URL}/clear/v1')

    dm_list = {"token": '-1'}
    response_create = requests.get(f'{BASE_URL}/dm/list/v1', json = dm_list)
    response_create_data = response_create.json()
    assert response_create_data['code'] == 403


'''
INVALIDITY TESTS FOR DM_REMOVE
'''

def test_dm_remove_invalid_token():
    requests.delete(f'{BASE_URL}/clear/v1')

    dm_remove = {"token": '-1', "dm_id": 1}
    response_create = requests.delete(f'{BASE_URL}/dm/remove/v1', json = dm_remove)
    response_create_data = response_create.json()
    assert response_create_data['code'] == 403

def test_dm_invalid_dm_id(setup):
    _, joe, _, _ = setup

    dm_remove = {"token": joe, "dm_id": 1}
    response_create = requests.delete(f'{BASE_URL}/dm/remove/v1', json = dm_remove)
    response_create_data = response_create.json()
    assert response_create_data['code'] == 400

def test_dm_unoriginal_owner(setup):
    dm_id, _, marry, _ = setup
    dm_remove = {'token': marry, 'dm_id': dm_id}
    response_create = requests.delete(f'{BASE_URL}/dm/remove/v1', json = dm_remove)
    response_create_data = response_create.json()
    assert response_create_data['code'] == 403

'''
INVALIDITY TEST FOR DM_DETAILS
'''
def test_details_invalid_dm(setup):
    _, joe, _, _ = setup
    dm_details = {"token": joe, "dm_id": 1}
    response_create = requests.get(f'{BASE_URL}/dm/details/v1', json = dm_details)
    response_create_data = response_create.json()
    assert response_create_data['code'] == 400

def test_details_invalid_token():
    requests.delete(f'{BASE_URL}/clear/v1')

    dm_details = {"token": '-1', "dm_id": 1}
    response_create = requests.get(f'{BASE_URL}/dm/details/v1', json = dm_details)
    response_create_data = response_create.json()
    assert response_create_data['code'] == 403

def test_details_not_member(setup):
    _, _, _, sam = setup
    dm_details = {"token": sam, "dm_id": 0}
    response_create = requests.get(f'{BASE_URL}/dm/details/v1', json = dm_details)
    response_create_data = response_create.json()
    assert response_create_data['code'] == 403

'''
INVALIDITY TESTS FOR DM_LEAVE
'''
def test_leave_invalid_dm(setup):
    _, joe, _, _ = setup
    dm_leave = {"token": joe, "dm_id": 1}
    response_create = requests.post(f'{BASE_URL}/dm/leave/v1', json = dm_leave)
    response_create_data = response_create.json()
    assert response_create_data['code'] == 400

def test_leave_invalid_token():
    requests.delete(f'{BASE_URL}/clear/v1')

    dm_leave = {"token": '-1', "dm_id": 1}
    response_create = requests.post(f'{BASE_URL}/dm/leave/v1', json = dm_leave)
    response_create_data = response_create.json()
    assert response_create_data['code'] == 403

def test_leave_not_member(setup):
    _, _, _, sam = setup
    dm_leave = {"token": sam, "dm_id": 0}
    response_create = requests.post(f'{BASE_URL}/dm/leave/v1', json = dm_leave)
    response_create_data = response_create.json()
    assert response_create_data['code'] == 403

'''
INVALIDITY TESTS FOR DM_MESSAGES
'''

def test_messages_invalid_dm_id(setup):
    _, joe, _, _ = setup
    dm_messages = {"token": joe, "dm_id": 1, 'start': 0}
    response_create = requests.get(f'{BASE_URL}/dm/messages/v1', json = dm_messages)
    response_create_data = response_create.json()
    assert response_create_data['code'] == 400

def test_messages_invalid_token():
    requests.delete(f'{BASE_URL}/clear/v1')

    dm_messages = {"token": '-1', "dm_id": 1, 'start': 0}
    response_create = requests.get(f'{BASE_URL}/dm/messages/v1', json = dm_messages)
    response_create_data = response_create.json()
    assert response_create_data['code'] == 403

def test_messages_invalid_start(setup):
    _, joe, _, _ = setup

    dm_messages = {"token": joe, "dm_id": 0, 'start': 5}
    response_create = requests.get(f'{BASE_URL}/dm/messages/v1', json = dm_messages)
    response_create_data = response_create.json()
    assert response_create_data['code'] == 400

def test_messages_not_member(setup):
    _, _, _, sam = setup

    dm_messages = {"token": sam, "dm_id": 0, 'start': 0}
    response_create = requests.get(f'{BASE_URL}/dm/messages/v1', json = dm_messages)
    response_create_data = response_create.json()
    assert response_create_data['code'] == 403

'''
SAMPLE TESTING FOR DM_CREATE
'''

def test_simple_dm_create(setup):
    dm1, _, _, _= setup
    assert dm1 == 0

def test_multiple_dm_create(setup):
    dm1, _, marry, _= setup
    #create a DM by Joe
    dm1_info = {'token': marry, 'u_ids': [0, 1]}
    dm2 = {'dm_id': requests.post(f'{BASE_URL}/dm/create/v1', json = dm1_info).json()['dm_id']}
    assert dm1 == 0  
    assert dm2['dm_id'] == 1

'''
SAMPLE TESTING FOR DM_LIST
'''    
def test_simple_dm_list(setup):
    _, joe, _, _ = setup

    dm_list = {"token": joe}
    response_create = requests.get(f'{BASE_URL}/dm/list/v1', json = dm_list)
    response_create_data = response_create.json()
    assert response_create_data['dms'] == [
        {'dm_id': 0, 'name': 'joesmith, marrysmith'}
    ]

'''
SAMPLE TESTING FOR DM_REMOVE
''' 
def test_simple_dm_remove(setup):
    _, joe, marry, _ = setup

    dm_remove = {'token': joe, 'dm_id': 0}
    response_create = requests.delete(f'{BASE_URL}/dm/remove/v1', json = dm_remove)

    dm_list = {"token": marry}
    response_create = requests.get(f'{BASE_URL}/dm/list/v1', json = dm_list)
    response_create_data = response_create.json()
    assert response_create_data['dms'] == []
'''
SAMPLE TESTING FOR DM_DETAILS
'''
def test_simple_dm_details(setup):
    _, joe, _, _ = setup
    dm_details = {"token": joe, "dm_id": 0}
    response_create = requests.get(f'{BASE_URL}/dm/details/v1', json = dm_details)
    response_create_data = response_create.json()
    assert response_create_data['name'] == 'joesmith, marrysmith' 
    assert response_create_data['members'] == [
        {
            'u_id': 0,
            'email': 'joe123@gmail.com',
            'name_first': 'Joe', 
            'name_last': 'Smith',
            'handle_str':  'joesmith'
        },
        {
            'u_id': 1,
            'email': 'marry123@gmail.com',
            'name_first': 'Marry', 
            'name_last': 'Smith',
            'handle_str': 'marrysmith'
        }
    ]
'''
SAMPLE TESTING FOR DM_LEAVE
'''

def test_simple_dm_leave(setup):
    _, joe, _, _ = setup
    dm_leave = {"token": joe, "dm_id": 0}
    requests.post(f'{BASE_URL}/dm/leave/v1', json = dm_leave)

    dm_details = {"token": joe, "dm_id": 0}
    response_create = requests.get(f'{BASE_URL}/dm/details/v1', json = dm_details)
    response_create_data = response_create.json()
    assert response_create_data['name'] == 'joesmith, marrysmith' 
    assert response_create_data['members'] == [
        {
            'u_id': 1,
            'email': 'marry123@gmail.com',
            'name_first': 'Marry', 
            'name_last': 'Smith',
            'handle_str': 'marrysmith'
        }
    ]

'''
SAMPLE TESTING FOR DM_MESSAGES
'''

def test_simple_dm_messages(setup):
    _, joe, marry, _ = setup
    send_dm1 = {'token': joe, 'dm_id': 0, 'message': 'big tings bruv'}
    send_dm2 = {'token': marry, 'dm_id': 0, 'message': 'small tings bruv'}

    response_create = requests.post(f'{BASE_URL}/message/senddm/v1', json = send_dm1)
    timestamp1 = datetime.datetime.now().timestamp()
    message_id1 = response_create.json()

    response_create = requests.post(f'{BASE_URL}/message/senddm/v1', json = send_dm2)
    timestamp2 = datetime.datetime.now().timestamp()
    message_id2 = response_create.json()

    dm_messages = {"token": joe, "dm_id": 0, 'start': 0}
    response_create = requests.get(f'{BASE_URL}/dm/messages/v1', json = dm_messages)
    response_create_data = response_create.json()
    assert response_create_data['start'] == 0
    assert response_create_data['end'] == -1
    assert response_create_data['messages'] == [
        {
            'message_id': message_id1,
            'u_id': 0,
            'message': 'big tings bruv',
            'time_created': timestamp1
        },
        {
            'message_id': message_id2,
            'u_id': 1,
            'message': 'small tings bruv',
            'time_created': timestamp2
        }
    ]







