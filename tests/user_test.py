import pytest
import requests

from src.other import clear_v1
from src.error import InputError, AccessError
from src.auth import auth_login_v1, auth_register_v1
# from src.users import user_profile_sethandle_v1, user_profile_setemail_v1,user_profile_setname_v1, user_profile_v1, user_all_v1
from src.config import *
from src.users import *

BASE_URL = url

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

def test_user_handle_too_short(setup):
    response_log_joe, _ = setup
    sethandle_info = {"token": response_log_joe['token'], "handle_str": "a"}
    response = requests.put(f'{BASE_URL}user/profile/sethandle/v1', json = sethandle_info)
    response_data = response.json()
    assert response_data['code'] == 400

def test_user_handle_too_long(setup):
    response_log_joe, _ = setup
    sethandle_info = {"token": response_log_joe['token'], "handle_str": "longlonglonglonglonglong"}
    response = requests.put(f'{BASE_URL}user/profile/sethandle/v1', json = sethandle_info)
    response_data = response.json()
    assert response_data['code'] == 400

def test_user_handle_contains_not_alnum(setup):
    response_log_joe, _ = setup
    sethandle_info = {"token": response_log_joe['token'], "handle_str": "my_name!"}
    response = requests.put(f'{BASE_URL}user/profile/sethandle/v1', json = sethandle_info)
    response_data = response.json()
    assert response_data['code'] == 400

def test_user_handle_duplicate(setup):
    response_log_joe, response_log_marry = setup

    sethandle_info_joe = {"token": response_log_joe['token'], "handle_str": "KobeBryant"}
    requests.put(f'{BASE_URL}user/profile/sethandle/v1', json = sethandle_info_joe)
    sethandle_info_marry = {"token": response_log_marry['token'], "handle_str": "KobeBryant"}
    response = requests.put(f'{BASE_URL}user/profile/sethandle/v1', json = sethandle_info_marry)
    response_data = response.json()
    assert response_data['code'] == 400


def test_valid_handle(setup):
    response_log_joe, _ = setup
    sethandle_info = {"token": response_log_joe['token'], "handle_str": "KobeBryant"}
    requests.put(f'{BASE_URL}user/profile/sethandle/v1', json = sethandle_info)
    user_profile_info = {"token": response_log_joe['token'], "u_id": 0}
    response = requests.get(f'{BASE_URL}user/profile/v1', params = user_profile_info)
    response_data = response.json()
    assert response_data == {
        'emails': 'joe123@gmail.com',
        'first_names': 'Joe',
        'last_names': 'Smith',
        'user_handles': 'KobeBryant',
        'user_id': 0,
        }

# import pytest

# from src.error import InputError, AccessError

# from src.users import *

# import requests

# from src.auth_auth_helpers import check_and_get_user_id

# from src.config import *

# BASE_URL = url

# @pytest.fixture
# def setup():

#    requests.delete(f'{BASE_URL}/clear/v1')
#    #register for joe
#    user_joe_info_reg = {"email": "joe123@gmail.com", "password": "password", "name_first": "Joe", "name_last": "Smith"}
#    user_joe_info_login = {"email": "joe123@gmail.com", "password": "password"}
#    requests.post(f'{BASE_URL}/auth/register/v2', json = user_joe_info_reg)
#    #register for marry
#    user_marry_info_reg = {"email": "marryjoe222@gmail.com", "password": "passwordM", "name_first": "Marry", "name_last": "Joe"}
#    user_marry_info_login = {"email": "marryjoe222@gmail.com", "password": "passwordM"}
#    requests.post(f'{BASE_URL}/auth/register/v2', json = user_marry_info_reg)
#    #log them in
#    response_log_joe = requests.post(f'{BASE_URL}/auth/login/v2', json = user_joe_info_login)
#    response_log_marry = requests.post(f'{BASE_URL}/auth/login/v2', json = user_marry_info_login)
#    response_log_joe = response_log_joe.json()
#    response_log_marry = response_log_marry.json()
#    return response_log_joe, response_log_marry



# Test for u_id
def test_user_u_id_big(setup):
    
    response_log_joe, _ = setup

    user_profile_info = {"token": response_log_joe['token'], "u_id": 100}
    
    response = requests.get(f'{BASE_URL}user/profile/v1', params = user_profile_info)
    response_data = response.json()
    assert response_data['code'] == 400


