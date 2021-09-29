import pytest
from src.channel import channel_invite_v1, channel_message_v1
from src.error import InputError, AccessError
from src.auth import auth_login_v1, auth_register_v1
from src.channels import channels_list_v1, channels_listall_v1, channels_create_v1
from src.other import clear_v1

@pytest.fixture
def set_up():
    clear_v1()
    register_user_id = auth_register_v1('abc1531@gmail.com', 'password', 'abc', '123')
    login_abc = auth_login_v1('abc1531@gmail.com', 'password')
    channels_abc = channels_create_v1(login_abc, 'abc', True)
    # create user Luka with private channel
    register_user_id = auth_register_v1('asd1531@gmail.com', 'passwordM', 'asd', '456')
    login_asd = auth_login_v1('asd1531@gmail.com', 'passwordM')
    channels_asd = channels_create_v1(login_asd, 'asd', False)
    return login_abc, login_asd, channels_abc, channels_asd



# InputError

# Test invalid channel_id
def test_invalid_channel_id_invite():
    with pytest.raises(InputError):
        channel_invite_v1(8,8)

def test_invalid_channel_id_message():
    with pytest.raises(InputError):
        channel_messages_v1(8,8)


# Test invalid u_id
def test_invalid_u_id_invite():
    with pytest.raises(InputError):
        channel_invite_v1(8,8)


# Test already member
def test_repeated_invite():
    channel_invite_v1(8,8)
    with pytest.raises(InputError):
        channel_invite_v1(8,8)


# Test start
def test_start_message():
    with pytest.raises(InputError):
        channel_messages_v1(8,88)




# AccessError

# Test authorised
def test_authorised_invite(set_up):
    with pytest.raises(AccessError):
        channel_invite_v1(login_abc, channels_asd)


def test_authorised_message(set_up):
    with pytest.raises(AccessError):
        channel_messages_v1(login_abc, channels_asd)
