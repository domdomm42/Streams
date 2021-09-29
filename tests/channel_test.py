import pytest

from src.other import clear_v1
from src.error import InputError
from src.auth import auth_login_v1, auth_register_v1
from src.channels import channels_list_v1, channels_listall_v1, channels_create_v1
from src.channel import channel_join_v1

''' 
Channels testing documentation
Setup creates the background for each channel list test by registering,
logging, and creating a channel for each user. A private channel for 
user Marry (channel 1) and a public channel for user Joe (channel 0 and 1).  
'''

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
    assert channels_create_v1(0, 'Joe', True) == 0
    assert channels_create_v1(1, 'Marry', True) == 1
    assert channels_create_v1(0, 'Joeseph', True) == 2
    
        
