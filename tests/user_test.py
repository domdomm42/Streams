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



# Test for user all and user profile

# Test invalid u id
def test_user_u_id_invalid(setup):
    
    # Load data from setup
    response_log_joe, _ = setup

    # Input invalid u id "100"
    user_profile_info = {"token": response_log_joe['token'], "u_id": 100}

    response = requests.get(f'{BASE_URL}user/profile/v1', params=user_profile_info)
    response_data = response.json()
    
    # Raise InputError, u id does not refer to a valid user
    assert response_data['code'] == 400




# Test valid u id
def test_valid_u_id(setup):
    
    # Load data from setup
    response_log_joe, _ = setup
    
    # Input valid u id
    user_profile_info = {"token": response_log_joe['token'], "u_id": 0}
    response = requests.get(f'{BASE_URL}user/profile/v1', params=user_profile_info)
    response_data = response.json()
    
    # Match the corresponding data
    assert response_data == {
        'emails': 'joe123@gmail.com',
        'first_names': 'Joe',
        'last_names': 'Smith',
        'user_handles': 'joesmith',
        'user_id': 0,
    }






# Test valid user all
def test_user_all_output(setup):
    
    # Load data from setup
    response_log_joe, _ = setup
    user_all_info = {"token": response_log_joe["token"]}
    response = requests.get(f'{BASE_URL}users/all/v1', json=user_all_info)
    response_data = response.json()
        
        
    # Match the corresponding data
    assert response_data == [
        {'email': 'joe123@gmail.com',
         'handle_str': 'joesmith',
         'name_first': 'Joe',
         'name_last': 'Smith',
         'u_id': 0},
         {'email': 'marryjoe222@gmail.com',
         'handle_str': 'marryjoe',
         'name_first': 'Marry',
         'name_last': 'Joe',
         'u_id': 1},

    ]


# Test valid user profile
def test_user_profile_output(setup):
    
    # Load data from setup
    response_log_joe, _ = setup

    user_profile_info = {"token": response_log_joe['token'], "u_id": 1}

    response = requests.get(f'{BASE_URL}user/profile/v1', params=user_profile_info)
    response_data = response.json()
    
    # Match the corresponding data
    assert response_data == {
        'emails': 'marryjoe222@gmail.com',
        'first_names': 'Marry',
        'last_names': 'Joe',
        'user_handles': 'marryjoe',
        'user_id': 1}





# Test for name

# Test invalid short first name
def test_user_name_first_too_short(setup):
    
    # Load data from setup
    response_log_joe, _ = setup

    # Last name is valid, last name out of range (1-50 characters)
    setname_info = {"token": response_log_joe["token"], "first_names": "", "last_names": "a"}
    response = requests.put(f'{BASE_URL}user/profile/setname/v1', json=setname_info)
    response_data = response.json()

    # Raise InputError, length of first name is not between 1 and 50
    assert response_data['code'] == 400


# Test invalid short last name
def test_user_name_last_too_short(setup):
    
    # Load data from setup
    response_log_joe, _ = setup

    # First name is valid, last name out of range (1-50 characters)
    setname_info = {"token": response_log_joe["token"], "first_names": "a", "last_names": ""}
    response = requests.put(f'{BASE_URL}user/profile/setname/v1', json=setname_info)
    response_data = response.json()
    
    # Raise InputError, length of last name is not between 1 and 50    
    assert response_data['code'] == 400



# Test invalid long first name
def test_user_name_first_too_long(setup):
    
    # Load data from setup
    response_log_joe, _ = setup
    
    # Last name is valid, first name out of range (1-50 characters)
    setname_info = {"token": response_log_joe["token"],
                    "first_names": "abcdefghijklmnopqrstuvwxyz1531abcdefghijklmnopqrstuvwxyz", "last_names": "a"}
    response = requests.put(f'{BASE_URL}user/profile/setname/v1', json=setname_info)
    response_data = response.json()
    
    # Raise InputError, length of first name is not between 1 and 50
    assert response_data['code'] == 400



