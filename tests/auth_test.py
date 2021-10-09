import pytest
import requests
from src.auth import auth_login_v1, auth_register_v1
from src.error import InputError
from src.other import clear_v1

BASE_URL = 'http://127.0.0.1:6564'

# def test_http():

#     user_info = {"email": "joe123@gmail.com", "password": "password", "name_first": "Joe", "name_last": "Smith"}

#     response = requests.post(f'{BASE_URL}/auth/register/v2', json = user_info)
#     response_data = response.json()

#     print(response_data)

#     assert response_data['auth_user_id'] == 0

# Test invalid emails
def test_register_invalid_email():
    user_info = {"email": "joe123.com", "password": "password", "name_first": "Joe", "name_last": "Smith"}
    response = requests.post(f'{BASE_URL}/auth/register/v2', json = user_info)
    response_data = response.json()
    assert response_data['code'] == 400

def test_register_invalid_email_2():
    user_info = {"email": "anika.com", "password": "password", "name_first": "Joe", "name_last": "Smith"}
    response = requests.post(f'{BASE_URL}/auth/register/v2', json = user_info)
    response_data = response.json()
    assert response_data['code'] == 400

def test_register_invalid_email_3():
    user_info = {"email": " ", "password": "password", "name_first": "Joe", "name_last": "Smith"}
    response = requests.post(f'{BASE_URL}/auth/register/v2', json = user_info)
    response_data = response.json()
    assert response_data['code'] == 400

def test_register_invalid_email_4():
    user_info = {"email": "@.com", "password": "password", "name_first": "Joe", "name_last": "Smith"}
    response = requests.post(f'{BASE_URL}/auth/register/v2', json = user_info)
    response_data = response.json()
    assert response_data['code'] == 400

def test_register_invalid_email_5():
    user_info = {"email": "2342ras@43", "password": "password", "name_first": "Joe", "name_last": "Smith"}
    response = requests.post(f'{BASE_URL}/auth/register/v2', json = user_info)
    response_data = response.json()
    assert response_data['code'] == 400

def test_register_invalid_email_6():
    user_info = {"email": "dklshfdoshfokishjfoihwokjbhfd", "password": "password", "name_first": "Joe", "name_last": "Smith"}
    response = requests.post(f'{BASE_URL}/auth/register/v2', json = user_info)
    response_data = response.json()
    assert response_data['code'] == 400

def test_register_invalid_email_7():
    user_info = {"email": "marry.joe!@gmail.com", "password": "password", "name_first": "Joe", "name_last": "Smith"}
    response = requests.post(f'{BASE_URL}/auth/register/v2', json = user_info)
    response_data = response.json()
    assert response_data['code'] == 400

# Test valid emails
def test_register_valid_email():
    
    requests.delete(f'{BASE_URL}/clear/v1')

    user_info = {"email": "joe123@gmail.com", "password": "password", "name_first": "Joe", "name_last": "Smith"}
    response = requests.post(f'{BASE_URL}/auth/register/v2', json = user_info)
    response_data = response.json()
    assert response_data['token'] == '0'
    assert response_data['auth_user_id'] == 0

def test_register_valid_email_2():

    requests.delete(f'{BASE_URL}/clear/v1')
    
    user_info = {"email": "marryjoe222@gmail.com", "password": "password", "name_first": "Marry", "name_last": "Joe"}
    response = requests.post(f'{BASE_URL}/auth/register/v2', json = user_info)
    response_data = response.json()
    assert response_data['token'] == '0'
    assert response_data['auth_user_id'] == 0

def test_register_valid_email_3():
    
    requests.delete(f'{BASE_URL}/clear/v1')

    user_info = {"email": "marryjoe222@gmail.com", "password": "password", "name_first": "Marry", "name_last": "Joe"}
    response = requests.post(f'{BASE_URL}/auth/register/v2', json = user_info)
    response_data = response.json()
    assert response_data['token'] == '0'
    assert response_data['auth_user_id'] == 0

    user_info = {"email": "jimmyjoe@gmail.com", "password": "password", "name_first": "Jimmy", "name_last": "Joe"}
    response = requests.post(f'{BASE_URL}/auth/register/v2', json = user_info)
    response_data = response.json()
    assert response_data['token'] == '1'
    assert response_data['auth_user_id'] == 1

