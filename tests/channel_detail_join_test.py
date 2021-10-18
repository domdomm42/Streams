import pytest
from src.channel import channel_details_v1, channel_join_v1
from src.error import InputError, AccessError
from src.auth import auth_login_v1, auth_register_v1
from src.channels import channels_list_v1, channels_listall_v1, channels_create_v1
from src.other import clear_v1
import requests
from src.auth_auth_helpers import check_and_get_user_id
from src.config import *
BASE_URL = url

#=====Input Error======================
#=====Test invalid channel_id==========

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
    #marry create a private channel called Marry
    create_info_marry = {"token": response_log_marry["token"], "name": "Marry", "is_public": False}
    channel_id_marry = requests.post(f'{BASE_URL}/channels/create/v2', json = create_info_marry)
    return channel_id_joe, channel_id_marry, response_log_joe, response_log_marry
    


#Test access details a channel with an invalid id(100 is not exist in data_store)
def test_invalid_channel_id_detail(setup):
    channel_id_joe, channel_id_marry, response_log_joe, response_log_marry = setup
    channel_detail_info = {"token": response_log_joe['token'], "channel_id": "100"}
    response = requests.get(f'{BASE_URL}/channel/details/v2', json = channel_detail_info)
    response_data = response.json()
    assert response_data['code'] == 400


#Test join a channel with an invalid id(100 is not exist in data_store)        
def test_invalid_channel_id_join(setup):
    channel_id_joe, channel_id_marry, response_log_joe, response_log_marry = setup
    channel_join_info = {"token": response_log_joe['token'], "channel_id": "100"}
    response = requests.post(f'{BASE_URL}/channel/join/v2', json = channel_join_info)
    response_data = response.json()
    assert response_data['code'] == 400


def test_negative_channel_id_in_details(setup):
    channel_id_joe, channel_id_marry, response_log_joe, response_log_marry = setup
    channel_detail_info = {"token": response_log_joe["token"], "channel_id": "-1"}
    response = requests.get(f'{BASE_URL}/channel/details/v2', json = channel_detail_info)
    response_data = response.json()
    assert response_data['code'] == 403


def test_negative_channel_id_in_join(setup):
    channel_id_joe, channel_id_marry, response_log_joe, response_log_marry = setup
    channel_join_info = {"token": response_log_joe['token'], "channel_id": "-1"}
    response = requests.post(f'{BASE_URL}/channel/join/v2', json = channel_join_info)
    response_data = response.json()
    assert response_data['code'] == 403


#=====Test member join again===========

def test_member_join_again_1(setup):
    channel_id_joe, channel_id_marry, response_log_joe, response_log_marry = setup
    channel_join_info = {"token": response_log_joe['token'], "channel_id": channel_id_joe}
    response = requests.post(f'{BASE_URL}/channel/join/v2', json = channel_join_info)
    response_data = response.json()
    assert response_data['code'] == 400      
    
   

def test_member_join_again_2(setup):
    channel_id_joe, channel_id_marry, response_log_joe, response_log_marry = setup
    channel_join_info = {"token": response_log_marry['token'], "channel_id": channel_id_marry}
    response = requests.post(f'{BASE_URL}/channel/join/v2', json = channel_join_info)
    response_data = response.json()
    assert response_data['code'] == 400      
    


#=====Access Error=====================
#=====Auth_user is not member==========
#User is not allow to access channel details
def test_no_member_access_detail_1(setup):
    channel_id_joe, channel_id_marry, response_log_joe, response_log_marry = setup
        #create channel and auth_user
    channel_details_info = {"token": response_log_joe['token'], "channel_id": channel_id_marry}
    response = requests.get(f'{BASE_URL}/channel/details/v2', json = channel_details_info)
    response_data = response.json()
    assert response_data['code'] == 400



def test_no_member_access_detail_2(setup):
    channel_id_joe, channel_id_marry, response_log_joe, response_log_marry = setup
        #create channel and auth_user
    channel_details_info = {"token": response_log_marry['token'], "channel_id": channel_id_joe}
    response = requests.get(f'{BASE_URL}/channel/details/v2', json = channel_details_info)
    response_data = response.json()
    assert response_data['code'] == 400
    
