import pytest

from src.auth import auth_login_v1, auth_register_v1
from src.error import InputError
from src.other import clear_v1

# Test invalid emails
def test_register_invalid_email():
    with pytest.raises(InputError):
        auth_register_v1('joe123.com', 'password', 'Joe', 'Smith')

def test_register_invalid_email_2():
    with pytest.raises(InputError):
        auth_register_v1('anika.com', 'password', 'Joe', 'Smith')

def test_register_invalid_email_3():
    with pytest.raises(InputError):
        auth_register_v1(' ', 'password', 'Joe', 'Smith')

def test_register_invalid_email_4():
    with pytest.raises(InputError):
        auth_register_v1('.com', 'password', 'Joe', 'Smith')

def test_register_invalid_email_5():
    with pytest.raises(InputError):
        auth_register_v1('@.com', 'password', 'Joe', 'Smith')

def test_register_invalid_email_6():
    with pytest.raises(InputError):
        auth_register_v1('2342ras@43', 'password', 'Joe', 'Smith')

def test_register_invalid_email_7():
    with pytest.raises(InputError):
        auth_register_v1('dklshfdoshfokishjfoihwokjbhfd', 'password', 'Joe', 'Smith')

def test_register_invalid_email_8():
    with pytest.raises(InputError):
        auth_register_v1('marry.joe!@gmail.com', 'password', 'Joe', 'Smith')

# Test valid emails
def test_register_valid_email():
    clear_v1()
    auth_register_v1('joe123@gmail.com', 'password', 'Joe', 'Smith')

def test_register_valid_email_2():
    clear_v1()
    auth_register_v1('marryjoe222@gmail.com', 'passwordM', 'Marry', 'Joe')

def test_register_valid_email_3():
    clear_v1()
    auth_register_v1('davidmo@gmail.com', 'passwordD', 'David', 'Mo')

# Test duplicate emails
def test_register_duplicate_email():
    clear_v1()
    auth_register_v1('joe123@gmail.com', 'password', 'Joe', 'Smith')
    with pytest.raises(InputError):
        auth_register_v1('joe123@gmail.com', 'password2', 'Joe2', 'Smith2')

# Test invalid password (<6 characters)
def test_invalid_password():
    clear_v1()
    with pytest.raises(InputError):
        auth_register_v1('joe123@gmail.com', 'joe', 'Joe', 'Smith')

def test_invalid_password_2():
    clear_v1()
    with pytest.raises(InputError):
        auth_register_v1('joe123@gmail.com', '123', 'Joe', 'Smith')

def test_invalid_password_3():
    clear_v1()
    with pytest.raises(InputError):
        auth_register_v1('joe123@gmail.com', ' ', 'Joe', 'Smith')

def test_invalid_password_4():
    clear_v1()
    with pytest.raises(InputError):
        auth_register_v1('joe123@gmail.com', '', 'Joe', 'Smith')

# Test invalid first name (not 1 <= characters <= 50)
def test_invalid_first_name():
    clear_v1()
    with pytest.raises(InputError):
        auth_register_v1('joe123@gmail.com', 'password', '', 'Smith')

def test_invalid_first_name_2():
    clear_v1()
    with pytest.raises(InputError):
        auth_register_v1('joe123@gmail.com', 'password', 'J'*51, 'Smith')

# Test invalid last name (not 1 <= characters <= 50)
def test_invalid_last_name():
    clear_v1()
    with pytest.raises(InputError):
        auth_register_v1('joe123@gmail.com', 'password', 'Joe', '')

def test_invalid_last_name_2():
    clear_v1()
    with pytest.raises(InputError):
        auth_register_v1('joe123@gmail.com', 'password', 'Joe', 'S'*51)

# Test unregistered email 
def test_unregistered_email():
    clear_v1()
    with pytest.raises(InputError):
        auth_login_v1('joe123.com', 'password')

def test_unregistered_email_2():
    clear_v1()
    with pytest.raises(InputError):
        auth_login_v1('anika.com', 'password')

def test_unregistered_email_3():
    clear_v1()
    with pytest.raises(InputError):
        auth_login_v1(' ', 'password')

def test_unregisterd_email_4():
    clear_v1()
    with pytest.raises(InputError):
        auth_login_v1('.com', 'password')

def test_unregistered_email_5():
    clear_v1()
    with pytest.raises(InputError):
        auth_login_v1('@.com', 'password')

def test_unregisted_email_6():
    clear_v1()
    with pytest.raises(InputError):
        auth_login_v1('2342ras@43', 'password')

def test_unregisted_email_7():
    clear_v1()
    with pytest.raises(InputError):
        auth_login_v1('dklshfdoshfokishjfoihwokjbhfd', 'password')

def test_unregistered_email_8():
    clear_v1()
    with pytest.raises(InputError):
        auth_login_v1('marry.joe!@gmail.com', 'password')

def test_unregistered_email_9():
    clear_v1()
    with pytest.raises(InputError):
        auth_login_v1('wolffangdan', 'dancarry')

# Test registered email
def test_registered_email():
    clear_v1()
    register_userID = auth_register_v1('joe123@gmail.com', 'password', 'Joe', 'Smith')
    login_userID = auth_login_v1('joe123@gmail.com', 'password')
    assert register_userID == login_userID

def test_registered_email_2():
    clear_v1()
    register_userID = auth_register_v1('marryjoe222@gmail.com', 'passwordM', 'Marry', 'Joe')
    login_userID = auth_login_v1('marryjoe222@gmail.com', 'passwordM')
    assert register_userID == login_userID

def test_registered_email_3():
    clear_v1()
    register_userID = auth_register_v1('davidmo@gmail.com', 'passwordD', 'David', 'Mo')
    login_userID = auth_login_v1('davidmo@gmail.com', 'passwordD')
    assert register_userID == login_userID

# Tests for multiple registers
def test_registered_email_4():
    clear_v1()
    register_userID = auth_register_v1('panhain7@gmail.com', '016758899', 'Panha', 'In')
    register_userID = auth_register_v1('oudomiscool@gmail.com', 'potatoyum', 'Oudom', 'Lim')
    login_userID = auth_login_v1('oudomiscool@gmail.com', 'potatoyum')
    assert register_userID == login_userID

# Testing for unmatched password
def test_wrong_password():
    clear_v1()
    with pytest.raises(InputError):
        auth_login_v1('joe123@gmail.com', 'cotton')

def test_wrong_password_2():
    clear_v1()
    with pytest.raises(InputError):
        auth_login_v1('marryjoe222@gmail.com', 'eyed')

def test_wrong_password_3():
    clear_v1()
    with pytest.raises(InputError):
        auth_login_v1('davidmo@gmail.com', 'joe')
