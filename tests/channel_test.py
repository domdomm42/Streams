import pytest
from src.channel import channel_invite_v1, channel_messages_v1
from src.channels import channels_create_v1
from src.error import InputError, AccessError
from src.auth import auth_login_v1, auth_register_v1
from src.other import clear_v1

@pytest.fixture
def set_up():
    clear_v1()
    register_user_id = auth_register_v1('abc1531@gmail.com', 'password', 'abc', '123')
    login_abc = auth_login_v1('abc1531@gmail.com', 'password')
    channels_abc = channels_create_v1(login_abc, 'abc', True)
    register_user_id = auth_register_v1('asd1531@gmail.com', 'passwordM', 'asd', '456')
    login_asd = auth_login_v1('asd1531@gmail.com', 'passwordM')
    channels_asd = channels_create_v1(login_asd, 'asd', False)
    return login_abc, login_asd, channels_abc, channels_asd



# InputError

# Test invalid channel_id
def test_invalid_channel_id_invite():
    clear_v1()
    register_user_id = auth_register_v1('abc1531@gmail.com', 'password', 'abc', '123')
    login_abc = auth_login_v1('abc1531@gmail.com', 'password')
    channels_abc = channels_create_v1(login_abc, 'abc', True)
    register_user_id = auth_register_v1('asd1531@gmail.com', 'passwordM', 'asd', '456')
    login_asd = auth_login_v1('asd1531@gmail.com', 'passwordM')
    channels_asd = channels_create_v1(login_asd, 'asd', False)
    with pytest.raises(InputError):
        channel_invite_v1(login_abc, channels_abc, login_asd)

def test_invalid_channel_id_message():
    
    clear_v1()
    register_user_id = auth_register_v1('abc1531@gmail.com', 'password', 'abc', '123')
    login_abc = auth_login_v1('abc1531@gmail.com', 'password')
    channels_abc = channels_create_v1(login_abc, 'abc', True)
    register_user_id = auth_register_v1('asd1531@gmail.com', 'passwordM', 'asd', '456')
    login_asd = auth_login_v1('asd1531@gmail.com', 'passwordM')
    channels_asd = channels_create_v1(login_asd, 'asd', False)
    start = 0
    
    with pytest.raises(InputError):
        channel_messages_v1(login_abc,999, start)


# Test invalid u_id
def test_invalid_u_id_invite():
    
    clear_v1()
    register_user_id = auth_register_v1('abc1531@gmail.com', 'password', 'abc', '123')
    login_abc = auth_login_v1('abc1531@gmail.com', 'password')
    channels_abc = channels_create_v1(login_abc, 'abc', True)
    register_user_id = auth_register_v1('asd1531@gmail.com', 'passwordM', 'asd', '456')
    login_asd = auth_login_v1('asd1531@gmail.com', 'passwordM')
    channels_asd = channels_create_v1(login_asd, 'asd', False)

    with pytest.raises(InputError):
        channel_invite_v1(login_abc, channels_abc, 999)


# Test already member
def test_repeated_invite():
    
    clear_v1()
    register_user_id = auth_register_v1('abc1531@gmail.com', 'password', 'abc', '123')
    login_abc = auth_login_v1('abc1531@gmail.com', 'password')
    channels_abc = channels_create_v1(login_abc, 'abc', True)
    register_user_id = auth_register_v1('asd1531@gmail.com', 'passwordM', 'asd', '456')
    login_asd = auth_login_v1('asd1531@gmail.com', 'passwordM')
    channels_asd = channels_create_v1(login_asd, 'asd', False)
    
    #channel_invite_v1(login_abc, channels_abc, login_asd)
    with pytest.raises(InputError):
        channel_invite_v1(login_abc, channels_abc, login_abc)


# Test start
def test_start_message():
    
    clear_v1()
    register_user_id = auth_register_v1('abc1531@gmail.com', 'password', 'abc', '123')
    login_abc = auth_login_v1('abc1531@gmail.com', 'password')
    channels_abc = channels_create_v1(login_abc, 'abc', True)
    register_user_id = auth_register_v1('asd1531@gmail.com', 'passwordM', 'asd', '456')
    login_asd = auth_login_v1('asd1531@gmail.com', 'passwordM')
    channels_asd = channels_create_v1(login_asd, 'asd', False)


    with pytest.raises(AccessError):
        channel_messages_v1(login_abc, channels_abc, 999)


# AccessError

# Test authorised
def test_authorised_invite():
    
    clear_v1()
    register_user_id = auth_register_v1('abc1531@gmail.com', 'password', 'abc', '123')
    login_abc = auth_login_v1('abc1531@gmail.com', 'password')
    channels_abc = channels_create_v1(login_abc, 'abc', True)
    register_user_id = auth_register_v1('asd1531@gmail.com', 'passwordM', 'asd', '456')
    login_asd = auth_login_v1('asd1531@gmail.com', 'passwordM')
    channels_asd = channels_create_v1(login_asd, 'asd', False)
    start = 0

    with pytest.raises(AccessError):
        channel_invite_v1(login_asd, channels_abc, login_asd)


def test_authorised_message():
    
    clear_v1()
    register_user_id = auth_register_v1('abc1531@gmail.com', 'password', 'abc', '123')
    login_abc = auth_login_v1('abc1531@gmail.com', 'password')
    channels_abc = channels_create_v1(login_abc, 'abc', True)
    register_user_id = auth_register_v1('asd1531@gmail.com', 'passwordM', 'asd', '456')
    login_asd = auth_login_v1('asd1531@gmail.com', 'passwordM')
    channels_asd = channels_create_v1(login_asd, 'asd', False)
    start = 0

    with pytest.raises(AccessError):
        channel_messages_v1(login_asd, channels_abc, start)