#=====Channel is private===============
#User is not a globle owner or member

def test_join_private_channel(setup):
    channel_id_joe, channel_id_marry, response_log_joe, response_log_marry = setup
    channel_join_info = {"token": response_log_marry['token'], "channel_id": channel_id_joe}
    response = requests.post(f'{BASE_URL}/channel/join/v2', json = channel_join_info)
    response_data = response.json()
    assert response_data['code'] == 400


#=====Valid case for detail===========
def test_valid_channel_id_detail_1(setup):
    
    channel_id_joe, channel_id_marry, response_log_joe, response_log_marry = setup
    
    channel_details_info = {"token": response_log_joe['token'], "channel_id": channel_id_joe}
    response = requests.get(f'{BASE_URL}/channel/details/v2', json = channel_details_info)
    u_id_joe = check_and_get_user_id(response_log_joe)
    details = response.json()
    assert details == {
        'name': 'Joe', 
        'is_public': True, 
        'owner_members': [
            {
                'u_id': u_id_joe, 
                'email': 'joe123@gmail.com', 
                'name_first': 'Joe', 
                'name_last': 'Smith', 
                'handle_str': 'joesmith'
            }
        ], 
        'all_members': [
            {
                'u_id': u_id_joe, 
                'email': 'joe123@gmail.com', 
                'name_first': 'Joe', 
                'name_last': 'Smith', 
                'handle_str': 'joesmith'
            }
        ]
    }

def test_valid_channel_id_detail_2(setup):
    channel_id_joe, channel_id_marry, response_log_joe, response_log_marry = setup
    channel_details_info = {"token": response_log_marry['token'], "channel_id": channel_id_marry}
    response = requests.get(f'{BASE_URL}/channel/details/v2', json = channel_details_info)
    u_id_marry = check_and_get_user_id(response_log_marry)
    details = response.json()
    
    
    details = channel_details_v1(login_marry, channels_marry)
    
    assert details == {
        'name': 'Marry', 
        'is_public': False, 
        'owner_members': [
            {
                'u_id': u_id_marry, 
                'email': 'marryjoe222@gmail.com', 
                'name_first': 'Marry', 
                'name_last': 'Joe', 
                'handle_str': 'marryjoe'
            }
        ], 
        'all_members': [
            {
                'u_id': u_id_marry, 
                'email': 'marryjoe222@gmail.com', 
                'name_first': 'Marry', 
                'name_last': 'Joe', 
                'handle_str': 'marryjoe'
            }
        ]
    }

#=====Valid case for join==============

def test_valid_channel_id_join(setup):
    channel_id_joe, channel_id_marry, response_log_joe, response_log_marry = setup
    channel_join_info = {"token": response_log_marry['token'], "channel_id": channel_id_joe}
    requests.post(f'{BASE_URL}/channel/join/v2', json = channel_join_info)
    channel_details_info = {"token": response_log_marry['token'], "channel_id": channel_id_marry}

    response = requests.get(f'{BASE_URL}/channel/details/v2', json = channel_details_info)
    u_id_joe = check_and_get_user_id(response_log_joe)
    u_id_marry = check_and_get_user_id(response_log_marry)

    details = response.json()
    
    assert details == {
        'name': 'Joe',
        'is_public': True,
        'owner_members': [
            {
                'u_id': u_id_joe, 
                'email': 'joe123@gmail.com', 
                'name_first': 'Joe', 
                'name_last': 'Smith', 
                'handle_str': 'joesmith'
            }
        ], 
        'all_members': [
            {
                'u_id': u_id_joe, 
                'email': 'joe123@gmail.com', 
                'name_first': 'Joe', 
                'name_last': 'Smith', 
                'handle_str': 'joesmith'
            }, 
            {   'u_id': u_id_marry, 
                'email': 'marryjoe222@gmail.com', 
                'name_first': 'Marry', 
                'name_last': 'Joe', 
                'handle_str': 'marryjoe'
            }
        ]
    }
    
