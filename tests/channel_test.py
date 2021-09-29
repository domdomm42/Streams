import pytest
from src.channel import channel_details_v1, channel_join_v1
from src.error import InputError, AccessError
from src.auth import auth_login_v1, auth_register_v1
from src.channels import channels_list_v1, channels_listall_v1, channels_create_v1
from src.other import clear_v1

#=====Input Error======================
#=====Test invalid channel_id==========



@pytest.fixture
def set_up():
    clear_v1()
    register_user_id = auth_register_v1('joe123@gmail.com', 'password', 'Joe', 'Smith')
    login_joe = auth_login_v1('joe123@gmail.com', 'password')
    channels_joe = channels_create_v1(login_joe, 'Joe', True)
    #create user Luka with private channel
    register_user_id = auth_register_v1('marryjoe222@gmail.com', 'passwordM', 'Marry', 'Joe')
    login_marry = auth_login_v1('marryjoe222@gmail.com', 'passwordM')
    channels_marry = channels_create_v1(login_marry, 'Marry', False)
    return login_joe, login_marry, channels_joe, channels_marry
    



def test_invalid_channel_id_detail():
    with pytest.raises(InputError):
        channel_details_v1(1, 100)
#   with pytest.raises(InputError)
#       channel_join_v1(1, 100)




#=====Test member join again===========

def test_member_join_again():
        #create a channel and auth_user
    clear_v1()
    register_user_id = auth_register_v1('joe123@gmail.com', 'password', 'Joe', 'Smith')
    login_joe = auth_login_v1('joe123@gmail.com', 'password')
    channels_joe = channels_create_v1(login_joe, 'Joe', True)
                
    with pytest.raises(InputError):
        channel_join_v1(login_joe, channels_joe)

#=====Access Error=====================
#=====Auth_user is not member==========
#User is not allow to access channel details
def test_no_member_access_detail():
        #create channel and auth_user
    clear_v1()
    register_user_id = auth_register_v1('joe123@gmail.com', 'password', 'Joe', 'Smith')
    login_joe = auth_login_v1('joe123@gmail.com', 'password')
    channels_joe = channels_create_v1(login_joe, 'Joe', True)
    #create user Luka with private channel
    register_user_id = auth_register_v1('marryjoe222@gmail.com', 'passwordM', 'Marry', 'Joe')
    login_marry = auth_login_v1('marryjoe222@gmail.com', 'passwordM')
    channels_marry = channels_create_v1(login_marry, 'Marry', False)
    with pytest.raises(AccessError):
        channel_details_v1(login_joe, channels_marry)

#=====Channel is private===============
#User is not a globle owner or member

def test_join_private_channel():
    clear_v1()
    register_user_id = auth_register_v1('joe123@gmail.com', 'password', 'Joe', 'Smith')
    login_joe = auth_login_v1('joe123@gmail.com', 'password')
    channels_joe = channels_create_v1(login_joe, 'Joe', True)
    #create user Luka with private channel
    register_user_id = auth_register_v1('marryjoe222@gmail.com', 'passwordM', 'Marry', 'Joe')
    login_marry = auth_login_v1('marryjoe222@gmail.com', 'passwordM')
    channels_marry = channels_create_v1(login_marry, 'Marry', False)
    with pytest.raises(AccessError):
        channel_join_v1(login_joe, channels_marry)


#=====Valid case for detail===========
def test_valid_channel_id_detail():
    clear_v1()
    register_user_id = auth_register_v1('joe123@gmail.com', 'password', 'Joe', 'Smith')
    login_joe = auth_login_v1('joe123@gmail.com', 'password')
    channels_joe = channels_create_v1(login_joe, 'Joe', True)
    
    
    details = channel_details_v1(login_joe, channels_joe)
    assert details['name'] == 'Joe'

#=====Valid case for join==============

def test_valid_channel_id_join():
    
    clear_v1()
    register_user_id = auth_register_v1('joe123@gmail.com', 'password', 'Joe', 'Smith')
    login_joe = auth_login_v1('joe123@gmail.com', 'password')
    channels_joe = channels_create_v1(login_joe, 'Joe', True)
    #create user Luka with private channel
    register_user_id = auth_register_v1('marryjoe222@gmail.com', 'passwordM', 'Marry', 'Joe')
    login_marry = auth_login_v1('marryjoe222@gmail.com', 'passwordM')
    channels_marry = channels_create_v1(login_marry, 'Marry', False)
    channel_join_v1(login_joe, channels_marry)
    details = channel_details_v1(login_marry, channels_joe)
    assert len(details['all_members']) == 2