def test_user_u_id_alpha(setup):
    
    response_log_joe, _ = setup

    user_profile_info = {"token": response_log_joe['token'], "u_id":"a"}
    
    response = requests.get(f'{BASE_URL}user/profile/v1', params = user_profile_info)
    response_data = response.json()
    assert response_data['code'] == 500

def test_user_u_id_not_alphanumeric(setup):
    
    response_log_joe, _ = setup

    user_profile_info = {"token": response_log_joe['token'], "u_id":"!"}
    
    response = requests.get(f'{BASE_URL}user/profile/v1', params = user_profile_info)
    response_data = response.json()
    assert response_data['code'] == 500


def test_user_u_id_negative(setup):
    
    response_log_joe, _ = setup

    user_profile_info = {"token": response_log_joe['token'], "u_id": -100}
    
    response = requests.get(f'{BASE_URL}user/profile/v1', params = user_profile_info)
    response_data = response.json()
    assert response_data['code'] == 500


def test_user_u_id_empty(setup):
    
    response_log_joe, _ = setup

    user_profile_info = {"token": response_log_joe['token'], "u_id":""}
    
    response = requests.get(f'{BASE_URL}user/profile/v1', params = user_profile_info)
    response_data = response.json()
    assert response_data['code'] == 500


def test_u_id_duplication(setup):

    response_log_joe, response_log_marry = setup
    # setname_info1 = {"token": response_log_joe["token"], "first_names": "a","last_names": "Smith"}
    # setname_info2 = {"token": response_log_marry["token"], "first_names": "a","last_names": "Smith"}

    # requests.put(f'{BASE_URL}user/profile/setname/v1', json = setname_info1)
    # response = requests.put(f'{BASE_URL}user/profile/setname/v1', json = setname_info2)

    user_profile_info1 = {"token": response_log_joe['token'], "u_id": 0}

    user_profile_info2 = {"token": response_log_marry['token'], "u_id": 0}


    response = requests.get(f'{BASE_URL}user/profile/v1', params = user_profile_info1)


    
    
    #response = (f'{BASE_URL}user/profile/v1', params = user_profile_info2)

    response_data = response.json()
    response_data = requests.get(f'{BASE_URL}user/profile/v1', params = user_profile_info2)
    assert  [200] == [200]



def test_valid_u_id(setup):
    response_log_joe, _ = setup
    user_profile_info = {"token": response_log_joe['token'], "u_id": 0}
    response = requests.get(f'{BASE_URL}user/profile/v1', params = user_profile_info)
    response_data = response.json()
    assert response_data == {
        'emails': 'joe123@gmail.com',
        'first_names': 'Joe',
        'last_names': 'Smith',
        'user_handles': 'joesmith',
        'user_id': 0,
        }
        

# def test_valid_u_id_removed(setup):
#     response_log_joe, _ = setup
#     user_profile_info = {"token": response_log_joe['token'], "u_id": 0, "removed_user":False}
#     response = requests.get(f'{BASE_URL}user/profile/v1', params = user_profile_info)
#     response_data = response.json()
#     assert response_data == {
#         'emails': 'joe123@gmail.com',
#         'first_names': 'Joe',
#         'last_names': 'Smith',
#         'user_handles': 'joesmith',
#         'user_id': 0,
#         }



# Test for name
def test_user_name_first_too_short(setup):
    response_log_joe, _ = setup
    setname_info = {"token": response_log_joe["token"], "first_names": "", "last_names":"a"}
    response = requests.put(f'{BASE_URL}user/profile/setname/v1', json = setname_info)
    response_data = response.json()
    assert response_data['code'] == 400

def test_user_name_last_too_short(setup):
    response_log_joe, _ = setup
    setname_info = {"token": response_log_joe["token"], "first_names":"a", "last_names": ""}
    response = requests.put(f'{BASE_URL}user/profile/setname/v1', json = setname_info)
    response_data = response.json()
    assert response_data['code'] == 400


def test_user_name_first_too_long(setup):
    response_log_joe, _ = setup
    setname_info = {"token": response_log_joe["token"], "first_names": "abcdefghijklmnopqrstuvwxyz1531abcdefghijklmnopqrstuvwxyz", "last_names": "a"}
    response = requests.put(f'{BASE_URL}user/profile/setname/v1', json=setname_info)
    response_data = response.json()
    assert response_data['code'] == 400


