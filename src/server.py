import sys
import signal
from json import dumps
from flask import Flask, request
from flask_cors import CORS
from src.error import InputError
from src import config
# from src.users import user_profile_sethandle_v1, user_profile_setemail_v1, user_profile_setname_v1, user_profile_v1, user_all_v1
from src.users import *
from src.auth import auth_register_v1, auth_login_v1, auth_logout_v1
from src.other import clear_v1
from src.channels import channels_create_v1, channels_list_v1, channels_listall_v1
from src.channel import channel_invite_v1, channel_join_v1, channel_details_v1, channel_leave_v1, channel_addowner_v1, channel_removeowner_v1
from src.message import message_send_v1, message_edit_v1, message_remove_v1
from src.admin import admin_user_remove_v1, admin_userpermission_change_v1


def quit_gracefully(*args):
    '''For coverage'''
    exit(0)

def defaultHandler(err):
    response = err.get_response()
    print('response', err, err.get_response())
    response.data = dumps({
        "code": err.code,
        "name": "System Error",
        "message": err.get_description(),
    })
    response.content_type = 'application/json'
    return response

APP = Flask(__name__)
CORS(APP)

APP.config['TRAP_HTTP_EXCEPTIONS'] = True
APP.register_error_handler(Exception, defaultHandler)

#### NO NEED TO MODIFY ABOVE THIS POINT, EXCEPT IMPORTS

@APP.route("/auth/register/v2", methods=['POST'])
def register_user():
    request_data = request.get_json()
    token_and_auth_user_id = auth_register_v1(request_data['email'], request_data['password'], request_data['name_first'], request_data['name_last'])
    return dumps(token_and_auth_user_id)

@APP.route("/clear/v1", methods=['DELETE'])
def clear_everything():
    clear_v1()
    return dumps({})

@APP.route("/auth/login/v2", methods=['POST'])
def auth_login():
    request_data = request.get_json()
    token_and_auth_user_id = auth_login_v1(request_data['email'], request_data['password'])
    return dumps(token_and_auth_user_id)

@APP.route("/auth/logout/v1", methods=['POST'])
def auth_logout():
    request_data = request.get_json()
    logging_out = auth_logout_v1(request_data['token'])
    return dumps(logging_out)


@APP.route("/channels/create/v2", methods=['POST'])
def channels_create():
    request_data = request.get_json()
    channel_id = channels_create_v1(request_data['token'], request_data['name'], request_data['is_public'])
    return dumps(channel_id)

@APP.route("/channel/invite/v2", methods=['POST'])
def channels_invite():
    request_data = request.get_json()
    response = channel_invite_v1(request_data['token'], request_data['channel_id'], request_data['u_id'])
    return dumps(response)

@APP.route("/message/send/v1", methods=['POST'])
def send_message():
    request_data = request.get_json()
    message_id = message_send_v1(request_data['token'], request_data['channel_id'], request_data['message'])
    return dumps(message_id)

@APP.route("/channel/details/v2", methods = ['GET'])
def channel_details():
    request_data = request.get_json('data')
    details = channel_details_v1(request_data['token'], request_data['channel_id'])
    return dumps(details)

@APP.route("/channel/leave/v1", methods = ['POST'])
def channel_leave():
    request_data = request.get_json('data')
    response = channel_leave_v1(request_data['token'], request_data['channel_id'])
    return dumps(response)
    
@APP.route("/channel/addowner/v1", methods = ['POST'])
def channel_addowner():
    request_data = request.get_json('data')
    response = channel_addowner_v1(request_data['token'], request_data['channel_id'], request_data['u_id'])
    return dumps(response)

@APP.route("/channel/removeowner/v1", methods = ['POST'])
def channel_removeowner():
    request_data = request.get_json('data')
    response = channel_removeowner_v1(request_data['token'], request_data['channel_id'], request_data['u_id'])
    return dumps(response)

@APP.route("/message/edit/v1", methods=['PUT'])
def edit_message():
    request_data = request.get_json()
    message_id = message_edit_v1(request_data['token'], request_data['message_id'], request_data['message'])
    return dumps(message_id)

@APP.route("/message/remove/v1", methods=['DELETE'])
def delete_message():
    request_data = request.get_json()
    response = message_remove_v1(request_data['token'], request_data['message_id'])
    return dumps(response)

@APP.route("/channel/join/v2", methods = ['POST'])
def channel_join():
    request_data = request.get_json()
    response = channel_join_v1(request_data['token'], request_data['channel_id'])
    return dumps(response)  

@APP.route("/channels/list/v2", methods = ['GET'])
def channel_list():
    request_data = request.get_json()
    channels = channels_list_v1(request_data['token'])
    return dumps(channels)  

@APP.route("/channels/listall/v2", methods = ['GET'])
def channel_listall():
    request_data = request.get_json()
    channels = channels_listall_v1(request_data['token'])
    return dumps(channels)  

@APP.route("/user/profile/sethandle/v1", methods=['PUT'])
def user_profile_sethandle():
    request_data = request.get_json()
    response = user_profile_sethandle_v1(request_data['token'], request_data['handle_str'])
    return dumps(response)

@APP.route("/admin/user/remove/v1", methods=['DELETE'])
def adminuser_remove_v1():
    request_data = request.get_json()
    response = admin_user_remove_v1(request_data['token'], request_data['u_id'])
    return dumps(response)

@APP.route("/admin/userpermission/change/v1", methods=['POST'])
def userpermission_change_v1():
    request_data = request.get_json()
    response = admin_userpermission_change_v1(request_data['token'], request_data['u_id'], request_data['permission_id'])
    return dumps(response)



# List of all users
@APP.route("/user/all/v1", methods=['GET'])
def user_all(token):
    request_data = request.get_json()

    user = user_all_v1(request_data['token'])

    return dumps(user)


# List of all valid users
@APP.route("/user/profile/v1", methods=['GET'])
def user_profile():
    request_data = request.get_json()

    user = user_profile_v1(request_data['token'], request_data['user_id'])

    return dumps(user)


# Update name
@APP.route("/user/profile/setname/v1", methods=['PUT'])
def user_profile_setname():
    request_data = request.get_json()

    response = user_profile_setname_v1(request_data['token'], request_data['first_names'], request_data['last_names'])
    return dumps(response)


# Update email
@APP.route("/user/profile/setemail/v1", methods=['PUT'])
def user_profile_setemail():
    request_data = request.get_json()
    response = user_profile_setemail_v1(request_data['token'], request_data['emails'])

    return dumps(response)


# # Update handle
# @APP.route("/users/profile/sethandle/v1", methods=['PUT'])
# def user_profile_sethandle_v1(toke, handle_str):
#     request_data = request.get_json()

#     return dumps()


# @APP.route("/channel/leave/v1", methods=['POST'])
# def channel_leave_v1(token, channel_id):
#     request_data = request.get_json()

#     channel_id = channel_leave_v1(request_data['token'], request_data['channel_id'])

#     del ['channels']['all_members'][channel_id]

#     return dumps()




# Example
@APP.route("/echo", methods=['GET'])
def echo():
    data = request.args.get('data')
    if data == 'echo':
   	    raise InputError(description='Cannot echo "echo"')
    return dumps({
    })

#### NO NEED TO MODIFY BELOW THIS POINT

if __name__ == "__main__":
    signal.signal(signal.SIGINT, quit_gracefully) # For coverage
    APP.run(port=config.port) # Do not edit this port
