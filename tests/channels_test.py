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
user Marry (channel 1) and a public channel for user Joe (channel 0 and 1).  
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
            }
        ]
    }

# Simple listing tests to return all channels that the given id is a part of
def test_given_channels(setup):
     assert channels_list_v1(setup) == {
        'channels': [
        	{
        		'channel_id': 1,
        		'name': 'Marry',
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
    assert channels_create_v1(0, 'Joe', True) == 0
    assert channels_create_v1(1, 'Marry', True) == 1
    assert channels_create_v1(0, 'Joeseph', True) == 2

def test_invalid_channel_id_detail():
    with pytest.raises(InputError):
        channel_details_v1(1, 100)


        
def test_invalid_channel_id_join():
    with pytest.raises(InputError):
        channel_join_v1(1, 100)




#=====Test member join again===========

def test_member_join_again_1():
        #create a channel and auth_user
    clear_v1()
    register_user_id = auth_register_v1('joe123@gmail.com', 'password', 'Joe', 'Smith')
    login_joe = auth_login_v1('joe123@gmail.com', 'password')
    channels_joe = channels_create_v1(login_joe, 'Joe', True)
                
    with pytest.raises(InputError):
        channel_join_v1(login_joe, channels_joe)

def test_member_join_again_2():
    clear_v1()
    register_user_id = auth_register_v1('marryjoe222@gmail.com', 'passwordM', 'Marry', 'Joe')
    login_marry = auth_login_v1('marryjoe222@gmail.com', 'passwordM')
    channels_marry = channels_create_v1(login_marry, 'Marry', False)
    with pytest.raises(InputError):
        channel_join_v1(login_marry, channels_marry)


#=====Access Error=====================
#=====Auth_user is not member==========
#User is not allow to access channel details
def test_no_member_access_detail_1():
        #create channel and auth_user
    clear_v1()
    register_user_id = auth_register_v1('joe123@gmail.com', 'password', 'Joe', 'Smith')
    login_joe = auth_login_v1('joe123@gmail.com', 'password')
    channels_joe = channels_create_v1(login_joe, 'Joe', True)
    
    
    register_user_id = auth_register_v1('marryjoe222@gmail.com', 'passwordM', 'Marry', 'Joe')
    login_marry = auth_login_v1('marryjoe222@gmail.com', 'passwordM')
    channels_marry = channels_create_v1(login_marry, 'Marry', False)
    with pytest.raises(AccessError):
        channel_details_v1(login_joe, channels_marry)



def test_no_member_access_detail_2():
        #create channel and auth_user
    clear_v1()
    register_user_id = auth_register_v1('joe123@gmail.com', 'password', 'Joe', 'Smith')
    login_joe = auth_login_v1('joe123@gmail.com', 'password')
    channels_joe = channels_create_v1(login_joe, 'Joe', True)
    
    
    register_user_id = auth_register_v1('marryjoe222@gmail.com', 'passwordM', 'Marry', 'Joe')
    login_marry = auth_login_v1('marryjoe222@gmail.com', 'passwordM')
    channels_marry = channels_create_v1(login_marry, 'Marry', False)
    with pytest.raises(AccessError):
        channel_details_v1(login_marry, channels_joe)
#=====Channel is private===============
#User is not a globle owner or member

def test_join_private_channel():
    clear_v1()
    register_user_id = auth_register_v1('joe123@gmail.com', 'password', 'Joe', 'Smith')
    login_joe = auth_login_v1('joe123@gmail.com', 'password')
    channels_joe = channels_create_v1(login_joe, 'Joe', True)
    
    register_user_id = auth_register_v1('marryjoe222@gmail.com', 'passwordM', 'Marry', 'Joe')
    login_marry = auth_login_v1('marryjoe222@gmail.com', 'passwordM')
    channels_marry = channels_create_v1(login_marry, 'Marry', False)
    with pytest.raises(AccessError):
        channel_join_v1(login_joe, channels_marry)


#=====Valid case for detail===========
def test_valid_channel_id_detail_1():
    clear_v1()
    register_user_id = auth_register_v1('joe123@gmail.com', 'password', 'Joe', 'Smith')
    login_joe = auth_login_v1('joe123@gmail.com', 'password')
    channels_joe = channels_create_v1(login_joe, 'Joe', True)
    
    
    details = channel_details_v1(login_joe, channels_joe)
    
    assert details == {
        'name': 'Joe', 
        'is_public': True, 
        'owner_members': [
            {
                'u_id': login_joe, 
                'email': 'joe123@gmail.com', 
                'name_first': 'Joe', 
                'name_last': 'Smith', 
                'handle_str': 'joesmith'
            }
        ], 
        'all_members': [
            {
                'u_id': login_joe, 
                'email': 'joe123@gmail.com', 
                'name_first': 'Joe', 
                'name_last': 'Smith', 
                'handle_str': 'joesmith'
            }
        ]
    }

def test_valid_channel_id_detail_2():
    clear_v1()
    register_user_id = auth_register_v1('marryjoe222@gmail.com', 'passwordM', 'Marry', 'Joe')
    login_marry = auth_login_v1('marryjoe222@gmail.com', 'passwordM')
    channels_marry = channels_create_v1(login_marry, 'Marry', False)
    
    
    details = channel_details_v1(login_marry, channels_marry)
    
    assert details == {
        'name': 'Marry', 
        'is_public': False, 
        'owner_members': [
            {
                'u_id': login_marry, 
                'email': 'marryjoe222@gmail.com', 
                'name_first': 'Marry', 
                'name_last': 'Joe', 
                'handle_str': 'marryjoe'
            }
        ], 
        'all_members': [
            {
                'u_id': login_marry, 
                'email': 'marryjoe222@gmail.com', 
                'name_first': 'Marry', 
                'name_last': 'Joe', 
                'handle_str': 'marryjoe'
            }
        ]
    }

#=====Valid case for join==============

def test_valid_channel_id_join():
    
    clear_v1()
    register_user_id = auth_register_v1('joe123@gmail.com', 'password', 'Joe', 'Smith')
    login_joe = auth_login_v1('joe123@gmail.com', 'password')
    channels_joe = channels_create_v1(login_joe, 'Joe', True)
    
    register_user_id = auth_register_v1('marryjoe222@gmail.com', 'passwordM', 'Marry', 'Joe')
    login_marry = auth_login_v1('marryjoe222@gmail.com', 'passwordM')
    channels_marry = channels_create_v1(login_marry, 'Marry', False)
    channel_join_v1(login_marry, channels_joe)
    details = channel_details_v1(login_marry, channels_joe)
    
    assert details == {
        'name': 'Joe',
        'is_public': True,
        'owner_members': [
            {
                'u_id': login_joe, 
                'email': 'joe123@gmail.com', 
                'name_first': 'Joe', 
                'name_last': 'Smith', 
                'handle_str': 'joesmith'
            }
        ], 
        'all_members': [
            {
                'u_id': login_joe, 
                'email': 'joe123@gmail.com', 
                'name_first': 'Joe', 
                'name_last': 'Smith', 
                'handle_str': 'joesmith'
            }, 
            {   'u_id': login_marry, 
                'email': 'marryjoe222@gmail.com', 
                'name_first': 'Marry', 
                'name_last': 'Joe', 
                'handle_str': 'marryjoe'
            }
        ]
    }