def test_user_name_last_too_long(setup):
    response_log_joe, _ = setup
    setname_info = {"token": response_log_joe["token"], "first_names":'a', "last_names": "abcdefghijklmnopqrstuvwxyz1531abcdefghijklmnopqrstuvwxyz"}
    response = requests.put(f'{BASE_URL}user/profile/setname/v1', json=setname_info)
    response_data = response.json()
    assert response_data['code'] == 400


def test_user_name_both_short(setup):
    response_log_joe, _ = setup
    setname_info = {"token": response_log_joe["token"], "first_names":"", "last_names": ""}
    response = requests.put(f'{BASE_URL}user/profile/setname/v1', json = setname_info)
    response_data = response.json()
    assert response_data['code'] == 400

def test_user_name_both_long(setup):
    response_log_joe, _ = setup
    setname_info = {"token": response_log_joe["token"], "first_names":"abcdefghijklmnopqrstuvwxyz1531abcdefghijklmnopqrstuvwxyz", "last_names": "abcdefghijklmnopqrstuvwxyz1531abcdefghijklmnopqrstuvwxyz"}
    response = requests.put(f'{BASE_URL}user/profile/setname/v1', json = setname_info)
    response_data = response.json()
    assert response_data['code'] == 400

def test_user_name_first_short_last_long(setup):
    response_log_joe, _ = setup
    setname_info = {"token": response_log_joe["token"], "first_names": '',
                    "last_names": "abcdefghijklmnopqrstuvwxyz1531abcdefghijklmnopqrstuvwxyz"}
    response = requests.put(f'{BASE_URL}user/profile/setname/v1', json=setname_info)
    response_data = response.json()
    assert response_data['code'] == 400


def test_user_name_first_long_last_short(setup):
    response_log_joe, _ = setup
    setname_info = {"token": response_log_joe["token"],
                    "first_names": "abcdefghijklmnopqrstuvwxyz1531abcdefghijklmnopqrstuvwxyz", "last_names": ""}
    response = requests.put(f'{BASE_URL}user/profile/setname/v1', json=setname_info)
    response_data = response.json()
    assert response_data['code'] == 400

def test_user_name_first_number(setup):
    response_log_joe, _ = setup
    setname_info = {"token": response_log_joe["token"],
                    "first_names": 888, "last_names": "a"}
    response = requests.put(f'{BASE_URL}user/profile/setname/v1', json=setname_info)
    response_data = response.json()
    assert response_data['code'] == 500

def test_user_name_last_number(setup):
    response_log_joe, _ = setup
    setname_info = {"token": response_log_joe["token"],
                    "first_names": "a", "last_names": 888}
    response = requests.put(f'{BASE_URL}user/profile/setname/v1', json=setname_info)
    response_data = response.json()
    assert response_data['code'] == 500



def test_user_name_duplication(setup):
    response_log_joe, response_log_marry = setup
    setname_info1 = {"token": response_log_joe["token"], "first_names": "a","last_names": "Smith"}
    setname_info2 = {"token": response_log_marry["token"], "first_names": "a","last_names": "Smith"}

    requests.put(f'{BASE_URL}user/profile/setname/v1', json = setname_info1)
    response = requests.put(f'{BASE_URL}user/profile/setname/v1', json = setname_info2)

    response_data = response.json()
    assert response_data == {}





def test_valid_first_name(setup):
    response_log_joe, _ = setup
    setname_info = {"token": response_log_joe['token'], "first_names": "a","last_names": "Smith"}
    requests.put(f'{BASE_URL}user/profile/setname/v1', json = setname_info)
    user_profile_info = {"token": response_log_joe['token'], "u_id": 0}
    response = requests.get(f'{BASE_URL}user/profile/v1', params = user_profile_info)
    response_data = response.json()
    assert response_data == {
        'emails': 'joe123@gmail.com',
        'first_names': 'a',
        'last_names': 'Smith',
        'user_handles': 'joesmith',
        'user_id': 0,
        }

def test_valid_last_name(setup):
    response_log_joe, _ = setup
    setname_info = {"token": response_log_joe['token'], "first_names": "Joe","last_names": "a"}
    requests.put(f'{BASE_URL}user/profile/setname/v1', json = setname_info)
    user_profile_info = {"token": response_log_joe['token'], "u_id": 0}
    response = requests.get(f'{BASE_URL}user/profile/v1', params = user_profile_info)
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

    requests.put(f'{BASE_URL}user/profile/setemail/v1', json = setemail_info1)
    response = requests.put(f'{BASE_URL}user/profile/setemail/v1', json = setemail_info2)

    response_data = response.json()
    assert response_data['code'] == 400

