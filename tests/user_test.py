import pytest
import requests

from src.other import clear_v1
from src.error import InputError, AccessError
from src.auth import auth_login_v1, auth_register_v1
from src.config import *
from src.users import *

BASE_URL = url


@pytest.fixture
def setup():
    requests.delete(f'{BASE_URL}/clear/v1')
    # register for joe
    user_joe_info_reg = {"email": "joe123@gmail.com", "password": "password", "name_first": "Joe", "name_last": "Smith"}
    user_joe_info_login = {"email": "joe123@gmail.com", "password": "password"}
    requests.post(f'{BASE_URL}/auth/register/v2', json=user_joe_info_reg)
    # register for marry
    user_marry_info_reg = {"email": "marryjoe222@gmail.com", "password": "passwordM", "name_first": "Marry",
                           "name_last": "Joe"}
    user_marry_info_login = {"email": "marryjoe222@gmail.com", "password": "passwordM"}
    requests.post(f'{BASE_URL}/auth/register/v2', json=user_marry_info_reg)
    # log them in
    response_log_joe = requests.post(f'{BASE_URL}/auth/login/v2', json=user_joe_info_login)
    response_log_marry = requests.post(f'{BASE_URL}/auth/login/v2', json=user_marry_info_login)
    response_log_joe = response_log_joe.json()
    response_log_marry = response_log_marry.json()
    return response_log_joe, response_log_marry


def test_user_handle_too_short(setup):
    response_log_joe, _ = setup
    sethandle_info = {"token": response_log_joe['token'], "handle_str": "a"}
    response = requests.put(f'{BASE_URL}user/profile/sethandle/v1', json=sethandle_info)
    response_data = response.json()
    assert response_data['code'] == 400


def test_user_handle_too_long(setup):
    response_log_joe, _ = setup
    sethandle_info = {"token": response_log_joe['token'], "handle_str": "longlonglonglonglonglong"}
    response = requests.put(f'{BASE_URL}user/profile/sethandle/v1', json=sethandle_info)
    response_data = response.json()
    assert response_data['code'] == 400


def test_user_handle_contains_not_alnum(setup):
    response_log_joe, _ = setup
    sethandle_info = {"token": response_log_joe['token'], "handle_str": "my_name!"}
    response = requests.put(f'{BASE_URL}user/profile/sethandle/v1', json=sethandle_info)
    response_data = response.json()
    assert response_data['code'] == 400


def test_user_handle_duplicate(setup):
    response_log_joe, response_log_marry = setup

    sethandle_info_joe = {"token": response_log_joe['token'], "handle_str": "KobeBryant"}
    requests.put(f'{BASE_URL}user/profile/sethandle/v1', json=sethandle_info_joe)
    sethandle_info_marry = {"token": response_log_marry['token'], "handle_str": "KobeBryant"}
    response = requests.put(f'{BASE_URL}user/profile/sethandle/v1', json=sethandle_info_marry)
    response_data = response.json()
    assert response_data['code'] == 400


def test_user_handle_duplicate_capital(setup):
    response_log_joe, response_log_marry = setup

    sethandle_info_joe = {"token": response_log_joe['token'], "handle_str": "aaa"}
    requests.put(f'{BASE_URL}user/profile/sethandle/v1', json=sethandle_info_joe)
    sethandle_info_marry = {"token": response_log_marry['token'], "handle_str": "AAA"}
    response = requests.put(f'{BASE_URL}user/profile/sethandle/v1', json=sethandle_info_marry)
    response_data = response.json()
    assert response_data == {}



def test_valid_handle(setup):
    response_log_joe, _ = setup
    sethandle_info = {"token": response_log_joe['token'], "handle_str": "KobeBryant"}
    requests.put(f'{BASE_URL}user/profile/sethandle/v1', json=sethandle_info)
    user_profile_info = {"token": response_log_joe['token'], "u_id": 0}
    response = requests.get(f'{BASE_URL}user/profile/v1', params=user_profile_info)
    response_data = response.json()
    assert response_data == {
        'emails': 'joe123@gmail.com',
        'first_names': 'Joe',
        'last_names': 'Smith',
        'user_handles': 'KobeBryant',
        'user_id': 0,
    }




