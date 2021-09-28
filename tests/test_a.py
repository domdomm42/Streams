import pytest
from src.channel import channel_invite_v1, channel_messages_v1
from src.error import InputError
from src.other import clear_v1


# InputError

# Test invalid channel_id
def test_invalid_channel_id_invite():
    with pytest.raises(InputError):
        channel_invite_v1('a', 'a')


def test_invalid_channel_id_message():
    with pytest.raises(InputError):
        channel_messages_v1('b', 'b')


# Test invalid u_id
def test_invalid_u_id_invite():
    with pytest.raises(InputError):
        channel_invite_v1('a', 'a')


# Test already member
def test_repeated_invite():
    channel_invite_v1('a', 'a')
    with pytest.raises(InputError):
        channel_invite_v1('a', 'a')


# Test start
def test_start_message():
    with pytest.raises(InputError):
        channel_messages_v1('1', '2')




# AccessError

# Test authorised
def test_authorised_invite():
    with pytest.raises(AccessError):
        channel_invite_v1('A', 'a')


def test_authorised_message():
    with pytest.raises(AccessError):
        channel_messages_v1('B', 'b')