def test_user_email_invalid(setup):
    response_log_joe, _ = setup
    setemail_info = {"token": response_log_joe["token"], "emails": "abcde"}
    response = requests.put(f'{BASE_URL}user/profile/setemail/v1', json = setemail_info)
    response_data = response.json()
    assert response_data['code'] == 400


def test_user_email_short(setup):
    response_log_joe, _ = setup
    setemail_info = {"token": response_log_joe["token"], "emails": "@gmail.com"}
    response = requests.put(f'{BASE_URL}user/profile/setemail/v1', json = setemail_info)
    response_data = response.json()
    assert response_data['code'] == 400

def test_user_email_empty(setup):
    response_log_joe, _ = setup
    setemail_info = {"token": response_log_joe["token"], "emails": ""}
    response = requests.put(f'{BASE_URL}user/profile/setemail/v1', json = setemail_info)
    response_data = response.json()
    assert response_data['code'] == 400

def test_user_email_number(setup):
    response_log_joe, _ = setup
    setemail_info = {"token": response_log_joe["token"], "emails": 888}
    response = requests.put(f'{BASE_URL}user/profile/setemail/v1', json = setemail_info)
    response_data = response.json()
    assert response_data['code'] == 500

def test_valid_email(setup):
    response_log_joe, _ = setup
    setemail_info = {"token": response_log_joe['token'], "emails": "joe123@gmail.com"}
    requests.put(f'{BASE_URL}user/profile/setemail/v1', json = setemail_info)
    user_profile_info = {"token": response_log_joe['token'], "u_id": 0}
    response = requests.get(f'{BASE_URL}user/profile/v1', params = user_profile_info)
    response_data = response.json()
    assert response_data == {
        'emails': 'joe123@gmail.com',
        'first_names': 'Joe',
        'last_names': 'Smith',
        'user_handles': 'joesmith',
        'user_id': 0,
        }





def test_user_all_correct(setup):
    response_log_joe, _ = setup
    
    setname_info = {"token": response_log_joe["token"], "first_names": "a", "last_names":"a"}
    response = requests.put(f'{BASE_URL}user/profile/setname/v1', json = setname_info)

    
    setemail_info = {"token": response_log_joe["token"], "emails": "kobebryant24881@gmail.com"}
    requests.put(f'{BASE_URL}user/profile/setemail/v1', json = setemail_info)

    sethandle_info_joe = {"token": response_log_joe['token'], "handle_str": "KobeBryant"}
    requests.put(f'{BASE_URL}user/profile/sethandle/v1', json = sethandle_info_joe)
    user_profile_info = {"token": response_log_joe['token'], "u_id": 0}
    response = requests.get(f'{BASE_URL}user/profile/v1', params = user_profile_info)
    response_data = response.json()
    assert response_data == {
        'emails': 'kobebryant24881@gmail.com',
        'first_names': 'a',
        'last_names': 'a',
        'user_handles': 'KobeBryant',
        'user_id': 0,
    }


def test_user_all_wrong(setup):
    response_log_joe, _ = setup
    
    setname_info = {"token": response_log_joe["token"], "first_names": "", "last_names":""}
    response = requests.put(f'{BASE_URL}user/profile/setname/v1', json = setname_info)

    
    setemail_info = {"token": response_log_joe["token"], "emails": ""}
    response = requests.put(f'{BASE_URL}user/profile/setemail/v1', json = setemail_info)

    sethandle_info_joe = {"token": response_log_joe['token'], "handle_str": ""}
    requests.put(f'{BASE_URL}user/profile/sethandle/v1', json = sethandle_info_joe)

    response_data = response.json()
    assert response_data['code'] == 400

def test_user_all_output(setup):
    response_log_joe, _ = setup
    user_all_info = {"token": response_log_joe["token"]}
    response = requests.get(f'{BASE_URL}users/all/v1', json = user_all_info)
    response_data = response.json()
    assert response_data == [
        {'email': 'joe123@gmail.com',
        'handle_str': 'joesmith',
         'is_remove': False,
         'name_first': 'Joe',
         'name_last': 'Smith',
         'u_id': 0},
        # {'email': 'marryjoe222@gmail.com',
        #  'handle_str': 'marryjoe',
        #  'is_remove': False,
        #  'name_first': 'Marry',
        #  'name_last': 'Joe',
        #  'u_id': 1}
    ]
    