# Test for u_id
def test_user_u_id_big(setup):
    response_log_joe, _ = setup

    user_profile_info = {"token": response_log_joe['token'], "u_id": 100}

    response = requests.get(f'{BASE_URL}user/profile/v1', params=user_profile_info)
    response_data = response.json()
    assert response_data['code'] == 400









def test_valid_u_id(setup):
    response_log_joe, _ = setup
    user_profile_info = {"token": response_log_joe['token'], "u_id": 0}
    response = requests.get(f'{BASE_URL}user/profile/v1', params=user_profile_info)
    response_data = response.json()
    assert response_data == {
        'emails': 'joe123@gmail.com',
        'first_names': 'Joe',
        'last_names': 'Smith',
        'user_handles': 'joesmith',
        'user_id': 0,
    }


# Test for name
def test_user_name_first_too_short(setup):
    response_log_joe, _ = setup
    setname_info = {"token": response_log_joe["token"], "first_names": "", "last_names": "a"}
    response = requests.put(f'{BASE_URL}user/profile/setname/v1', json=setname_info)
    response_data = response.json()
    assert response_data['code'] == 400


def test_user_name_last_too_short(setup):
    response_log_joe, _ = setup
    setname_info = {"token": response_log_joe["token"], "first_names": "a", "last_names": ""}
    response = requests.put(f'{BASE_URL}user/profile/setname/v1', json=setname_info)
    response_data = response.json()
    assert response_data['code'] == 400


def test_user_name_first_too_long(setup):
    response_log_joe, _ = setup
    setname_info = {"token": response_log_joe["token"],
                    "first_names": "abcdefghijklmnopqrstuvwxyz1531abcdefghijklmnopqrstuvwxyz", "last_names": "a"}
    response = requests.put(f'{BASE_URL}user/profile/setname/v1', json=setname_info)
    response_data = response.json()
    assert response_data['code'] == 400


def test_user_name_last_too_long(setup):
    response_log_joe, _ = setup
    setname_info = {"token": response_log_joe["token"], "first_names": 'a',
                    "last_names": "abcdefghijklmnopqrstuvwxyz1531abcdefghijklmnopqrstuvwxyz"}
    response = requests.put(f'{BASE_URL}user/profile/setname/v1', json=setname_info)
    response_data = response.json()
    assert response_data['code'] == 400









def test_user_name_duplication(setup):
    response_log_joe, response_log_marry = setup
    setname_info1 = {"token": response_log_joe["token"], "first_names": "a", "last_names": "Smith"}
    setname_info2 = {"token": response_log_marry["token"], "first_names": "a", "last_names": "Smith"}

    requests.put(f'{BASE_URL}user/profile/setname/v1', json=setname_info1)
    response = requests.put(f'{BASE_URL}user/profile/setname/v1', json=setname_info2)

    response_data = response.json()
    assert response_data == {}




def test_valid_first_name(setup):
    response_log_joe, _ = setup
    setname_info = {"token": response_log_joe['token'], "first_names": "a", "last_names": "Smith"}
    requests.put(f'{BASE_URL}user/profile/setname/v1', json=setname_info)
    user_profile_info = {"token": response_log_joe['token'], "u_id": 0}
    response = requests.get(f'{BASE_URL}user/profile/v1', params=user_profile_info)
    response_data = response.json()
    assert response_data == {
        'emails': 'joe123@gmail.com',
        'first_names': 'a',
        'last_names': 'Smith',
        'user_handles': 'joesmith',
        'user_id': 0,
    }


