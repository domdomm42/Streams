import pytest
import requests
import jwt
from src.auth_auth_helpers import SECRET
from src.config import *

BASE_URL = url
ACCESS_ERROR = 403
INPUT_ERROR = 400

# Test invalid emails
def test_register_invalid_email():
    user_info = {"email": "joe123.com", "password": "password", "name_first": "Joe", "name_last": "Smith"}

    # register user using invalid user_info
    response = requests.post(f'{BASE_URL}/auth/register/v2', json = user_info)
    response_data = response.json()
    assert response_data['code'] == INPUT_ERROR

def test_register_invalid_email_2():
    user_info = {"email": "anika.com", "password": "password", "name_first": "Joe", "name_last": "Smith"}

    # register user using invalid user_info
    response = requests.post(f'{BASE_URL}/auth/register/v2', json = user_info)
    response_data = response.json()
    assert response_data['code'] == INPUT_ERROR

def test_register_invalid_email_3():
    user_info = {"email": " ", "password": "password", "name_first": "Joe", "name_last": "Smith"}

    # register user using invalid user_info
    response = requests.post(f'{BASE_URL}/auth/register/v2', json = user_info)
    response_data = response.json()
    assert response_data['code'] == INPUT_ERROR

def test_register_invalid_email_4():
    user_info = {"email": "@.com", "password": "password", "name_first": "Joe", "name_last": "Smith"}

    # register user using invalid user_info
    response = requests.post(f'{BASE_URL}/auth/register/v2', json = user_info)
    response_data = response.json()
    assert response_data['code'] == INPUT_ERROR

def test_register_invalid_email_5():
    user_info = {"email": "2342ras@43", "password": "password", "name_first": "Joe", "name_last": "Smith"}
    
    # register user using invalid user_info
    response = requests.post(f'{BASE_URL}/auth/register/v2', json = user_info)
    response_data = response.json()
    assert response_data['code'] == INPUT_ERROR

def test_register_invalid_email_6():
    user_info = {"email": "dklshfdoshfokishjfoihwokjbhfd", "password": "password", "name_first": "Joe", "name_last": "Smith"}

    # register user using invalid user_info
    response = requests.post(f'{BASE_URL}/auth/register/v2', json = user_info)
    response_data = response.json()
    assert response_data['code'] == INPUT_ERROR

def test_register_invalid_email_7():
    user_info = {"email": "marry.joe!@gmail.com", "password": "password", "name_first": "Joe", "name_last": "Smith"}

    # register user using invalid user_info
    response = requests.post(f'{BASE_URL}/auth/register/v2', json = user_info)
    response_data = response.json()
    assert response_data['code'] == INPUT_ERROR

# Test valid emails
def test_register_valid_email():
    
    requests.delete(f'{BASE_URL}/clear/v1')

    user_info = {"email": "joe123@gmail.com", "password": "password", "name_first": "Joe", "name_last": "Smith"}

    # register user using valid user_info
    response = requests.post(f'{BASE_URL}/auth/register/v2', json = user_info)
    response_data = response.json()
    assert response_data['token'] == jwt.encode({'user_id': 0, 'session_id': 1}, SECRET, algorithm='HS256')
    assert response_data['auth_user_id'] == 0

def test_register_valid_email_2():

    requests.delete(f'{BASE_URL}/clear/v1')
    
    user_info = {"email": "marryjoe222@gmail.com", "password": "password", "name_first": "Marry", "name_last": "Joe"}

    # register user using valid user_info
    response = requests.post(f'{BASE_URL}/auth/register/v2', json = user_info)
    response_data = response.json()
    assert response_data['token'] == jwt.encode({'user_id': 0, 'session_id': 1}, SECRET, algorithm='HS256')
    assert response_data['auth_user_id'] == 0