def test_user_profile_output(setup):
    response_log_joe, _ = setup
    
    user_profile_info = {"token": response_log_joe['token'], "u_id": 1}
    
    response = requests.get(f'{BASE_URL}user/profile/v1', params = user_profile_info)
    response_data = response.json()
    assert response_data == {   
        'emails': 'marryjoe222@gmail.com',
        'first_names': 'Marry',
        'last_names': 'Joe',
        'user_handles': 'marryjoe',
        'user_id': 1}


def test_user_profile_removed(setup):
    response_log_joe, _ = setup
    
    user_profile_info = {"token": response_log_joe['token'], "u_id": 2,'removed_user':True}
    
    response = requests.get(f'{BASE_URL}user/profile/v1', params = user_profile_info)
    response_data = response.json()
    assert response_data == {   
           'code': 400,
         'message': '<p>This user does not exist!</p>',
          'name': 'System Error',}

# def test_user_profile_not_removed(setup):
#     response_log_joe, _ = setup
    
#     user_profile_info = {"token": response_log_joe['token'], "u_id": 2,'removed_user':False}
    
#     response = requests.get(f'{BASE_URL}user/profile/v1', params = user_profile_info)
#     response_data = response.json()
#     assert response_data == {   
#         'emails': 'marryjoe222@gmail.com',
#         'first_names': 'Marry',
#         'last_names': 'Joe',
#         'user_handles': 'marryjoe',
#         'user_id': 2
#         }

# def test_user_profile_user_removed(setup):
#     response_log_joe, _ = setup
    
#     user_profile_info = {"token": response_log_joe['token'], "u_id": 3,'removed_user':True}
    
#     response = requests.get(f'{BASE_URL}user/profile/v1', params = user_profile_info)
#     response_data = response.json()
#     assert response_data == {   
#         # 'emails': 'marryjoe222@gmail.com',
#         # 'first_names': 'Marry',
#         # 'last_names': 'Joe',
#         # 'user_handles': 'marryjoe',
#         # 'user_id': 0
#         }


def test_user_handle_short_and_not_alphanumeric(setup):
    response_log_joe, _ = setup
    sethandle_info = {"token": response_log_joe['token'], "handle_str": "a!"}
    response = requests.put(f'{BASE_URL}user/profile/sethandle/v1', json=sethandle_info)
    response_data = response.json()
    assert response_data['code'] == 400


def test_user_handle_long_and_not_alphanumeric(setup):
    response_log_joe, _ = setup
    sethandle_info = {"token": response_log_joe['token'], "handle_str": "abcdefghijklmnopqrstuvwxyz!"}
    response = requests.put(f'{BASE_URL}user/profile/sethandle/v1', json=sethandle_info)
    response_data = response.json()
    assert response_data['code'] == 400


def test_user_handle_empty(setup):
    response_log_joe, _ = setup
    sethandle_info = {"token": response_log_joe['token'], "handle_str": ""}
    response = requests.put(f'{BASE_URL}user/profile/sethandle/v1', json=sethandle_info)
    response_data = response.json()
    assert response_data['code'] == 400

def test_user_handle_number(setup):
    response_log_joe, _ = setup
    sethandle_info = {"token": response_log_joe['token'], "handle_str": 888}
    response = requests.put(f'{BASE_URL}user/profile/sethandle/v1', json=sethandle_info)
    response_data = response.json()
    assert response_data['code'] == 500



def test_user_handle_duplicate_long(setup):
    response_log_joe, response_log_marry = setup

    sethandle_info_joe = {"token": response_log_joe['token'], "handle_str": "abcdefghijklmnopqrstuvwxyz"}
    requests.put(f'{BASE_URL}user/profile/sethandle/v1', json = sethandle_info_joe)
    sethandle_info_marry = {"token": response_log_marry['token'], "handle_str": "abcdefghijklmnopqrstuvwxyz"}
    response = requests.put(f'{BASE_URL}user/profile/sethandle/v1', json = sethandle_info_marry)
    response_data = response.json()
    assert response_data['code'] == 400


