import pytest
from src.channel import channel_details_v1, channel_join_v1
from src.error import InputError, AccessError
from src.auth import auth_login_v1, auth_register_v1
from src.channel import channel_invite_v1, channel_join_v1, channel_details_v1, channel_leave_v1, channel_addowner_v1, channel_removeowner_v1
from src.other import clear_v1
import requests

from src.users import user_profile_sethandle_v1
from src.auth_auth_helpers import check_and_get_user_id
from src.config import *
BASE_URL = url

@pytest.fixture
def setup():
    #clean data_store
    requests.delete(f'{BASE_URL}/clear/v1')
    #register for joe 
    user_joe_info_reg = {"email": "joe123@gmail.com", "password": "password", "name_first": "Joe", "name_last": "Smith"}
    user_joe_info_login = {"email": "joe123@gmail.com", "password": "password"}
    requests.post(f'{BASE_URL}/auth/register/v2', json = user_joe_info_reg)
    #register for marry
    user_marry_info_reg = {"email": "marryjoe222@gmail.com", "password": "passwordM", "name_first": "Marry", "name_last": "Joe"}
    user_marry_info_login = {"email": "marryjoe222@gmail.com", "password": "passwordM"}
    requests.post(f'{BASE_URL}/auth/register/v2', json = user_marry_info_reg)
    #log them in
    response_log_joe = requests.post(f'{BASE_URL}/auth/login/v2', json = user_joe_info_login)
    response_log_marry = requests.post(f'{BASE_URL}/auth/login/v2', json = user_marry_info_login)
    response_log_joe = response_log_joe.json()
    response_log_marry = response_log_marry.json()
    #create channel for them 
    #joe create a public channel called Joe
    create_info_joe = {"token": response_log_joe["token"], "name": "Joe", "is_public": True}
    channel_id_joe = requests.post(f'{BASE_URL}/channels/create/v2', json = create_info_joe)
    channel_id_joe = channel_id_joe.json()
    #marry create a private channel called Marry
    create_info_marry = {"token": response_log_marry["token"], "name": "Marry", "is_public": False}
    channel_id_marry = requests.post(f'{BASE_URL}/channels/create/v2', json = create_info_marry)
    channel_id_marry = channel_id_marry.json()
    return channel_id_joe, channel_id_marry, response_log_joe, response_log_marry



# if the channel is not refer to a valid channel, it will return 400 error
def test_invalid_channel_id_leave(setup):
    _, _, response_log_joe, _ = setup
    channel_leave_info = {"token": response_log_joe['token'], "channel_id": "100"}
    response = requests.post(f'{BASE_URL}/channel/leave/v1', json = channel_leave_info)
    response_data = response.json()
    assert response_data['code'] == 400

def test_invalid_channel_id_add(setup):
    _, _, response_log_joe, _ = setup
    channel_add_info = {"token": response_log_joe['token'], "channel_id": "100", "u_id": response_log_joe['auth_user_id']}
    response = requests.post(f'{BASE_URL}/channel/addowner/v1', json = channel_add_info)
    response_data = response.json()
    assert response_data['code'] == 400

def test_invalid_channel_id_remove(setup):
    _, _, response_log_joe, _ = setup
    channel_remove_info = {"token": response_log_joe['token'], "channel_id": "100", "u_id": response_log_joe['auth_user_id']}
    response = requests.post(f'{BASE_URL}/channel/removeowner/v1', json = channel_remove_info)
    response_data = response.json()
    assert response_data['code'] == 400

#channel_id is valid and the authorised user is not a member of the channelm it will return 403 error
def test_no_member_channel_leave(setup):
    channel_id_joe, _, _, response_log_marry = setup
    channel_leave_info = {"token": response_log_marry['token'], "channel_id": channel_id_joe['channel_id']}
    response = requests.post(f'{BASE_URL}/channel/leave/v1', json = channel_leave_info)
    response_data = response.json()
    assert response_data['code'] == 403

#test invalid u_id ,it should return 400
def test_invalid_u_id_add(setup):
    channel_id_joe, _, response_log_joe, _ = setup
    channel_add_info = {"token": response_log_joe['token'], "channel_id": channel_id_joe['channel_id'], "u_id": "100"}
    response = requests.post(f'{BASE_URL}/channel/addowner/v1', json = channel_add_info)
    response_data = response.json()
    assert response_data['code'] == 400