def test_register_valid_email_3():
    
    requests.delete(f'{BASE_URL}/clear/v1')

    user_info = {"email": "marryjoe222@gmail.com", "password": "password", "name_first": "Marry", "name_last": "Joe"}

    # register user using valid user_info
    response = requests.post(f'{BASE_URL}/auth/register/v2', json = user_info)
    response_data = response.json()
    assert response_data['token'] == jwt.encode({'user_id': 0, 'session_id': 1}, SECRET, algorithm='HS256')
    assert response_data['auth_user_id'] == 0

    user_info = {"email": "jimmyjoe@gmail.com", "password": "password", "name_first": "Jimmy", "name_last": "Joe"}
    response = requests.post(f'{BASE_URL}/auth/register/v2', json = user_info)
    response_data = response.json()
    assert response_data['token'] == jwt.encode({'user_id': 1, 'session_id': 2}, SECRET, algorithm='HS256')
    assert response_data['auth_user_id'] == 1

# Test duplicate emails
def test_register_duplicate_email():

    requests.delete(f'{BASE_URL}/clear/v1')

    user_info = {"email": "joe123@gmail.com", "password": "password", "name_first": "Joe", "name_last": "Smith"}
    response = requests.post(f'{BASE_URL}/auth/register/v2', json = user_info)

    # registering the same user twice
    user_info = {"email": "joe123@gmail.com", "password": "password2", "name_first": "Joe2", "name_last": "Smith2"}
    response = requests.post(f'{BASE_URL}/auth/register/v2', json = user_info)
    response_data = response.json()
    assert response_data['code'] == INPUT_ERROR

# Test invalid password (<6 characters)
def test_invalid_password():

    requests.delete(f'{BASE_URL}/clear/v1')
    
    # Registering password thats too short
    user_info = {"email": "joe123@gmail.com", "password": "joe", "name_first": "Joe", "name_last": "Smith"}
    response = requests.post(f'{BASE_URL}/auth/register/v2', json = user_info)
    response_data = response.json()
    assert response_data['code'] == INPUT_ERROR

def test_invalid_password_2():

    requests.delete(f'{BASE_URL}/clear/v1')
    
    # Registering short password
    user_info = {"email": "joe123@gmail.com", "password": "123", "name_first": "Joe", "name_last": "Smith"}
    response = requests.post(f'{BASE_URL}/auth/register/v2', json = user_info)
    response_data = response.json()
    assert response_data['code'] == INPUT_ERROR

def test_invalid_password_3():

    requests.delete(f'{BASE_URL}/clear/v1')
    
    # Registering short password
    user_info = {"email": "joe123@gmail.com", "password": " ", "name_first": "Joe", "name_last": "Smith"}
    response = requests.post(f'{BASE_URL}/auth/register/v2', json = user_info)
    response_data = response.json()
    assert response_data['code'] == INPUT_ERROR

def test_invalid_password_4():

    requests.delete(f'{BASE_URL}/clear/v1')
    
    # Registering no password
    user_info = {"email": "joe123@gmail.com", "password": "", "name_first": "Joe", "name_last": "Smith"}
    response = requests.post(f'{BASE_URL}/auth/register/v2', json = user_info)
    response_data = response.json()
    assert response_data['code'] == INPUT_ERROR

# Test invalid first name (not 1 <= characters <= 50)
def test_invalid_first_name():

    requests.delete(f'{BASE_URL}/clear/v1')
    
    # Registering no first name
    user_info = {"email": "joe123@gmail.com", "password": "password", "name_first": "", "name_last": "Smith"}
    response = requests.post(f'{BASE_URL}/auth/register/v2', json = user_info)
    response_data = response.json()
    assert response_data['code'] == INPUT_ERROR

def test_invalid_first_name_2():

    requests.delete(f'{BASE_URL}/clear/v1')
    
    # Registering first name thats too long
    user_info = {"email": "joe123@gmail.com", "password": "password", "name_first": "J"*51, "name_last": "Smith"}
    response = requests.post(f'{BASE_URL}/auth/register/v2', json = user_info)
    response_data = response.json()
    assert response_data['code'] == INPUT_ERROR

# Test invalid last name (not 1 <= characters <= 50)
def test_invalid_last_name():

    requests.delete(f'{BASE_URL}/clear/v1')
    
    # Registering no last name
    user_info = {"email": "joe123@gmail.com", "password": "password", "name_first": "Joe", "name_last": ""}
    response = requests.post(f'{BASE_URL}/auth/register/v2', json = user_info)
    response_data = response.json()
    assert response_data['code'] == INPUT_ERROR

