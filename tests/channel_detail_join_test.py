# import pytest
# from src.channel import channel_details_v1, channel_join_v1
# from src.error import InputError, AccessError
# from src.auth import auth_login_v1, auth_register_v1
# from src.channels import channels_list_v1, channels_listall_v1, channels_create_v1
# from src.other import clear_v1

# #=====Input Error======================
# #=====Test invalid channel_id==========




    



# def test_invalid_channel_id_detail():
#     with pytest.raises(InputError):
#         channel_details_v1(1, 100)


        
# def test_invalid_channel_id_join():
#     with pytest.raises(InputError):
#         channel_join_v1(1, 100)




# #=====Test member join again===========

# def test_member_join_again_1():
#         #create a channel and auth_user
#     clear_v1()
#     auth_register_v1('joe123@gmail.com', 'password', 'Joe', 'Smith').get('auth_user_id')
#     login_joe = auth_login_v1('joe123@gmail.com', 'password').get('auth_user_id')
#     channels_joe = channels_create_v1(login_joe, 'Joe', True).get('channel_id')
                
#     with pytest.raises(InputError):
#         channel_join_v1(login_joe, channels_joe)

# def test_member_join_again_2():
#     clear_v1()
#     auth_register_v1('marryjoe222@gmail.com', 'passwordM', 'Marry', 'Joe').get('auth_user_id')
#     login_marry = auth_login_v1('marryjoe222@gmail.com', 'passwordM').get('auth_user_id')
#     channels_marry = channels_create_v1(login_marry, 'Marry', False).get('channel_id')
#     with pytest.raises(InputError):
#         channel_join_v1(login_marry, channels_marry)


# #=====Access Error=====================
# #=====Auth_user is not member==========
# #User is not allow to access channel details
# def test_no_member_access_detail_1():
#         #create channel and auth_user
#     clear_v1()
#     auth_register_v1('joe123@gmail.com', 'password', 'Joe', 'Smith').get('auth_user_id')
#     login_joe = auth_login_v1('joe123@gmail.com', 'password').get('auth_user_id')
#     channels_create_v1(login_joe, 'Joe', True).get('channel_id')
    
    
#     auth_register_v1('marryjoe222@gmail.com', 'passwordM', 'Marry', 'Joe').get('auth_user_id')
#     login_marry = auth_login_v1('marryjoe222@gmail.com', 'passwordM').get('auth_user_id')
#     channels_marry = channels_create_v1(login_marry, 'Marry', False).get('channel_id')
#     with pytest.raises(AccessError):
#         channel_details_v1(login_joe, channels_marry)



# def test_no_member_access_detail_2():
#         #create channel and auth_user
#     clear_v1()
#     auth_register_v1('joe123@gmail.com', 'password', 'Joe', 'Smith').get('auth_user_id')
#     login_joe = auth_login_v1('joe123@gmail.com', 'password').get('auth_user_id')
#     channels_joe = channels_create_v1(login_joe, 'Joe', True).get('channel_id')
    
    
#     auth_register_v1('marryjoe222@gmail.com', 'passwordM', 'Marry', 'Joe').get('auth_user_id')
#     login_marry = auth_login_v1('marryjoe222@gmail.com', 'passwordM').get('auth_user_id')
#     channels_create_v1(login_marry, 'Marry', False).get('channel_id')
#     with pytest.raises(AccessError):
#         channel_details_v1(login_marry, channels_joe)
# #=====Channel is private===============
# #User is not a globle owner or member

# def test_join_private_channel():
#     clear_v1()
#     auth_register_v1('joe123@gmail.com', 'password', 'Joe', 'Smith').get('auth_user_id')
#     login_joe = auth_login_v1('joe123@gmail.com', 'password').get('auth_user_id')
#     channels_create_v1(login_joe, 'Joe', True).get('channel_id')
    
#     auth_register_v1('marryjoe222@gmail.com', 'passwordM', 'Marry', 'Joe').get('auth_user_id')
#     login_marry = auth_login_v1('marryjoe222@gmail.com', 'passwordM').get('auth_user_id')
#     channels_marry = channels_create_v1(login_marry, 'Marry', False).get('channel_id')
#     with pytest.raises(AccessError):
#         channel_join_v1(login_joe, channels_marry)


