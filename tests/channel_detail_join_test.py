import pytest
import requests
from src.config import *

BASE_URL = url
ACCESS_ERROR = 403
INPUT_ERROR = 400


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
    channel_id_joe = channel_id_joe.json()
    #marry create a private channel called Marry
    create_info_marry = {"token": response_log_marry["token"], "name": "Marry", "is_public": False}
    channel_id_marry = requests.post(f'{BASE_URL}/channels/create/v2', json = create_info_marry)
    channel_id_marry = channel_id_marry.json()
    return channel_id_joe, channel_id_marry, response_log_joe, response_log_marry
    


#Test access details a channel with an invalid id(100 is not exist in data_store)
def test_invalid_channel_id_detail(setup):
    _, _, response_log_joe, _ = setup
    channel_detail_info = {"token": response_log_joe['token'], "channel_id": 100}
    response = requests.get(f'{BASE_URL}/channel/details/v2', params = channel_detail_info)
    response_data = response.json()
    assert response_data['code'] == INPUT_ERROR


#Test join a channel with an invalid id(100 is not exist in data_store)        
def test_invalid_channel_id_join(setup):
    _, _, response_log_joe, _ = setup
    channel_join_info = {"token": response_log_joe['token'], "channel_id": 100}
    response = requests.post(f'{BASE_URL}/channel/join/v2', json = channel_join_info)
    response_data = response.json()
    assert response_data['code'] == INPUT_ERROR


def test_negative_channel_id_in_details(setup):
    _, _, response_log_joe, _ = setup
    channel_detail_info = {"token": response_log_joe["token"], "channel_id": -1}
    response = requests.get(f'{BASE_URL}/channel/details/v2', params = channel_detail_info)
    response_data = response.json()
    assert response_data['code'] == 400


def test_negative_channel_id_in_join(setup):
    _, _, response_log_joe, _ = setup
    channel_join_info = {"token": response_log_joe['token'], "channel_id": -1}
    response = requests.post(f'{BASE_URL}/channel/join/v2', json = channel_join_info)
    response_data = response.json()
    assert response_data['code'] == 400


#=====Test member join again===========

def test_member_join_again_1(setup):
    channel_id_joe, _, response_log_joe, _ = setup
    channel_join_info = {"token": response_log_joe['token'], "channel_id": channel_id_joe['channel_id']}
    response = requests.post(f'{BASE_URL}/channel/join/v2', json = channel_join_info)
    response_data = response.json()
    assert response_data['code'] == INPUT_ERROR      
    
   

def test_member_join_again_2(setup):
    _, channel_id_marry, _, response_log_marry = setup
    channel_join_info = {"token": response_log_marry['token'], "channel_id": channel_id_marry['channel_id']}
    response = requests.post(f'{BASE_URL}/channel/join/v2', json = channel_join_info)
    response_data = response.json()
    assert response_data['code'] == INPUT_ERROR      
    


#=====Access Error=====================
#=====Auth_user is not member==========
#User is not allow to access channel details
def test_no_member_access_detail_1(setup):
    _, channel_id_marry, response_log_joe, _ = setup
        #create channel and auth_user
    channel_details_info = {"token": response_log_joe['token'], "channel_id": channel_id_marry['channel_id']}
    response = requests.get(f'{BASE_URL}/channel/details/v2', params = channel_details_info)
    response_data = response.json()
    assert response_data['code'] == ACCESS_ERROR



def test_no_member_access_detail_2(setup):
    channel_id_joe, _, _, response_log_marry = setup
        #create channel and auth_user
    channel_details_info = {"token": response_log_marry['token'], "channel_id": channel_id_joe['channel_id']}
    response = requests.get(f'{BASE_URL}/channel/details/v2', params = channel_details_info)
    response_data = response.json()
    assert response_data['code'] == ACCESS_ERROR
    
#=====Channel is private===============
#User is not a global owner or member

def test_join_private_channel(setup): # making joe join marry's channel
    _, channel_id_marry, _, _ = setup

    user_milly_reg = {"email": "milly3@gmail.com", "password": "passwordS", "name_first": "Milly", "name_last": "Mae"}
    milly_token = requests.post(f'{BASE_URL}/auth/register/v2', json = user_milly_reg).json()['token']
    channel_join_info = {"token": milly_token, "channel_id": channel_id_marry['channel_id']}
    response = requests.post(f'{BASE_URL}/channel/join/v2', json = channel_join_info)
    response_data = response.json()
    assert response_data['code'] == ACCESS_ERROR