# Test duplicate emails
def test_register_duplicate_email():

    requests.delete(f'{BASE_URL}/clear/v1')

    user_info = {"email": "joe123@gmail.com", "password": "password", "name_first": "Joe", "name_last": "Smith"}
    response = requests.post(f'{BASE_URL}/auth/register/v2', json = user_info)

    user_info = {"email": "joe123@gmail.com", "password": "password2", "name_first": "Joe2", "name_last": "Smith2"}
    response = requests.post(f'{BASE_URL}/auth/register/v2', json = user_info)
    response_data = response.json()
    assert response_data['code'] == 400

# Test invalid password (<6 characters)
def test_invalid_password():

    requests.delete(f'{BASE_URL}/clear/v1')
    
    user_info = {"email": "joe123@gmail.com", "password": "joe", "name_first": "Joe", "name_last": "Smith"}
    response = requests.post(f'{BASE_URL}/auth/register/v2', json = user_info)
    response_data = response.json()
    assert response_data['code'] == 400

def test_invalid_password_2():

    requests.delete(f'{BASE_URL}/clear/v1')
    
    user_info = {"email": "joe123@gmail.com", "password": "123", "name_first": "Joe", "name_last": "Smith"}
    response = requests.post(f'{BASE_URL}/auth/register/v2', json = user_info)
    response_data = response.json()
    assert response_data['code'] == 400

def test_invalid_password_3():

    requests.delete(f'{BASE_URL}/clear/v1')
    
    user_info = {"email": "joe123@gmail.com", "password": " ", "name_first": "Joe", "name_last": "Smith"}
    response = requests.post(f'{BASE_URL}/auth/register/v2', json = user_info)
    response_data = response.json()
    assert response_data['code'] == 400

def test_invalid_password_4():

    requests.delete(f'{BASE_URL}/clear/v1')
    
    user_info = {"email": "joe123@gmail.com", "password": "", "name_first": "Joe", "name_last": "Smith"}
    response = requests.post(f'{BASE_URL}/auth/register/v2', json = user_info)
    response_data = response.json()
    assert response_data['code'] == 400

# Test invalid first name (not 1 <= characters <= 50)
def test_invalid_first_name():

    requests.delete(f'{BASE_URL}/clear/v1')
    
    user_info = {"email": "joe123@gmail.com", "password": "password", "name_first": "", "name_last": "Smith"}
    response = requests.post(f'{BASE_URL}/auth/register/v2', json = user_info)
    response_data = response.json()
    assert response_data['code'] == 400

def test_invalid_first_name_2():

    requests.delete(f'{BASE_URL}/clear/v1')
    
    user_info = {"email": "joe123@gmail.com", "password": "password", "name_first": "J"*51, "name_last": "Smith"}
    response = requests.post(f'{BASE_URL}/auth/register/v2', json = user_info)
    response_data = response.json()
    assert response_data['code'] == 400

# Test invalid last name (not 1 <= characters <= 50)
def test_invalid_last_name():

    requests.delete(f'{BASE_URL}/clear/v1')
    
    user_info = {"email": "joe123@gmail.com", "password": "password", "name_first": "Joe", "name_last": ""}
    response = requests.post(f'{BASE_URL}/auth/register/v2', json = user_info)
    response_data = response.json()
    assert response_data['code'] == 400

def test_invalid_last_name_2():

    requests.delete(f'{BASE_URL}/clear/v1')
    
    user_info = {"email": "joe123@gmail.com", "password": "password", "name_first": "Joe", "name_last": "S"*51}
    response = requests.post(f'{BASE_URL}/auth/register/v2', json = user_info)
    response_data = response.json()
    assert response_data['code'] == 400

 #########################################################################
 ############################################################################

