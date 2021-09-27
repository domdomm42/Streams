import pytest

from src.other import clear_v1
from src.channels import channels_list_v1, channels_listall_v1

''' 
Channels testing documentation
Setup creates the background for each channel list test by registering,
logging, and creating a channel for each user. A private channel for 
user Marry (channel 1) and a public channel for user Joe (channel 0 and 1).  
'''

@pytest.fixture
def setup():
    clear_v1()
    register_userID = auth_register_v1('joe123@gmail.com', 'password', 'Joe', 'Smith')
    login_joe = auth_login_v1('joe123@gmail.com', 'password')
    channel_joe = channels_create_v1(login_userID, 'Joe', False)
    register_userID = auth_register_v1('marryjoe222@gmail.com', 'passwordM', 'Marry', 'Joe')
    login_marry = auth_login_v1('marryjoe222@gmail.com', 'passwordM')
    channel_marry = channels_create_v1(login_userID, 'Marry', True)
    channel_join_v1(login_joe, channel_marry)
    return login_marry

# Simple Listing tests to return all channels created
def test_all_channels(setup):
    assert channels_list_v1(setup) == {
        'channels': [
        	{
        		'channel_id': 0,
        		'name': 'Joe',
        	},
            {
                'channel_id': 1,
                'name': 'Marry'
            }
        ],
    }

# Simple listing tests to return all channels that the given id is a part of
def test_given_channels(setup):
     assert channels_list_v1(setup) == {
        'channels': [
        	{
        		'channel_id': 2,
        		'name': 'Marry',
        	}
        ],
     }     

