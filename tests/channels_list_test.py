import pytest

from src.other import clear_v1
from src.error import InputError, AccessError
from src.auth import auth_login_v1, auth_register_v1
from src.channels import channels_list_v1, channels_listall_v1, channels_create_v1
from src.channel import channel_join_v1, channel_messages_v1, channel_join_v1, channel_details_v1

''' 
Channels testing documentation
Setup creates the background for each channel list test by registering,
logging, and creating a channel for each user. A private channel for 
user Marry (channel 1 and 2) and a public channel for user Joe (channel 0 and 1).  
'''

@pytest.fixture
def setup():
    clear_v1()
    register_userID = auth_register_v1('joe123@gmail.com', 'password', 'Joe', 'Smith')
    login_joe = auth_login_v1('joe123@gmail.com', 'password')
    channel_joe = channels_create_v1(login_joe, 'Joe', False)
    register_userID = auth_register_v1('marryjoe222@gmail.com', 'passwordM', 'Marry', 'Joe')
    login_marry = auth_login_v1('marryjoe222@gmail.com', 'passwordM')
    channel_marry = channels_create_v1(login_marry, 'Marry', True)
    channel_second_marry = channels_create_v1(login_marry, 'Second_Marry', False)
    channel_join_v1(login_joe, channel_marry)
    return login_marry

# Simple Listing tests to return all channels created
def test_all_channels(setup):
    assert channels_listall_v1(setup) == {
        'channels': [
        	{
        		'channel_id': 0,
        		'name': 'Joe',
        	},
            {
                'channel_id': 1,
                'name': 'Marry'
            },
            {
                'channel_id': 2,
                'name': 'Second_Marry'
            }
        ]
    }

# Simple listing tests to return all channels that the given id is a part of
def test_mary_channels(setup):
     assert channels_list_v1(setup) == {
        'channels': [
        	{
        		'channel_id': 1,
        		'name': 'Marry',
        	},
            {   
                'channel_id': 2,
        		'name': 'Second_Marry',
            }

        ]
    }


# Testing Invalid names for channel creation
def test_empty_name():
    with pytest.raises(InputError):
        channels_create_v1(1, '', True)

def test_long_name():
    with pytest.raises(InputError):
        channels_create_v1(1, 'bigbigbigbigbigbigbigbig', True)

def test_empty_name():
    with pytest.raises(InputError):
        channels_create_v1(1, '', False)

def test_long_name():
    with pytest.raises(InputError):
        channels_create_v1(1, 'bigbigbigbigbigbigbigbig', False)

# Testing simple channel creation
def test_new_channel():
    clear_v1()
    assert channels_create_v1(0, 'Joe', True).get('channel_id') == 0
    assert channels_create_v1(1, 'Marry', True).get('channel_id') == 1
    assert channels_create_v1(0, 'Joeseph', True).get('channel_id') == 2