# Test unregistered email 
def test_unregistered_email():
    requests.delete(f'{BASE_URL}/clear/v1')

    user_info = {"email": "joe123@gmail.com", "password": "password"}
    response = requests.post(f'{BASE_URL}/auth/login/v2', json = user_info)
    response_data = response.json()
    assert response_data['code'] == 400


# def test_unregistered_email_2():
#     requests.delete(f'{BASE_URL}/clear/v1')
#     with pytest.raises(InputError):
#         auth_login_v1('anika.com', 'password')

# def test_unregistered_email_3():
#     requests.delete(f'{BASE_URL}/clear/v1')
#     with pytest.raises(InputError):
#         auth_login_v1(' ', 'password')

# def test_unregisterd_email_4():
#     requests.delete(f'{BASE_URL}/clear/v1')
#     with pytest.raises(InputError):
#         auth_login_v1('.com', 'password')

# def test_unregistered_email_5():
#     requests.delete(f'{BASE_URL}/clear/v1')
#     with pytest.raises(InputError):
#         auth_login_v1('@.com', 'password')

# def test_unregisted_email_6():
#     requests.delete(f'{BASE_URL}/clear/v1')
#     with pytest.raises(InputError):
#         auth_login_v1('2342ras@43', 'password')

# def test_unregisted_email_7():
#     requests.delete(f'{BASE_URL}/clear/v1')
#     with pytest.raises(InputError):
#         auth_login_v1('dklshfdoshfokishjfoihwokjbhfd', 'password')

# def test_unregistered_email_8():
#     requests.delete(f'{BASE_URL}/clear/v1')
#     with pytest.raises(InputError):
#         auth_login_v1('marry.joe!@gmail.com', 'password')

# def test_unregistered_email_9():
#     requests.delete(f'{BASE_URL}/clear/v1')
#     with pytest.raises(InputError):
#         auth_login_v1('wolffangdan', 'dancarry')

# # Test registered email
# def test_registered_email():
#     requests.delete(f'{BASE_URL}/clear/v1')
#     register_userID = auth_register_v1('joe123@gmail.com', 'password', 'Joe', 'Smith')
#     login_userID = auth_login_v1('joe123@gmail.com', 'password')
#     assert register_userID == login_userID

# def test_registered_email_2():
#     requests.delete(f'{BASE_URL}/clear/v1')
#     register_userID = auth_register_v1('marryjoe222@gmail.com', 'passwordM', 'Marry', 'Joe')
#     login_userID = auth_login_v1('marryjoe222@gmail.com', 'passwordM')
#     assert register_userID == login_userID

# def test_registered_email_3():
#     requests.delete(f'{BASE_URL}/clear/v1')
#     register_userID = auth_register_v1('davidmo@gmail.com', 'passwordD', 'David', 'Mo')
#     login_userID = auth_login_v1('davidmo@gmail.com', 'passwordD')
#     assert register_userID == login_userID

# # Tests for multiple registers
# def test_registered_email_4():
#     requests.delete(f'{BASE_URL}/clear/v1')
#     register_userID = auth_register_v1('panhain7@gmail.com', '016758899', 'Panha', 'In')
#     register_userID = auth_register_v1('oudomiscool@gmail.com', 'potatoyum', 'Oudom', 'Lim')
#     login_userID = auth_login_v1('oudomiscool@gmail.com', 'potatoyum')
#     assert register_userID == login_userID

# # Testing for unmatched password
# def test_wrong_password():
#     requests.delete(f'{BASE_URL}/clear/v1')
#     with pytest.raises(InputError):
#         auth_login_v1('joe123@gmail.com', 'cotton')

# def test_wrong_password_2():
#     requests.delete(f'{BASE_URL}/clear/v1')
#     with pytest.raises(InputError):
#         auth_login_v1('marryjoe222@gmail.com', 'eyed')

# def test_wrong_password_3():
#     requests.delete(f'{BASE_URL}/clear/v1')
#     with pytest.raises(InputError):
#         auth_login_v1('davidmo@gmail.com', 'joe')