# #=====Valid case for detail===========
# def test_valid_channel_id_detail_1():
#     clear_v1()
#     auth_register_v1('joe123@gmail.com', 'password', 'Joe', 'Smith').get('auth_user_id')
#     login_joe = auth_login_v1('joe123@gmail.com', 'password').get('auth_user_id')
#     channels_joe = channels_create_v1(login_joe, 'Joe', True).get('channel_id')
    
    
#     details = channel_details_v1(login_joe, channels_joe)
    
#     assert details == {
#         'name': 'Joe', 
#         'is_public': True, 
#         'owner_members': [
#             {
#                 'u_id': login_joe, 
#                 'email': 'joe123@gmail.com', 
#                 'name_first': 'Joe', 
#                 'name_last': 'Smith', 
#                 'handle_str': 'joesmith'
#             }
#         ], 
#         'all_members': [
#             {
#                 'u_id': login_joe, 
#                 'email': 'joe123@gmail.com', 
#                 'name_first': 'Joe', 
#                 'name_last': 'Smith', 
#                 'handle_str': 'joesmith'
#             }
#         ]
#     }

# def test_valid_channel_id_detail_2():
#     clear_v1()
#     auth_register_v1('marryjoe222@gmail.com', 'passwordM', 'Marry', 'Joe').get('auth_user_id')
#     login_marry = auth_login_v1('marryjoe222@gmail.com', 'passwordM').get('auth_user_id')
#     channels_marry = channels_create_v1(login_marry, 'Marry', False).get('channel_id')
    
    
#     details = channel_details_v1(login_marry, channels_marry)
    
#     assert details == {
#         'name': 'Marry', 
#         'is_public': False, 
#         'owner_members': [
#             {
#                 'u_id': login_marry, 
#                 'email': 'marryjoe222@gmail.com', 
#                 'name_first': 'Marry', 
#                 'name_last': 'Joe', 
#                 'handle_str': 'marryjoe'
#             }
#         ], 
#         'all_members': [
#             {
#                 'u_id': login_marry, 
#                 'email': 'marryjoe222@gmail.com', 
#                 'name_first': 'Marry', 
#                 'name_last': 'Joe', 
#                 'handle_str': 'marryjoe'
#             }
#         ]
#     }

# #=====Valid case for join==============

# def test_valid_channel_id_join():
    
#     clear_v1()
#     auth_register_v1('joe123@gmail.com', 'password', 'Joe', 'Smith').get('auth_user_id')
#     login_joe = auth_login_v1('joe123@gmail.com', 'password').get('auth_user_id')
#     channels_joe = channels_create_v1(login_joe, 'Joe', True).get('channel_id')
    
#     auth_register_v1('marryjoe222@gmail.com', 'passwordM', 'Marry', 'Joe').get('auth_user_id')
#     login_marry = auth_login_v1('marryjoe222@gmail.com', 'passwordM').get('auth_user_id')
#     channels_create_v1(login_marry, 'Marry', False).get('channel_id')
#     channel_join_v1(login_marry, channels_joe)
#     details = channel_details_v1(login_marry, channels_joe)
    
#     assert details == {
#         'name': 'Joe',
#         'is_public': True,
#         'owner_members': [
#             {
#                 'u_id': login_joe, 
#                 'email': 'joe123@gmail.com', 
#                 'name_first': 'Joe', 
#                 'name_last': 'Smith', 
#                 'handle_str': 'joesmith'
#             }
#         ], 
#         'all_members': [
#             {
#                 'u_id': login_joe, 
#                 'email': 'joe123@gmail.com', 
#                 'name_first': 'Joe', 
#                 'name_last': 'Smith', 
#                 'handle_str': 'joesmith'
#             }, 
#             {   'u_id': login_marry, 
#                 'email': 'marryjoe222@gmail.com', 
#                 'name_first': 'Marry', 
#                 'name_last': 'Joe', 
#                 'handle_str': 'marryjoe'
#             }
#         ]
#     }
    