def test_invalid_u_id_remove(setup):
    channel_id_joe, _, response_log_joe, _ = setup
    channel_remove_info = {"token": response_log_joe['token'], "channel_id": channel_id_joe['channel_id'], "u_id": "100"}
    response = requests.post(f'{BASE_URL}/channel/removeowner/v1', json = channel_remove_info)
    response_data = response.json()
    assert response_data['code'] == 400

def test_u_id_not_member_add(setup):
    channel_id_joe, _, response_log_joe, response_log_marry = setup
    channel_add_info = {"token": response_log_joe['token'], "channel_id": channel_id_joe['channel_id'], "u_id": response_log_marry['auth_user_id']}
    response = requests.post(f'{BASE_URL}/channel/addowner/v1', json = channel_add_info)
    response_data = response.json()
    assert response_data['code'] == 400



def test_owner_member_add(setup):
    channel_id_joe, _, response_log_joe, _ = setup
    channel_add_info = {"token": response_log_joe['token'], "channel_id": channel_id_joe['channel_id'], "u_id": response_log_joe['auth_user_id']}
    response = requests.post(f'{BASE_URL}/channel/addowner/v1', json = channel_add_info)
    response_data = response.json()
    assert response_data['code'] == 400

def test_owner_permission_add(setup):
    channel_id_joe, _, _, response_log_marry = setup
    user_milly_reg = {"email": "milly3@gmail.com", "password": "passwordS", "name_first": "Milly", "name_last": "Mae"}
    milly_token = requests.post(f'{BASE_URL}/auth/register/v2', json = user_milly_reg).json()['token']
    channel_join_info1 = {"token": milly_token, "channel_id": channel_id_joe['channel_id']}
    requests.post(f'{BASE_URL}/channel/join/v2', json = channel_join_info1)
    channel_join_info2 = {"token": response_log_marry['token'], "channel_id": channel_id_joe['channel_id']}
    requests.post(f'{BASE_URL}/channel/join/v2', json = channel_join_info2)
    channel_add_info = {"token": milly_token, "channel_id": channel_id_joe['channel_id'], "u_id": response_log_marry['auth_user_id']}
    response = requests.post(f'{BASE_URL}/channel/addowner/v1', json = channel_add_info)
    response_data = response.json()
    assert response_data['code'] == 403

def test_no_owner_remove(setup):
    channel_id_joe, _, response_log_joe, response_log_marry = setup
    channel_join_info = {"token": response_log_marry['token'], "channel_id": channel_id_joe['channel_id']}
    requests.post(f'{BASE_URL}/channel/join/v2', json = channel_join_info)
    channel_remove_info = {"token": response_log_joe['token'], "channel_id": channel_id_joe['channel_id'], "u_id": response_log_marry['auth_user_id']}
    response = requests.post(f'{BASE_URL}/channel/removeowner/v1', json = channel_remove_info)
    response_data = response.json()
    assert response_data['code'] == 400

def test_last_owner_remove(setup):
    channel_id_joe, _, response_log_joe, _ = setup
    channel_remove_info = {"token": response_log_joe['token'], "channel_id": channel_id_joe['channel_id'], "u_id": response_log_joe['auth_user_id']}
    response = requests.post(f'{BASE_URL}/channel/removeowner/v1', json = channel_remove_info)
    response_data = response.json()
    assert response_data['code'] == 400

def test_owner_permission_remove(setup):
    channel_id_joe, _, response_log_joe, response_log_marry = setup
    channel_join_info = {"token": response_log_marry['token'], "channel_id": channel_id_joe['channel_id']}
    requests.post(f'{BASE_URL}/channel/join/v2', json = channel_join_info)
    channel_remove_info = {"token": response_log_marry['token'], "channel_id": channel_id_joe['channel_id'], "u_id": response_log_joe['auth_user_id']}
    response = requests.post(f'{BASE_URL}/channel/removeowner/v1', json = channel_remove_info)
    response_data = response.json()
    assert response_data['code'] == 403

#==========================================
#    valid input test
#==========================================

