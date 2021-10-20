import pytest
import requests
import jwt
from src.auth import auth_login_v1, auth_register_v1
from src.error import InputError, AccessError
from src.other import clear_v1
from src.config import *
from src.auth_auth_helpers import SECRET
import src.direct_messages

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

    # Set User handles for each User
    # user_sethandle(joe_token, 'Joe')
    # user_sethandle(marry_token, 'Marry')
    # user_sethandle(sam_token, 'Sam')

    # Create a DM by Joe
    dm1_info = {'token': joe_token, 'u_ids': [0, 1]}
    dm_id = {'dm_id': requests.post(f'{BASE_URL}/dm/create/v1', json = dm_info).json()['dm_id']}

    return dm_id, joe_token, marry_token, sam_token


'''
INVALIDITY TESTS FOR DM_CREATE
'''
u_ids = [0, 1, 2]
def dm_create_invalid_token_test():
    requests.delete(f'{BASE_URL}/clear/v1')

    dm_creation = {"token": '-1', "u_ids": u_ids}
    response_create = requests.post(f'{BASE_URL}/dm/create/v1', json = dm_creation)
    response_create_data = response_create.json()
    assert response_create_data['code'] == 403

def dm_create_invalid_list_test():
    requests.delete(f'{BASE_URL}/clear/v1')
    user_info = {'email': 'joe123@gmail.com', 'password': 'password', 'name_first': 'Joe', 'name_last': 'Smith'}
    joe_token = {'token': requests.post(f'{BASE_URL}/auth/register/v2', json = user_info).json()['token']}

    dm_creation = {"token": joe_token, "u_ids": u_ids}
    response_create = requests.post(f'{BASE_URL}/dm/create/v1', json = dm_creation)
    response_create_data = response_create.json()
    assert response_create_data['code'] == 400    

'''
INVALIDITY TESTS FOR DM_LIST
'''

def dm_list_invalid_token_test():
    requests.delete(f'{BASE_URL}/clear/v1')

    dm_list = {"token": '-1'}
    response_create = requests.post(f'{BASE_URL}/dm/list/v1', json = dm_list)
    response_create_data = response_create.json()
    assert response_create_data['code'] == 403


'''
INVALIDITY TESTS FOR DM_REMOVE
'''

def dm_remove_invalid_token_test():
    requests.delete(f'{BASE_URL}/clear/v1')

    dm_remove = {"token": '-1', "dm_id": '1'}
    response_create = requests.post(f'{BASE_URL}/dm/remove/v1', json = dm_remove)
    response_create_data = response_create.json()
    assert response_create_data['code'] == 403

def dm_invalid_dm_id_test(setup):
    _, joe, _, _ = setup

    dm_remove = {"token": joe, "dm_id": '1'}
    response_create = requests.post(f'{BASE_URL}/dm/remove/v1', json = dm_remove)
    response_create_data = response_create.json()
    assert response_create_data['code'] == 400

def dm_unoriginal_owner_test(setup):
    dm_id, _, marry, _ = setup
    dm_remove = {'token': marry, 'dm_id': dm_id}
    response_create = requests.post(f'{BASE_URL}/dm/remove/v1', json = dm_remove)
    response_create_data = response_create.json()
    assert response_create_data['code'] == 403

'''
INVALIDITY TEST FOR DM_DETAILS
'''
def details_invalid_dm_test(setup):
    _, joe, _, _ = setup
    dm_details = {"token": joe, "dm_id": '1'}
    response_create = requests.post(f'{BASE_URL}/dm/details/v1', json = dm_details)
    response_create_data = response_create.json()
    assert response_create_data['code'] == 400

def details_invalid_token_test():
    requests.delete(f'{BASE_URL}/clear/v1')

    dm_details = {"token": '-1', "dm_id": '1'}
    response_create = requests.post(f'{BASE_URL}/dm/details/v1', json = dm_details)
    response_create_data = response_create.json()
    assert response_create_data['code'] == 403

def details_not_member_test(setup):
    _, _, _, sam = setup
    dm_details = {"token": sam, "dm_id": '0'}
    response_create = requests.post(f'{BASE_URL}/dm/details/v1', json = dm_details)
    response_create_data = response_create.json()
    assert response_create_data['code'] == 403