def test_invalid_last_name_2():

    requests.delete(f'{BASE_URL}/clear/v1')
    
    # Registering last name that is too long
    user_info = {"email": "joe123@gmail.com", "password": "password", "name_first": "Joe", "name_last": "S"*51}
    response = requests.post(f'{BASE_URL}/auth/register/v2', json = user_info)
    response_data = response.json()
    assert response_data['code'] == INPUT_ERROR

 #########################################################################
 #########################################################################

# Test unregistered email 
def test_unregistered_email():
    requests.delete(f'{BASE_URL}/clear/v1')

    # Logging in with unregistered data
    user_info = {"email": "joe123@gmail.com", "password": "password"}
    response = requests.post(f'{BASE_URL}/auth/login/v2', json = user_info)
    response_data = response.json()
    assert response_data['code'] == INPUT_ERROR


def test_unregistered_email_2():
    requests.delete(f'{BASE_URL}/clear/v1')

    # Logging in with unregistered data
    user_info = {"email": "anika.com", "password": "password"}
    response = requests.post(f'{BASE_URL}/auth/login/v2', json = user_info)
    response_data = response.json()
    assert response_data['code'] == INPUT_ERROR


def test_unregistered_email_3():
    requests.delete(f'{BASE_URL}/clear/v1')

    # Logging in with unregistered data
    user_info = {"email": "", "password": "password"}
    response = requests.post(f'{BASE_URL}/auth/login/v2', json = user_info)
    response_data = response.json()
    assert response_data['code'] == INPUT_ERROR


def test_unregisterd_email_4():
    requests.delete(f'{BASE_URL}/clear/v1')

    # Logging in with unregistered data
    user_info = {"email": ".com", "password": "password"}
    response = requests.post(f'{BASE_URL}/auth/login/v2', json = user_info)
    response_data = response.json()
    assert response_data['code'] == INPUT_ERROR

def test_unregistered_email_5():
    requests.delete(f'{BASE_URL}/clear/v1')

    # Logging in with unregistered data
    user_info = {"email": "@.com", "password": "password"}
    response = requests.post(f'{BASE_URL}/auth/login/v2', json = user_info)
    response_data = response.json()
    assert response_data['code'] == INPUT_ERROR


def test_unregisted_email_6():
    requests.delete(f'{BASE_URL}/clear/v1')

    # Logging in with unregistered data
    user_info = {"email": "2342ras@43", "password": "password"}
    response = requests.post(f'{BASE_URL}/auth/login/v2', json = user_info)
    response_data = response.json()
    assert response_data['code'] == INPUT_ERROR

def test_unregisted_email_7():
    requests.delete(f'{BASE_URL}/clear/v1')

    # Logging in with unregistered data
    user_info = {"email": "dklshfdoshfokishjfoihwokjbhfd", "password": "password"}
    response = requests.post(f'{BASE_URL}/auth/login/v2', json = user_info)
    response_data = response.json()
    assert response_data['code'] == INPUT_ERROR

def test_unregistered_email_8():
    requests.delete(f'{BASE_URL}/clear/v1')

    # Logging in with unregistered data
    user_info = {"email": "marry.joe!@gmail.com", "password": "password"}
    response = requests.post(f'{BASE_URL}/auth/login/v2', json = user_info)
    response_data = response.json()
    assert response_data['code'] == INPUT_ERROR

def test_unregistered_email_9():
    requests.delete(f'{BASE_URL}/clear/v1')

    # Logging in with unregistered data
    user_info = {"email": "wolffangdan", "password": "dancarry"}
    response = requests.post(f'{BASE_URL}/auth/login/v2', json = user_info)
    response_data = response.json()
    assert response_data['code'] == INPUT_ERROR


# # Test registered email
def test_registered_email():
    requests.delete(f'{BASE_URL}/clear/v1')


    user_info_reg = {"email": "joe123@gmail.com", "password": "password", "name_first": "Joe", "name_last": "Smith"}
    user_info_login = {"email": "joe123@gmail.com", "password": "password"}

    # Registering user
    requests.post(f'{BASE_URL}/auth/register/v2', json = user_info_reg)
    # Logging in with correct user data
    response_log = requests.post(f'{BASE_URL}/auth/login/v2', json = user_info_login) 
    response_log = response_log.json()
    assert response_log['token'] == jwt.encode({'user_id': 0, 'session_id': 2}, SECRET, algorithm='HS256')