def test_valid_input_leave(setup):
    channel_id_joe, _, response_log_joe, response_log_marry = setup
    channel_join_info = {"token": response_log_marry['token'], "channel_id": channel_id_joe['channel_id']}
    requests.post(f'{BASE_URL}/channel/join/v2', json = channel_join_info)
    channel_leave_info = {"token": response_log_joe['token'], "channel_id": channel_id_joe['channel_id']}
    requests.post(f'{BASE_URL}/channel/leave/v1', json = channel_leave_info)
    channel_details_info = {"token": response_log_marry['token'], "channel_id": channel_id_joe['channel_id']}

    response = requests.get(f'{BASE_URL}/channel/details/v2', json = channel_details_info)
    details = response.json()
    assert details == {
        'all_members': [{   'email': 'marryjoe222@gmail.com',
                            'handle_str': 'marryjoe',
                            'name_first': 'Marry',
                            'name_last': 'Joe',
                            'u_id': 1}],
        'is_public': True,
        'name': 'Joe',
        'owner_members': [],
    }

def test_valid_input_add(setup):
    channel_id_joe, _, response_log_joe, response_log_marry = setup
    channel_join_info = {"token": response_log_marry['token'], "channel_id": channel_id_joe['channel_id']}
    requests.post(f'{BASE_URL}/channel/join/v2', json = channel_join_info)
    channel_add_info = {"token": response_log_joe['token'], "channel_id": channel_id_joe['channel_id'], "u_id": response_log_marry['auth_user_id']}
    requests.post(f'{BASE_URL}/channel/addowner/v1', json = channel_add_info)
    channel_details_info = {"token": response_log_marry['token'], "channel_id": channel_id_joe['channel_id']}

    response = requests.get(f'{BASE_URL}/channel/details/v2', json = channel_details_info)
    details = response.json()
    assert details == {
        'all_members': [{'email': 'joe123@gmail.com',
                        'handle_str': 'joesmith',
                        'name_first': 'Joe',
                        'name_last': 'Smith',
                        'u_id': 0},
                        {'email': 'marryjoe222@gmail.com',
                        'handle_str': 'marryjoe',
                        'name_first': 'Marry',
                        'name_last': 'Joe',
                        'u_id': 1}],
        'is_public': True,
        'name': 'Joe',
        'owner_members': [{'email': 'joe123@gmail.com',
                            'handle_str': 'joesmith',
                            'name_first': 'Joe',
                            'name_last': 'Smith',
                            'u_id': 0},
                        {'email': 'marryjoe222@gmail.com',
                            'handle_str': 'marryjoe',
                            'name_first': 'Marry',
                            'name_last': 'Joe',
                            'u_id': 1}],
    }
def test_valid_input_remove(setup):
    channel_id_joe, _, response_log_joe, response_log_marry = setup
    channel_join_info = {"token": response_log_marry['token'], "channel_id": channel_id_joe['channel_id']}
    requests.post(f'{BASE_URL}/channel/join/v2', json = channel_join_info)
    channel_test_info = {"token": response_log_joe['token'], "channel_id": channel_id_joe['channel_id'], "u_id": response_log_marry['auth_user_id']}
    requests.post(f'{BASE_URL}/channel/addowner/v1', json = channel_test_info)
    channel_details_info = {"token": response_log_marry['token'], "channel_id": channel_id_joe['channel_id']}
    requests.post(f'{BASE_URL}/channel/removeowner/v1', json = channel_test_info)
    
    response = requests.get(f'{BASE_URL}/channel/details/v2', json = channel_details_info)
    details = response.json()
    assert details == {
        'all_members': [{'email': 'joe123@gmail.com',
                        'handle_str': 'joesmith',
                        'name_first': 'Joe',
                        'name_last': 'Smith',
                        'u_id': 0},
                        {'email': 'marryjoe222@gmail.com',
                        'handle_str': 'marryjoe',
                        'name_first': 'Marry',
                        'name_last': 'Joe',
                        'u_id': 1}],
        'is_public': True,
        'name': 'Joe',
        'owner_members': [{'email': 'joe123@gmail.com',
                            'handle_str': 'joesmith',
                            'name_first': 'Joe',
                            'name_last': 'Smith',
                            'u_id': 0}],
    }