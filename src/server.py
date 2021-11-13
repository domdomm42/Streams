import sys
import signal
from json import dumps
import json
from flask import Flask, request, send_from_directory
from flask_cors import CORS
from src.error import InputError
from src import config
from src.users import *
from src.auth import auth_register_v1, auth_login_v1, auth_logout_v1, auth_passwordreset_request_v1, \
    auth_passwordreset_reset_v1
from src.other import clear_v1, print_store_debug
from src.channels import channels_create_v1, channels_list_v1, channels_listall_v1
from src.channel import channel_invite_v1, channel_join_v1, channel_details_v1, channel_leave_v1, channel_addowner_v1, \
    channel_removeowner_v1, channel_messages_v1
from src.message import message_send_v1, message_edit_v1, message_remove_v1, message_senddm_v1, message_sendlater_v1, \
    message_sendlaterdm_v1
from src.admin import admin_user_remove_v1, admin_userpermission_change_v1
from src.DM_functions import dm_create_v1, dm_list_v1, dm_remove_v1, dm_leave_v1, dm_messages_v1, dm_details_v1
from src.notifications import notifications_get_v1
from src.standup import standup_active_v1, standup_send_v1, standup_start_v1

'''
Persistence implementation

This is commented out, as git ignores the database.json, which will
cause the pipeline to fail on gitLab

with open('database.json', 'r') as FILE:
    data = json.load(FILE)
    data_store.set(data)

def save():
    data = data_store.get()
    with open('database.json', 'w') as FILE:
        json.dump(data, FILE)
'''


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


APP = Flask(__name__, static_url_path='/src/static/')
CORS(APP)

APP.config['TRAP_HTTP_EXCEPTIONS'] = True
APP.register_error_handler(Exception, defaultHandler)


#### NO NEED TO MODIFY ABOVE THIS POINT, EXCEPT IMPORTS

@APP.route("/auth/register/v2", methods=['POST'])
def register_user():
    request_data = request.get_json()
    token_and_auth_user_id = auth_register_v1(request_data['email'], request_data['password'],
                                              request_data['name_first'], request_data['name_last'])
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


@APP.route("/auth/passwordreset/request/v1", methods=['POST'])
def password_reset_request():
    request_data = request.get_json()
    auth_passwordreset_request_v1(request_data['email'])
    return dumps({})


@APP.route("/auth/passwordreset/reset/v1", methods=['POST'])
def password_reset_reset():
    request_data = request.get_json()
    auth_passwordreset_reset_v1(request_data['reset_code'], request_data['new_password'])
    return dumps({})


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


@APP.route("/channel/details/v2", methods=['GET'])
def channel_details():
    token = request.args.get('token')
    channel_id = int(request.args.get('channel_id'))
    details = channel_details_v1(token, channel_id)
    return dumps(details)


@APP.route("/channel/messages/v2", methods=['GET'])
def channel_messages():
    token = request.args.get('token')
    channel_id = int(request.args.get('channel_id'))
    start = int(request.args.get('start'))
    details = channel_messages_v1(token, channel_id, start)
    return dumps(details)


@APP.route("/channel/leave/v1", methods=['POST'])
def channel_leave():
    request_data = request.get_json('data')
    response = channel_leave_v1(request_data['token'], request_data['channel_id'])
    return dumps(response)


@APP.route("/channel/addowner/v1", methods=['POST'])
def channel_addowner():
    request_data = request.get_json('data')
    response = channel_addowner_v1(request_data['token'], request_data['channel_id'], request_data['u_id'])
    return dumps(response)


@APP.route("/channel/removeowner/v1", methods=['POST'])
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


@APP.route("/channel/join/v2", methods=['POST'])
def channel_join():
    request_data = request.get_json()
    response = channel_join_v1(request_data['token'], request_data['channel_id'])
    return dumps(response)


@APP.route("/channels/list/v2", methods=['GET'])
def channel_list():
    token = request.args.get('token')
    channels = channels_list_v1(token)
    return dumps(channels)


@APP.route("/channels/listall/v2", methods=['GET'])
def channel_listall():
    token = request.args.get('token')
    channels = channels_listall_v1(token)
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
    response = admin_userpermission_change_v1(request_data['token'], request_data['u_id'],
                                              request_data['permission_id'])
    return dumps(response)


@APP.route("/message/senddm/v1", methods=['POST'])
def send_dm():
    request_data = request.get_json()
    message_id = message_senddm_v1(request_data['token'], request_data['dm_id'], request_data['message'])
    return dumps(message_id)


# Example
@APP.route("/echo", methods=['GET'])
def echo():
    data = request.args.get('data')
    if data == 'echo':
        raise InputError(description='Cannot echo "echo"')
    return dumps({})