# Test invalid long last name
def test_user_name_last_too_long(setup):
    
    # Load data from setup
    response_log_joe, _ = setup  
    
    # First name is valid, last name out of range (1-50 characters)
    setname_info = {"token": response_log_joe["token"], "first_names": 'a',
                    "last_names": "abcdefghijklmnopqrstuvwxyz1531abcdefghijklmnopqrstuvwxyz"}
    response = requests.put(f'{BASE_URL}user/profile/setname/v1', json=setname_info)
    response_data = response.json()

    # Raise InputError, length of last name is not between 1 and 50
    assert response_data['code'] == 400





# Test name duplications
def test_user_name_duplication(setup):
   
    # Load data from setup
    response_log_joe, response_log_marry = setup
    
    

    # Two same names "a" "Smith",  there are no restrictions
    setname_info1 = {"token": response_log_joe["token"], "first_names": "a", "last_names": "Smith"}
    setname_info2 = {"token": response_log_marry["token"], "first_names": "a", "last_names": "Smith"}

    requests.put(f'{BASE_URL}user/profile/setname/v1', json=setname_info1)
    response = requests.put(f'{BASE_URL}user/profile/setname/v1', json=setname_info2)

    response_data = response.json()
    assert response_data == {}



# Test for valid first and last names
def test_valid_name(setup):
    
    # Load data from setup
    response_log_joe, _ = setup
    
    # Input valid first name "a" and valid last "b"
    setname_info = {"token": response_log_joe['token'], "first_names": "a", "last_names": "b"}
    requests.put(f'{BASE_URL}user/profile/setname/v1', json=setname_info)
    user_profile_info = {"token": response_log_joe['token'], "u_id": 0}
    response = requests.get(f'{BASE_URL}user/profile/v1', params=user_profile_info)
    response_data = response.json()
    
    # Match the corresponding data
    assert response_data == {
        'emails': 'joe123@gmail.com',
        'first_names': 'a',
        'last_names': 'b',
        'user_handles': 'joesmith',
        'user_id': 0,
    }






# Test for email

#Test email duplication
def test_user_email_duplication(setup):
    
    # Load data from setup
    response_log_joe, response_log_marry = setup
    
    # Input two same emails
    setemail_info1 = {"token": response_log_joe["token"], "emails": "kobebryant24881@gmail.com"}
    setemail_info2 = {"token": response_log_marry["token"], "emails": "kobebryant24881@gmail.com"}

    requests.put(f'{BASE_URL}user/profile/setemail/v1', json=setemail_info1)
    response = requests.put(f'{BASE_URL}user/profile/setemail/v1', json=setemail_info2)

    response_data = response.json()
    
    # Raise InputError, email is already being used by others
    assert response_data['code'] == 400




# Test two similar email, one lowercase the other uppercase
def test_user_email_duplication_invalid_capital(setup):
    
    # Load data from setup
    response_log_joe, response_log_marry = setup
    
    # One lowercase the other uppercase
    setemail_info1 = {"token": response_log_joe["token"], "emails": "aaa@gmail.com"}
    setemail_info2 = {"token": response_log_marry["token"], "emails": "AAA@gmail.com"}

    requests.put(f'{BASE_URL}user/profile/setemail/v1', json=setemail_info1)
    response = requests.put(f'{BASE_URL}user/profile/setemail/v1', json=setemail_info2)

    response_data = response.json()
    assert response_data == {}



# Test invalid email
def test_user_email_invalid(setup):
    
    # Load data from setup
    response_log_joe, _ = setup
    
    # Input "abcde" is invalid 
    setemail_info = {"token": response_log_joe["token"], "emails": "abcde"}
    response = requests.put(f'{BASE_URL}user/profile/setemail/v1', json=setemail_info)
    response_data = response.json()
    
    # Raise InputError, email is not valid
    assert response_data['code'] == 400




# Test valid user email
def test_valid_email(setup):

    # Load data from setup
    response_log_joe, _ = setup
    setemail_info = {"token": response_log_joe['token'], "emails": "joe123@gmail.com"}
    requests.put(f'{BASE_URL}user/profile/setemail/v1', json=setemail_info)
    user_profile_info = {"token": response_log_joe['token'], "u_id": 0}
    response = requests.get(f'{BASE_URL}user/profile/v1', params=user_profile_info)
    response_data = response.json()
    
    # Match the corresponding data
    assert response_data == {
        'emails': 'joe123@gmail.com',
        'first_names': 'Joe',
        'last_names': 'Smith',
        'user_handles': 'joesmith',
        'user_id': 0,
    }






