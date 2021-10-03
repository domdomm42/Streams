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
user Marry (channel 1, 2, 3) and a public channel for user Joe (channel 0, 1, 3).  
'''

@pytest.fixture
def setup():
    clear_v1()

    login_joe = auth_register_v1('joe123@gmail.com', 'password', 'Joe', 'Smith')
    channel_joe = channels_create_v1(login_joe, 'Joe', False).get('channel_id')

    login_marry = auth_register_v1('marryjoe222@gmail.com', 'passwordM', 'Marry', 'Joe')
    channel_marry = channels_create_v1(login_marry, 'Marry', True).get('channel_id')

    channel_second_marry = channels_create_v1(login_marry, 'Second_Marry', False).get('channel_id')
    channel_join_v1(login_joe, channel_marry)

    channel_second_joe = channels_create_v1(login_joe, 'Second_Joe', True).get('channel_id')
    channel_join_v1(login_marry, channel_second_joe)

    login_sam = auth_register_v1('sam123@gmail.com', 'passwordJ', 'Sam', 'Smith')
    channels_create_v1(login_sam, 'Sam', True).get('channel_id')
    
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
            },
            {
                'channel_id': 3,
        		'name': 'Second_Joe'
            },
            {
                'channel_id': 4,
        		'name': 'Sam'
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
            },
            {
                'channel_id': 3,
        		'name': 'Second_Joe'
            }
        ]
    }


# Testing Invalid names for channel creation
def test_empty_name1():
    with pytest.raises(InputError):
        channels_create_v1(1, '', True)

def test_long_name1():
    with pytest.raises(InputError):
        channels_create_v1(1, 'bigbigbigbigbigbigbigbig', True)

def test_empty_name2():
    with pytest.raises(InputError):
        channels_create_v1(1, '', False)

def test_long_name2():
    with pytest.raises(InputError):
        channels_create_v1(1, 'bigbigbigbigbigbigbigbig', False)

# Testing simple channel creation
def test_new_channel():
    clear_v1()
    assert channels_create_v1(0, 'Joe', True).get('channel_id') == 0
    assert channels_create_v1(1, 'Marry', True).get('channel_id') == 1
    assert channels_create_v1(0, 'Joeseph', True).get('channel_id') == 2

        