'''
INVALIDITY TESTS FOR DM_LEAVE
'''
def leave_invalid_dm_test(setup):
    _, joe, _, _ = setup
    dm_leave = {"token": joe, "dm_id": '1'}
    response_create = requests.post(f'{BASE_URL}/dm/leave/v1', json = dm_leave)
    response_create_data = response_create.json()
    assert response_create_data['code'] == 400

def leave_invalid_token_test():
    requests.delete(f'{BASE_URL}/clear/v1')

    dm_leave = {"token": '-1', "dm_id": '1'}
    response_create = requests.post(f'{BASE_URL}/dm/leave/v1', json = dm_leave)
    response_create_data = response_create.json()
    assert response_create_data['code'] == 403

def leave_not_member_test(setup):
    _, _, _, sam = setup
    dm_leave = {"token": sam, "dm_id": '0'}
    response_create = requests.post(f'{BASE_URL}/dm/leave/v1', json = dm_leave)
    response_create_data = response_create.json()
    assert response_create_data['code'] == 403

'''
INVALIDITY TESTS FOR DM_MESSAGES
'''

def messages_invalid_dm_id_test(setup):
    _, joe, _, _ = setup
    dm_messages = {"token": joe, "dm_id": '1', 'start': 0}
    response_create = requests.post(f'{BASE_URL}/dm/messages/v1', json = dm_messages)
    response_create_data = response_create.json()
    assert response_create_data['code'] == 400

def messages_invalid_token_test():
    requests.delete(f'{BASE_URL}/clear/v1')

    dm_messages = {"token": '-1', "dm_id": '1', 'start': 0}
    response_create = requests.post(f'{BASE_URL}/dm/messages/v1', json = dm_messages)
    response_create_data = response_create.json()
    assert response_create_data['code'] == 403

def messages_invalid_start_test(setup):
    _, joe, _, _ = setup

    dm_messages = {"token": joe, "dm_id": '0', 'start': 5}
    response_create = requests.post(f'{BASE_URL}/dm/messages/v1', json = dm_messages)
    response_create_data = response_create.json()
    assert response_create_data['code'] == 400

def messages_not_member_test(setup):
    _, _, _, sam = setup

    dm_messages = {"token": sam, "dm_id": '0', 'start': 0}
    response_create = requests.post(f'{BASE_URL}/dm/messages/v1', json = dm_messages)
    response_create_data = response_create.json()
    assert response_create_data['code'] == 403



'''
SAMPLE TESTING FOR DM_CREATE
'''

def simple_dm_create_test(setup):
    assert setup == 0

def multiple_dm_create_test(setup):
    dm1, _, marry, _= setup
    #create a DM by Joe
    dm1_info = {'token': marry, 'u_ids': [0, 1]}
    dm2 = {'dm_id': requests.post(f'{BASE_URL}/dm/create/v1', json = dm_info).json()['dm_id']}
    assert dm1 == 0 and assert dm2 == 1

'''
SAMPLE TESTING FOR DM_LIST
'''    
def simple_dm_list_test(setup):
    _, joe, _, _ = setup

    dm_list = {"token": joe}
    response_create = requests.post(f'{BASE_URL}/dm/list/v1', json = dm_list)
    response_create_data = response_create.json()
    assert response_create_data['dms'] = {[
        {'dm_id': 0, 'dm_name': 'joesmith, marrysmith'}
    ]}

'''
SAMPLE TESTING FOR DM_REMOVE
''' 
def simple_dm_remove_test(setup):
    _, joe, marry, _ = setup

    dm_remove = {'token': joe, 'dm_id': '0'}
    response_create = requests.post(f'{BASE_URL}/dm/remove/v1', json = dm_remove)

    dm_list = {"token": marry}
    response_create = requests.post(f'{BASE_URL}/dm/list/v1', json = dm_list)
    response_create_data = response_create.json()
    assert response_create_data['dms'] = {[]}
'''
SAMPLE TESTING FOR DM_DETAILS
'''
def simple_dm_details_test(setup):
    _, joe, _, _ = setup
    dm_details = {"token": joe, "dm_id": '0'}
    response_create = requests.post(f'{BASE_URL}/dm/details/v1', json = dm_details)
    response_create_data = response_create.json()
    assert response_create_data['name'] == 'Joe, Marry, Sam' 
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

def simple_dm_remove_test(setup):
    _, joe, _, _ = setup
    