# Test for handle

# Test invalid short handle
def test_user_handle_too_short(setup):
    
    # Load data from setup
    response_log_joe, _ = setup
    
    
    # Input invalid short handle 'a', out of range (3-20)
    sethandle_info = {"token": response_log_joe['token'], "handle_str": "a"}
    response = requests.put(f'{BASE_URL}user/profile/sethandle/v1', json=sethandle_info)
    response_data = response.json()
    
    # Raise InputError, length of handle_str is not between 3 and 20
    assert response_data['code'] == 400


# Test invalid long handle
def test_user_handle_too_long(setup):
    
    # Load data from setup
    response_log_joe, _ = setup
    

    # Input invalid long handle 'longlonglonglonglonglong', out of range (3-20)
    sethandle_info = {"token": response_log_joe['token'], "handle_str": "longlonglonglonglonglong"}
    response = requests.put(f'{BASE_URL}user/profile/sethandle/v1', json=sethandle_info)
    response_data = response.json()
    
    # Raise InputError, length of handle_str is not between 3 and 20    
    assert response_data['code'] == 400


# Test not alphanumeric handle
def test_user_handle_contains_not_alnum(setup):
    
    # Load data from setup
    response_log_joe, _ = setup
    
    # Input invalid not alphanumeric handle 'my_name!'
    sethandle_info = {"token": response_log_joe['token'], "handle_str": "my_name!"}
    response = requests.put(f'{BASE_URL}user/profile/sethandle/v1', json=sethandle_info)
    response_data = response.json()

    # Raise InputError, handle_str contains characters that are not alphanumeric
    assert response_data['code'] == 400



# Test handle duplication
def test_user_handle_duplicate(setup):
    
    # Load data from setup
    response_log_joe, response_log_marry = setup


    # Input two same handles
    sethandle_info_joe = {"token": response_log_joe['token'], "handle_str": "KobeBryant"}
    requests.put(f'{BASE_URL}user/profile/sethandle/v1', json=sethandle_info_joe)
    sethandle_info_marry = {"token": response_log_marry['token'], "handle_str": "KobeBryant"}
    response = requests.put(f'{BASE_URL}user/profile/sethandle/v1', json=sethandle_info_marry)
    response_data = response.json()
    
    # Raise InputError, the handle is already being used by others
    assert response_data['code'] == 400



# Test similar handle, one lowercase the other uppcase
def test_user_handle_duplicate_capital(setup):
    
    # Load data from setup
    response_log_joe, response_log_marry = setup

    # Two handles, one lowercase, the other uppcase
    sethandle_info_joe = {"token": response_log_joe['token'], "handle_str": "aaa"}
    requests.put(f'{BASE_URL}user/profile/sethandle/v1', json=sethandle_info_joe)
    sethandle_info_marry = {"token": response_log_marry['token'], "handle_str": "AAA"}
    response = requests.put(f'{BASE_URL}user/profile/sethandle/v1', json=sethandle_info_marry)
    response_data = response.json()
    assert response_data == {}



# Test valid handle
def test_valid_handle(setup):
    
    # Load data from setup
    response_log_joe, _ = setup
    
    # Input valid user handle
    sethandle_info = {"token": response_log_joe['token'], "handle_str": "KobeBryant"}
    requests.put(f'{BASE_URL}user/profile/sethandle/v1', json=sethandle_info)
    user_profile_info = {"token": response_log_joe['token'], "u_id": 0}
    response = requests.get(f'{BASE_URL}user/profile/v1', params=user_profile_info)
    response_data = response.json()
    
    # Match the corresponding data
    assert response_data == {
        'emails': 'joe123@gmail.com',
        'first_names': 'Joe',
        'last_names': 'Smith',
        'user_handles': 'KobeBryant',
        'user_id': 0,
    }