def test_global_owner_join_private(setup):
    _, channel_id_marry, response_log_joe, _ = setup
    channel_join_info = {"token": response_log_joe['token'], "channel_id": channel_id_marry['channel_id']}
    requests.post(f'{BASE_URL}/channel/join/v2', json = channel_join_info)
    channel_details_info = {"token": response_log_joe['token'], "channel_id": channel_id_marry['channel_id']}
    response = requests.get(f'{BASE_URL}/channel/details/v2', params = channel_details_info)
    details = response.json()

    assert details == {
        'name': 'Marry',
        'is_public': False,
        'owner_members': [
            {   
                'email': 'marryjoe222@gmail.com',
                'handle_str': 'marryjoe',
                'name_first': 'Marry',
                'name_last': 'Joe',
                'u_id': 1,
                'profile_img_url': ''
            }
        ],
        'all_members': [
            {   'email': 'marryjoe222@gmail.com',
                'handle_str': 'marryjoe',
                'name_first': 'Marry',
                'name_last': 'Joe',
                'u_id': 1,
                'profile_img_url': ''
            },
            {   'email': 'joe123@gmail.com',
                'handle_str': 'joesmith',
                'name_first': 'Joe',
                'name_last': 'Smith',
                'u_id': 0,
                'profile_img_url': ''
            }
        ],
    }


#=====Valid case for detail===========
def test_valid_channel_id_detail_1(setup):
    
    channel_id_joe, _, response_log_joe, _ = setup
    
    channel_details_info = {"token": response_log_joe['token'], "channel_id": channel_id_joe['channel_id']}
    response = requests.get(f'{BASE_URL}/channel/details/v2', params = channel_details_info)
    
    details = response.json()
    assert details == {
        'name': 'Joe', 
        'is_public': True, 
        'owner_members': [
            {
                'u_id': 0, 
                'email': 'joe123@gmail.com', 
                'name_first': 'Joe', 
                'name_last': 'Smith', 
                'handle_str': 'joesmith',
                'profile_img_url': ''
            }
        ], 
        'all_members': [
            {
                'u_id': 0, 
                'email': 'joe123@gmail.com', 
                'name_first': 'Joe', 
                'name_last': 'Smith', 
                'handle_str': 'joesmith',
                'profile_img_url': ''
            }
        ]
    }

def test_valid_channel_id_detail_2(setup):
    _, channel_id_marry, _, response_log_marry = setup
    channel_details_info = {"token": response_log_marry['token'], "channel_id": channel_id_marry['channel_id']}
    response = requests.get(f'{BASE_URL}/channel/details/v2', params = channel_details_info)
    
    details = response.json()
    
    
   
    
    assert details == {
        'name': 'Marry', 
        'is_public': False, 
        'owner_members': [
            {
                'u_id': 1, 
                'email': 'marryjoe222@gmail.com', 
                'name_first': 'Marry', 
                'name_last': 'Joe', 
                'handle_str': 'marryjoe',
                'profile_img_url': ''
            }
        ], 
        'all_members': [
            {
                'u_id': 1, 
                'email': 'marryjoe222@gmail.com', 
                'name_first': 'Marry', 
                'name_last': 'Joe', 
                'handle_str': 'marryjoe',
                'profile_img_url': ''
            }
        ]
    }

#=====Valid case for join==============

def test_valid_channel_id_join(setup):
    channel_id_joe, _, _, response_log_marry = setup
    channel_join_info = {"token": response_log_marry['token'], "channel_id": channel_id_joe['channel_id']}
    requests.post(f'{BASE_URL}/channel/join/v2', json = channel_join_info)
    channel_details_info = {"token": response_log_marry['token'], "channel_id": channel_id_joe['channel_id']}

    response = requests.get(f'{BASE_URL}/channel/details/v2', params = channel_details_info)
    
    

    details = response.json()
    
    assert details == {
        'name': 'Joe',
        'is_public': True,
        'owner_members': [
            {
                'u_id': 0, 
                'email': 'joe123@gmail.com', 
                'name_first': 'Joe', 
                'name_last': 'Smith', 
                'handle_str': 'joesmith',
                'profile_img_url': ''
            }
        ], 
        'all_members': [
            {
                'u_id': 0, 
                'email': 'joe123@gmail.com', 
                'name_first': 'Joe', 
                'name_last': 'Smith', 
                'handle_str': 'joesmith',
                'profile_img_url': ''
            }, 
            {   'u_id': 1, 
                'email': 'marryjoe222@gmail.com', 
                'name_first': 'Marry', 
                'name_last': 'Joe', 
                'handle_str': 'marryjoe',
                'profile_img_url': ''
            }
        ]
    }