def test_valid_name(setup):
    response_log_joe, _ = setup
    setname_info = {"token": response_log_joe['token'], "first_names": "a", "last_names": "b"}
    requests.put(f'{BASE_URL}user/profile/setname/v1', json=setname_info)
    user_profile_info = {"token": response_log_joe['token'], "u_id": 0}
    response = requests.get(f'{BASE_URL}user/profile/v1', params=user_profile_info)
    response_data = response.json()
    assert response_data == {
        'emails': 'joe123@gmail.com',
        'first_names': 'a',
        'last_names': 'b',
        'user_handles': 'joesmith',
        'user_id': 0,
    }




def test_valid_last_name(setup):
    response_log_joe, _ = setup
    setname_info = {"token": response_log_joe['token'], "first_names": "Joe", "last_names": "a"}
    requests.put(f'{BASE_URL}user/profile/setname/v1', json=setname_info)
    user_profile_info = {"token": response_log_joe['token'], "u_id": 0}
    response = requests.get(f'{BASE_URL}user/profile/v1', params=user_profile_info)
    response_data = response.json()
    assert response_data == {
        'emails': 'joe123@gmail.com',
        'first_names': 'Joe',
        'last_names': 'a',
        'user_handles': 'joesmith',
        'user_id': 0,
    }


# Test for email
def test_user_email_duplication(setup):
    response_log_joe, response_log_marry = setup
    setemail_info1 = {"token": response_log_joe["token"], "emails": "kobebryant24881@gmail.com"}
    setemail_info2 = {"token": response_log_marry["token"], "emails": "kobebryant24881@gmail.com"}

    requests.put(f'{BASE_URL}user/profile/setemail/v1', json=setemail_info1)
    response = requests.put(f'{BASE_URL}user/profile/setemail/v1', json=setemail_info2)

    response_data = response.json()
    assert response_data['code'] == 400





def test_user_email_duplication_invalid_capital(setup):
    response_log_joe, response_log_marry = setup
    setemail_info1 = {"token": response_log_joe["token"], "emails": "aaa@gmail.com"}
    setemail_info2 = {"token": response_log_marry["token"], "emails": "AAA@gmail.com"}

    requests.put(f'{BASE_URL}user/profile/setemail/v1', json=setemail_info1)
    response = requests.put(f'{BASE_URL}user/profile/setemail/v1', json=setemail_info2)

    response_data = response.json()
    assert response_data == {}




def test_user_email_invalid(setup):
    response_log_joe, _ = setup
    setemail_info = {"token": response_log_joe["token"], "emails": "abcde"}
    response = requests.put(f'{BASE_URL}user/profile/setemail/v1', json=setemail_info)
    response_data = response.json()
    assert response_data['code'] == 400





def test_valid_email(setup):
    response_log_joe, _ = setup
    setemail_info = {"token": response_log_joe['token'], "emails": "joe123@gmail.com"}
    requests.put(f'{BASE_URL}user/profile/setemail/v1', json=setemail_info)
    user_profile_info = {"token": response_log_joe['token'], "u_id": 0}
    response = requests.get(f'{BASE_URL}user/profile/v1', params=user_profile_info)
    response_data = response.json()
    assert response_data == {
        'emails': 'joe123@gmail.com',
        'first_names': 'Joe',
        'last_names': 'Smith',
        'user_handles': 'joesmith',
        'user_id': 0,
    }





def test_user_all_output(setup):
    response_log_joe, _ = setup
    user_all_info = {"token": response_log_joe["token"]}
    response = requests.get(f'{BASE_URL}users/all/v1', json=user_all_info)
    response_data = response.json()
    assert response_data == [
        {'email': 'joe123@gmail.com',
         'handle_str': 'joesmith',
         'is_remove': False,
         'name_first': 'Joe',
         'name_last': 'Smith',
         'u_id': 0},

    ]


def test_user_profile_output(setup):
    response_log_joe, _ = setup

    user_profile_info = {"token": response_log_joe['token'], "u_id": 1}

    response = requests.get(f'{BASE_URL}user/profile/v1', params=user_profile_info)
    response_data = response.json()
    assert response_data == {
        'emails': 'marryjoe222@gmail.com',
        'first_names': 'Marry',
        'last_names': 'Joe',
        'user_handles': 'marryjoe',
        'user_id': 1}