def test_user_handle_duplicate_short(setup):
    response_log_joe, response_log_marry = setup

    sethandle_info_joe = {"token": response_log_joe['token'], "handle_str": "a"}
    requests.put(f'{BASE_URL}user/profile/sethandle/v1', json = sethandle_info_joe)
    sethandle_info_marry = {"token": response_log_marry['token'], "handle_str": "a"}
    response = requests.put(f'{BASE_URL}user/profile/sethandle/v1', json = sethandle_info_marry)
    response_data = response.json()
    assert response_data['code'] == 400

def test_user_handle_duplicate_not_alphanumeric(setup):
    response_log_joe, response_log_marry = setup

    sethandle_info_joe = {"token": response_log_joe['token'], "handle_str": "abc!"}
    requests.put(f'{BASE_URL}user/profile/sethandle/v1', json = sethandle_info_joe)
    sethandle_info_marry = {"token": response_log_marry['token'], "handle_str": "abc!"}
    response = requests.put(f'{BASE_URL}user/profile/sethandle/v1', json = sethandle_info_marry)
    response_data = response.json()
    assert response_data['code'] == 400

def test_user_handle_duplicate_not_alphanumeric_short(setup):
    response_log_joe, response_log_marry = setup

    sethandle_info_joe = {"token": response_log_joe['token'], "handle_str": "a!"}
    requests.put(f'{BASE_URL}user/profile/sethandle/v1', json = sethandle_info_joe)
    sethandle_info_marry = {"token": response_log_marry['token'], "handle_str": "a!"}
    response = requests.put(f'{BASE_URL}user/profile/sethandle/v1', json = sethandle_info_marry)
    response_data = response.json()
    assert response_data['code'] == 400

def test_user_handle_duplicate_not_alphanumeric_long(setup):
    response_log_joe, response_log_marry = setup

    sethandle_info_joe = {"token": response_log_joe['token'], "handle_str": "abcdefghijklmnopqrstuvwxyz!"}
    requests.put(f'{BASE_URL}user/profile/sethandle/v1', json = sethandle_info_joe)
    sethandle_info_marry = {"token": response_log_marry['token'], "handle_str": "abcdefghijklmnopqrstuvwxyz!"}
    response = requests.put(f'{BASE_URL}user/profile/sethandle/v1', json = sethandle_info_marry)
    response_data = response.json()
    assert response_data['code'] == 400


def test_user_handle_duplicate_not_alphanumeric_empty(setup):
    response_log_joe, response_log_marry = setup

    sethandle_info_joe = {"token": response_log_joe['token'], "handle_str": ""}
    requests.put(f'{BASE_URL}user/profile/sethandle/v1', json = sethandle_info_joe)
    sethandle_info_marry = {"token": response_log_marry['token'], "handle_str": ""}
    response = requests.put(f'{BASE_URL}user/profile/sethandle/v1', json = sethandle_info_marry)
    response_data = response.json()
    assert response_data['code'] == 400
# Test for handle
# def test_user_handle_too_short(setup):
#     response_log_joe, response_log_marry = setup
#     sethandle_info = {"token": response_log_joe["token"], "handle_str": "a"}
#     response = requests.put(f'{BASE_URL}/user/profile/sethandle/v1', json = sethandle_info)
#     response_data = response.json()
#     assert response_data['code'] == 400

# def test_user_handle_too_long(setup):
#     response_log_joe, response_log_marry = setup
#     sethandle_info = {"token": response_log_joe["token"], "handle_str": "comp1531abcdefghijklmnopqrstuvwxyz"}
#     response = requests.put(f'{BASE_URL}/user/profile/sethandle/v1', json = sethandle_info)
#     response_data = response.json()
#     assert response_data['code'] == 400

# def test_user_handle_not_alphanumeric(setup):
#     response_log_joe, response_log_marry = setup
#     sethandle_info = {"token": response_log_joe["token"], "handle_str": "a*b+c"}
#     response = requests.put(f'{BASE_URL}/user/profile/sethandle/v1', json = sethandle_info)
#     response_data = response.json()
#     assert response_data['code'] == 400

# def test_user_handle_duplication(setup):
#     response_log_joe, response_log_marry = setup
#     sethandle_info1 = {"token": response_log_joe["token"], "handle_str": "abcde"}
#     sethandle_info2 = {"token": response_log_joe["token"], "handle_str": "abcde"}
#     response = requests.put(f'{BASE_URL}/user/profile/sethandle/v1', json = sethandle_info2)
#     response_data = response.json()
#     assert response_data['code'] == 400
