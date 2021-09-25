import pytest

from src.auth import auth_login_v1, auth_register_v1
from src.error import InputError
from src.data_store import clear_v1

# Test Invalid Emails
# --------------------------
# The user should not be able to log in if they use an invalid email
# Dom remove the hashtags to test your auth_login_v1 function - Ridho
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

# Test Valid Emails
# --------------------------
# The user should be able to log in if they use a valid email
# Dom remove the hashtags to test your auth_login_v1 function - Ridho
def test_register_valid_email():
    clear_v1()
    register_userID = auth_register_v1('joe123@gmail.com', 'password', 'Joe', 'Smith')
    #login_userID = auth_login_v1('joe123@gmail.com', 'password')
    #assert register_userID = login_userID

def test_register_valid_email_2():
    clear_v1()
    register_userID = auth_register_v1('marryjoe222@gmail.com', 'passwordM', 'Marry', 'Joe')
    #login_userID = auth_login_v1('marryjoe222@gmail.com', 'passwordM')
    #assert register_userID = login_userID


def test_register_valid_email_3():
    clear_v1()
    register_userID = auth_register_v1('davidmo@gmail.com', 'passwordD', 'David', 'Mo')
    #login_userID = auth_login_v1('joe123@gmail.com', 'passwordD')
    #assert register_userID = login_userID


# Test Duplicate Emails
def test_register_duplicate_email():
    auth_register_v1('joe123@gmail.com', 'password', 'Joe', 'Smith')
    with pytest.raises(InputError):
        auth_register_v1('joe123@gmail.com', 'password2', 'Joe2', 'Smith2')