def test_registered_email_2():
    requests.delete(f'{BASE_URL}/clear/v1')

    user_info_reg = {"email": "marryjoe222@gmail.com", "password": "passwordM", "name_first": "Marry", "name_last": "Joe"}
    user_info_login = {"email": "marryjoe222@gmail.com", "password": "passwordM"}

    # Registering user
    requests.post(f'{BASE_URL}/auth/register/v2', json = user_info_reg)
    # Logging in with correct user data
    response_log = requests.post(f'{BASE_URL}/auth/login/v2', json = user_info_login)
    response_log = response_log.json()
    assert response_log['token'] == jwt.encode({'user_id': 0, 'session_id': 2}, SECRET, algorithm='HS256')


def test_registered_email_3():
    requests.delete(f'{BASE_URL}/clear/v1')

    user_info_reg = {"email": "davidmo@gmail.com", "password": "passwordD", "name_first": "David", "name_last": "Mo"}
    user_info_login = {"email": "davidmo@gmail.com", "password": "passwordD"}

    # Registering with user data
    requests.post(f'{BASE_URL}/auth/register/v2', json = user_info_reg)
    # Logging in with correct user data
    response_log = requests.post(f'{BASE_URL}/auth/login/v2', json = user_info_login)
    response_log = response_log.json()
    assert response_log['token'] == jwt.encode({'user_id': 0, 'session_id': 2}, SECRET, algorithm='HS256')

# Testing for unmatched password
def test_wrong_password():
    requests.delete(f'{BASE_URL}/clear/v1')

    user_info_reg = {"email": "davidmo@gmail.com", "password": "passwordD", "name_first": "David", "name_last": "Mo"}
    user_info_login = {"email": "davidmo@gmail.com", "password": "passwordy"}

    requests.post(f'{BASE_URL}/auth/register/v2', json = user_info_reg)

    # Logging on with wrong password
    response_log = requests.post(f'{BASE_URL}/auth/login/v2', json = user_info_login)
    response_log_data = response_log.json()
    assert response_log_data['code'] == INPUT_ERROR

def test_wrong_password_2():
    requests.delete(f'{BASE_URL}/clear/v1')

    user_info_reg = {"email": "marryjoe222@gmail.com", "password": "yayayaoyy", "name_first": "Marry", "name_last": "Joe"}
    user_info_login = {"email": "marryjoe222@gmail.com", "password": "passwordy"}

    requests.post(f'{BASE_URL}/auth/register/v2', json = user_info_reg)

    # Logging on with wrong password
    response_log = requests.post(f'{BASE_URL}/auth/login/v2', json = user_info_login)
    response_log_data = response_log.json()
    assert response_log_data['code'] == INPUT_ERROR


def test_wrong_password_3():
    requests.delete(f'{BASE_URL}/clear/v1')

    user_info_login = {"email": "marryjoe222@gmail.com", "password": "passwordy"}

    # Logging on to a unregistered account
    response_log = requests.post(f'{BASE_URL}/auth/login/v2', json = user_info_login)
    response_log_data = response_log.json()
    assert response_log_data['code'] == INPUT_ERROR


# Logout Tests
def test_double_logout():
    requests.delete(f'{BASE_URL}/clear/v1')
    user_info_reg_1 = {"email": "marryjoe@gmail.com", "password": "password", "name_first": "Marry", "name_last": "Joe"}
    
    response_data = requests.post(f'{BASE_URL}/auth/register/v2', json = user_info_reg_1)

    user_info_logout = response_data.json()
    user_info_logout = {'token': user_info_logout['token']} 

    # Logging out twice
    requests.post(f'{BASE_URL}/auth/logout/v1', json = user_info_logout)
    return_value = requests.post(f'{BASE_URL}/auth/logout/v1', json = user_info_logout)

    return_value = return_value.json()
    assert return_value['code'] == ACCESS_ERROR