# List of all users
@APP.route("/users/all/v1", methods=['GET'])
def user_all():
    token = request.args.get('token')
    users = user_all_v1(token)
    return dumps(users)


# List of all valid users
@APP.route("/user/profile/v1", methods=['GET'])
def user_profile():
    token = request.args.get('token')
    u_id = int(request.args.get('u_id'))
    user = user_profile_v1(token, u_id)
    return dumps(user)


# Update name
@APP.route("/user/profile/setname/v1", methods=['PUT'])
def user_profile_setname():
    request_data = request.get_json()
    response = user_profile_setname_v1(request_data['token'], request_data['name_first'], request_data['name_last'])
    return dumps(response)


# Update email
@APP.route("/user/profile/setemail/v1", methods=['PUT'])
def user_profile_setemail():
    request_data = request.get_json()
    response = user_profile_setemail_v1(request_data['token'], request_data['email'])
    return dumps(response)


@APP.route("/dm/create/v1", methods=['POST'])
def dm_create():
    request_data = request.get_json()
    dm_id = dm_create_v1(request_data['token'], request_data['u_ids'])
    return dumps(dm_id)


@APP.route("/dm/list/v1", methods=['GET'])
def dm_list():
    token = request.args.get('token')
    dms = dm_list_v1(token)
    return dumps(dms)


@APP.route("/dm/remove/v1", methods=['DELETE'])
def dm_remove():
    request_data = request.get_json()
    response = dm_remove_v1(request_data['token'], request_data['dm_id'])
    return dumps(response)


@APP.route("/dm/details/v1", methods=['GET'])
def dm_details():
    token = request.args.get('token')
    dm_id = int(request.args.get('dm_id'))
    details = dm_details_v1(token, dm_id)
    return dumps(details)


@APP.route("/dm/leave/v1", methods=['POST'])
def dm_leave():
    request_data = request.get_json()
    response = dm_leave_v1(request_data['token'], request_data['dm_id'])
    return dumps(response)


@APP.route("/dm/messages/v1", methods=['GET'])
def dm_messages():
    token = request.args.get('token')
    start = int(request.args.get('start'))
    dm_id = int(request.args.get('dm_id'))
    messages = dm_messages_v1(token, dm_id, start)
    return dumps(messages)


@APP.route("/message/sendlater/v1", methods=['POST'])
def send_later():
    request_data = request.get_json()
    response = message_sendlater_v1(request_data['token'], request_data['channel_id'], request_data['message'],
                                    request_data['time_sent'])
    return dumps(response)


@APP.route("/message/sendlaterdm/v1", methods=['POST'])
def send_laterdm():
    request_data = request.get_json()
    response = message_sendlaterdm_v1(request_data['token'], request_data['dm_id'], request_data['message'],
                                      request_data['time_sent'])
    return dumps(response)


@APP.route("/notifications/get/v1", methods=['GET'])
def notifications():
    token = request.args.get('token')
    notifications = notifications_get_v1(token)
    return dumps(notifications)


@APP.route("/user/profile/uploadphoto/v1", methods=['POST'])
def user_profile_uploadphoto():
    request_data = request.get_json()
    response = user_profile_uploadphoto_v1(request_data['token'], request_data['img_url'], request_data['x_start'],
                                           request_data['y_start'], request_data['x_end'], request_data['y_end'])

    return dumps(response)


@APP.route("/user/stats/v1", methods=['GET'])
def user_stats():
    token = request.args.get('token')
    user_stats = user_stats_v1(token)
    return dumps(user_stats)


@APP.route("/users/stats/v1", methods=['GET'])
def users_stats():
    token = request.args.get('token')
    users_stats = users_stats_v1(token)
    return dumps(users_stats)


@APP.route("/debug/printstore", methods=['GET'])
def print_store():
    print_store_debug()
    return dumps({})


@APP.route("/standup/start/v1", methods=['POST'])
def standup_start():
    request_data = request.get_json()
    response = standup_start_v1(request_data['token'], request_data['channel_id'], request_data['length'])
    return dumps(response)


@APP.route("/standup/active/v1", methods=['GET'])
def standup_active():
    token = request.args.get('token')
    channel_id = int(request.args.get('channel_id'))
    response = standup_active_v1(token, channel_id)
    return dumps(response)


@APP.route("/standup/send/v1", methods=['POST'])
def standup_send():
    request_data = request.get_json()
    response = standup_send_v1(request_data['token'], request_data['channel_id'], request_data['message'])
    return dumps(response)

@APP.route("/src/static/<path:path>")
def send_js(path):
    return send_from_directory('', path)


#### NO NEED TO MODIFY BELOW THIS POINT
if __name__ == "__main__":
    signal.signal(signal.SIGINT, quit_gracefully)  # For coverage
    APP.run(port=config.port)  # Do not edit this port
