import pytest
from src.channel import channel_details_v1, channel_join_v1
from src.error import InputError
from src.other import clear_v1

#=====Input Error======================
#=====Test invalid channel_id==========

def test_invalid_channel_id()
    with pytest.raises(InputError)
        channel_details_v1('1', '-1')
#   with pytest.raises(InputError)
#       channel_join_v1('1', '-1')




#=====Test member join again===========

def test_member_join_again()
        #create a channel and auth_user
        channel_join_v1('1', '1')          
    with pytest.raises(InputError)
        channel_join_v1('1', '1')

#=====Access Error=====================
#=====Auth_user is not member==========
#User is not allow to access channel details
def test_no_member_access_detail()
        #create channel and auth_user
    with pytest.raises(InputError)
        channel_details_v1('2', '1')

#=====Channel is private===============
#User is not a globle owner or member

def test_private_channel()
        #create a private channel and auth_user
    with pytest.raises(InputError)
        channel_join_v1('1', '2')
