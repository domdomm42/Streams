import pytest

from src.error import InputError, AccessError

from src.users import *

@pytest.fixture
def setup():

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
   return response_log_joe, response_log_marry


def setup():
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
    return response_log_joe, response_log_marry

def test__user_handle_too_short(setup):
    response_log_joe, response_log_marry = setup
    sethandle_info = {"token": response_log_joe["token"], "handle_str": "a"}
    response = requests.put(f'{BASE_URL}/user/profile/sethandle/v2', json = sethandle_info)
    response_data = response.json()
    assert response_data['code'] == 400
