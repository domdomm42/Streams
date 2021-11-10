from flask.globals import request
import pytest
import requests
from datetime import datetime, timezone
import time

from src.config import *
BASE_URL = url
INPUT_ERROR = 400
ACCESS_ERROR = 403

@pytest.fixture
def setup_users():
    requests.delete(f'{BASE_URL}/clear/v1')

    # Create user Joe Smith
    user_info = {"email": "joe123@gmail.com", "password": "delicious23", "name_first": "Joe", "name_last": "Smith"}
    joe_smith_data = requests.post(f'{BASE_URL}/auth/register/v2', json = user_info).json()

    # Create user Marry Mae
    user_info = {"email": "marrymae@gmail.com", "password": "cats1010", "name_first": "Marry", "name_last": "Mae"}
    marry_mae_data = requests.post(f'{BASE_URL}/auth/register/v2', json = user_info).json()

    return joe_smith_data['token'], marry_mae_data['token']

@pytest.fixture
def setup_channel(setup_users):

    joe_smith_token, marry_mae_token = setup_users

    # Joe Smith creates a Private channel named "Joe's Reading Club"
    channel_info = {"token": joe_smith_token, "name": "Joe's Reading Club", "is_public": False}
    joes_funland_data = requests.post(f'{BASE_URL}/channels/create/v2', json = channel_info).json()

    return joe_smith_token, marry_mae_token, joes_funland_data

@pytest.fixture
def setup_dm(setup_users):

    joe_smith_token, marry_mae_token = setup_users

    # Create another user Darron Mike
    user_info = {"email": "darronmike@gmail.com", "password": "delicious23", "name_first": "Darron", "name_last": "Mike"}
    darron_mike_token = requests.post(f'{BASE_URL}/auth/register/v2', json = user_info).json()['token']

    # Joe Smith creates a DM with Marry and Darron in it
    dm_info = {"token": joe_smith_token, "u_ids": [1, 2]}
    joe_dm_data = requests.post(f'{BASE_URL}/dm/create/v1', json = dm_info).json()

    return joe_smith_token, marry_mae_token, darron_mike_token, joe_dm_data

'''
Test Invited to a Channel Notifications
'''
def test_invite_to_channel(setup_channel):

    joe_smith_token, marry_mae_token, joes_funland_data = setup_channel

    # Ensure Marry has no notifications at the moment
    notification_input = {"token": marry_mae_token}
    response = requests.get(f'{BASE_URL}/notifications/get/v1', params = notification_input).json()
    assert response == {'notifications': []}

    # Invite Marry to the channel
    channel_invite_info = {'token': joe_smith_token, 'channel_id': joes_funland_data['channel_id'], 'u_id': 1}
    response = requests.post(f'{BASE_URL}/channel/invite/v2', json = channel_invite_info)
    assert response.status_code in [200, 201]
    
    # Marry has one notification
    notification_input = {"token": marry_mae_token}
    response = requests.get(f'{BASE_URL}/notifications/get/v1', params = notification_input).json()
    assert response == {
        'notifications': [
            {
                'channel_id': 0,
                'dm_id': -1,
                'notification_message': "joesmith added you to Joe's Reading Club"
            }
        ]
    }

def test_invited_to_multiple_channels(setup_channel):

    joe_smith_token, marry_mae_token, joes_funland_data = setup_channel

    # Ensure Marry has no notifications at the moment
    notification_input = {"token": marry_mae_token}
    response = requests.get(f'{BASE_URL}/notifications/get/v1', params = notification_input).json()
    assert response == {'notifications': []}

    # Invite Marry to the channel
    channel_invite_info = {'token': joe_smith_token, 'channel_id': joes_funland_data['channel_id'], 'u_id': 1}
    response = requests.post(f'{BASE_URL}/channel/invite/v2', json = channel_invite_info)
    assert response.status_code in [200, 201]
    
    # Marry has one notification
    notification_input = {"token": marry_mae_token}
    response = requests.get(f'{BASE_URL}/notifications/get/v1', params = notification_input).json()
    assert response == {
        'notifications': [
            {
                'channel_id': 0,
                'dm_id': -1,
                'notification_message': "joesmith added you to Joe's Reading Club"
            }
        ]
    }

    # Create another user Darron Mike
    user_info = {"email": "darronmike@gmail.com", "password": "delicious23", "name_first": "Darron", "name_last": "Mike"}
    darron_mike_data = requests.post(f'{BASE_URL}/auth/register/v2', json = user_info).json()

    # Darron Mike creates a Public channel named "Games"
    channel_info = {"token": darron_mike_data['token'], "name": "Games", "is_public": True}
    games_data = requests.post(f'{BASE_URL}/channels/create/v2', json = channel_info).json()

    # Darron invites Marry to "Games" channel
    channel_invite_info = {'token': darron_mike_data['token'], 'channel_id': games_data['channel_id'], 'u_id': 1}
    response = requests.post(f'{BASE_URL}/channel/invite/v2', json = channel_invite_info)
    assert response.status_code in [200, 201]

    # Marry has two notification
    notification_input = {"token": marry_mae_token}
    response = requests.get(f'{BASE_URL}/notifications/get/v1', params = notification_input).json()
    assert response == {
        'notifications': [
            {
                'channel_id': 1,
                'dm_id': -1,
                'notification_message': "darronmike added you to Games"
            },
            {
                'channel_id': 0,
                'dm_id': -1,
                'notification_message': "joesmith added you to Joe's Reading Club"
            }
        ]
    }

'''
Test Tagged in a Channel Message Notifications
'''
def test_tagged_message_to_channel(setup_channel):

    joe_smith_token, marry_mae_token, joes_funland_data = setup_channel

    # Ensure Marry has no notifications at the moment
    notification_input = {"token": marry_mae_token}
    response = requests.get(f'{BASE_URL}/notifications/get/v1', params = notification_input).json()
    assert response == {'notifications': []}

    # Joe sends a message which tags Marry but Marry is not in the channel so she should not get a notification
    message_send_input = {"token": joe_smith_token, "channel_id": joes_funland_data['channel_id'], "message": "Hi @marrymae!"}
    response = requests.post(f'{BASE_URL}/message/send/v1', json = message_send_input)
    assert response.status_code in [200, 201]

    # Ensure Marry has no notifications at the moment
    notification_input = {"token": marry_mae_token}
    response = requests.get(f'{BASE_URL}/notifications/get/v1', params = notification_input).json()
    assert response == {'notifications': []}

    # Invite Marry to the channel
    channel_invite_info = {'token': joe_smith_token, 'channel_id': joes_funland_data['channel_id'], 'u_id': 1}
    response = requests.post(f'{BASE_URL}/channel/invite/v2', json = channel_invite_info)
    assert response.status_code in [200, 201]

    # Joe sends another message which tags Marry
    message_send_input = {"token": joe_smith_token, "channel_id": joes_funland_data['channel_id'], "message": "Hi @marrymae! Again"}
    response = requests.post(f'{BASE_URL}/message/send/v1', json = message_send_input)
    assert response.status_code in [200, 201]

    # Marry has two notifications
    notification_input = {"token": marry_mae_token}
    response = requests.get(f'{BASE_URL}/notifications/get/v1', params = notification_input).json()
    assert response == {
        'notifications': [
            {
                'channel_id': 0,
                'dm_id': -1,
                'notification_message': "joesmith tagged you in Joe's Reading Club: Hi @marrymae! Again"
            },
            {
                'channel_id': 0,
                'dm_id': -1,
                'notification_message': "joesmith added you to Joe's Reading Club"
            }
        ]
    }

def test_tagged_message_to_channel_over_20(setup_channel):

    joe_smith_token, marry_mae_token, joes_funland_data = setup_channel

    # Ensure Marry has no notifications at the moment
    notification_input = {"token": marry_mae_token}
    response = requests.get(f'{BASE_URL}/notifications/get/v1', params = notification_input).json()
    assert response == {'notifications': []}

    # Invite Marry to the channel
    channel_invite_info = {'token': joe_smith_token, 'channel_id': joes_funland_data['channel_id'], 'u_id': 1}
    response = requests.post(f'{BASE_URL}/channel/invite/v2', json = channel_invite_info)
    assert response.status_code in [200, 201]

    for num in range(0,30):
        message_send_input = {"token": joe_smith_token, "channel_id": joes_funland_data['channel_id'], "message": f"Hi @marrymae! {num}"}
        response = requests.post(f'{BASE_URL}/message/send/v1', json = message_send_input)
        assert response.status_code in [200, 201]

    # Marry has twenty recent notification
    notification_input = {"token": marry_mae_token}
    response = requests.get(f'{BASE_URL}/notifications/get/v1', params = notification_input).json()
    assert response == {
        'notifications': [
            {'channel_id': 0, 'dm_id': -1, 'notification_message': "joesmith tagged you in Joe's Reading Club: Hi @marrymae! 29"},
            {'channel_id': 0, 'dm_id': -1, 'notification_message': "joesmith tagged you in Joe's Reading Club: Hi @marrymae! 28"},
            {'channel_id': 0, 'dm_id': -1, 'notification_message': "joesmith tagged you in Joe's Reading Club: Hi @marrymae! 27"},
            {'channel_id': 0, 'dm_id': -1, 'notification_message': "joesmith tagged you in Joe's Reading Club: Hi @marrymae! 26"},
            {'channel_id': 0, 'dm_id': -1, 'notification_message': "joesmith tagged you in Joe's Reading Club: Hi @marrymae! 25"},
            {'channel_id': 0, 'dm_id': -1, 'notification_message': "joesmith tagged you in Joe's Reading Club: Hi @marrymae! 24"},
            {'channel_id': 0, 'dm_id': -1, 'notification_message': "joesmith tagged you in Joe's Reading Club: Hi @marrymae! 23"},
            {'channel_id': 0, 'dm_id': -1, 'notification_message': "joesmith tagged you in Joe's Reading Club: Hi @marrymae! 22"},
            {'channel_id': 0, 'dm_id': -1, 'notification_message': "joesmith tagged you in Joe's Reading Club: Hi @marrymae! 21"},
            {'channel_id': 0, 'dm_id': -1, 'notification_message': "joesmith tagged you in Joe's Reading Club: Hi @marrymae! 20"},
            {'channel_id': 0, 'dm_id': -1, 'notification_message': "joesmith tagged you in Joe's Reading Club: Hi @marrymae! 19"},
            {'channel_id': 0, 'dm_id': -1, 'notification_message': "joesmith tagged you in Joe's Reading Club: Hi @marrymae! 18"},
            {'channel_id': 0, 'dm_id': -1, 'notification_message': "joesmith tagged you in Joe's Reading Club: Hi @marrymae! 17"},
            {'channel_id': 0, 'dm_id': -1, 'notification_message': "joesmith tagged you in Joe's Reading Club: Hi @marrymae! 16"},
            {'channel_id': 0, 'dm_id': -1, 'notification_message': "joesmith tagged you in Joe's Reading Club: Hi @marrymae! 15"},
            {'channel_id': 0, 'dm_id': -1, 'notification_message': "joesmith tagged you in Joe's Reading Club: Hi @marrymae! 14"},
            {'channel_id': 0, 'dm_id': -1, 'notification_message': "joesmith tagged you in Joe's Reading Club: Hi @marrymae! 13"},
            {'channel_id': 0, 'dm_id': -1, 'notification_message': "joesmith tagged you in Joe's Reading Club: Hi @marrymae! 12"},
            {'channel_id': 0, 'dm_id': -1, 'notification_message': "joesmith tagged you in Joe's Reading Club: Hi @marrymae! 11"},
            {'channel_id': 0, 'dm_id': -1, 'notification_message': "joesmith tagged you in Joe's Reading Club: Hi @marrymae! 10"}
        ]
    }

def test_tagging_themself_in_messages(setup_channel):

    joe_smith_token, _, joes_funland_data = setup_channel

    # Ensure Joe has no notifications at the moment
    notification_input = {"token": joe_smith_token}
    response = requests.get(f'{BASE_URL}/notifications/get/v1', params = notification_input).json()
    assert response == {'notifications': []}

    # Joe sends a message which tags himself, he should not get a notification
    message_send_input = {"token": joe_smith_token, "channel_id": joes_funland_data['channel_id'], "message": "Hi @joesmith!"}
    response = requests.post(f'{BASE_URL}/message/send/v1', json = message_send_input)
    assert response.status_code in [200, 201]

    # Ensure Joe has no notifications at the moment
    notification_input = {"token": joe_smith_token}
    response = requests.get(f'{BASE_URL}/notifications/get/v1', params = notification_input).json()
    assert response == {'notifications': []}

def test_sendlater_notification(setup_channel):

    joe_smith_token, marry_mae_token, joes_funland_data = setup_channel

    # Ensure Joe has no notifications at the moment
    notification_input = {"token": joe_smith_token}
    response = requests.get(f'{BASE_URL}/notifications/get/v1', params = notification_input).json()
    assert response == {'notifications': []}    

    # Invite Marry to the channel
    channel_invite_info = {'token': joe_smith_token, 'channel_id': joes_funland_data['channel_id'], 'u_id': 1}
    response = requests.post(f'{BASE_URL}/channel/invite/v2', json = channel_invite_info)
    assert response.status_code in [200, 201]

    # Marry sends a message for later
    message_later_time = int(datetime.now(timezone.utc).timestamp()) + 2
    message_send_input = {"token": marry_mae_token, "channel_id": joes_funland_data['channel_id'], "message": "Hi @joesmith!", "time_sent": message_later_time}
    response = requests.post(f'{BASE_URL}/message/sendlater/v1', json = message_send_input)
    assert response.status_code in [200, 201]

    # Ensure Joe has no notifications at the moment
    notification_input = {"token": joe_smith_token}
    response = requests.get(f'{BASE_URL}/notifications/get/v1', params = notification_input).json()
    assert response == {'notifications': []}    

    time.sleep(3)

    # After the message_later_time Joe has one notification
    notification_input = {"token": joe_smith_token}
    response = requests.get(f'{BASE_URL}/notifications/get/v1', params = notification_input).json()
    assert response == {
        'notifications': [
            {
                'channel_id': 0,
                'dm_id': -1,
                'notification_message': "marrymae tagged you in Joe's Reading Club: Hi @joesmith!"
            },
        ]
    }

'''
Test Added to a DM Notifications
'''
def test_added_to_dm(setup_dm):

    joe_smith_token, marry_mae_token, darron_mike_token, _ = setup_dm

    # Joe has no notifications
    notification_input = {"token": joe_smith_token}
    response = requests.get(f'{BASE_URL}/notifications/get/v1', params = notification_input).json()
    assert response == {'notifications': []}

    # Marry has one notification
    notification_input = {"token": marry_mae_token}
    response = requests.get(f'{BASE_URL}/notifications/get/v1', params = notification_input).json()
    assert response == {
        'notifications': [
            {
                'channel_id': -1,
                'dm_id': 0,
                'notification_message': "joesmith added you to darronmike, joesmith, marrymae"
            }
        ]
    }

    # Darron has one notification
    notification_input = {"token": darron_mike_token}
    response = requests.get(f'{BASE_URL}/notifications/get/v1', params = notification_input).json()
    assert response == {
        'notifications': [
            {
                'channel_id': -1,
                'dm_id': 0,
                'notification_message': "joesmith added you to darronmike, joesmith, marrymae"
            }
        ]
    }

def test_added_multiple_dms(setup_dm):

    joe_smith_token, marry_mae_token, _, _ = setup_dm

    # Create another user Peppa Pig
    user_info = {"email": "peppapig@gmail.com", "password": "delicious23", "name_first": "Peppa", "name_last": "Pig"}
    peppa_pig_data = requests.post(f'{BASE_URL}/auth/register/v2', json = user_info).json()

    # Peppa Pig makes a DM with Joe and Marry in it
    dm_info = {"token": peppa_pig_data['token'], "u_ids": [0, 1]}
    response = requests.post(f'{BASE_URL}/dm/create/v1', json = dm_info)
    assert response.status_code in [200, 201]

    notification_input = {"token": joe_smith_token}
    response = requests.get(f'{BASE_URL}/notifications/get/v1', params = notification_input).json()
    assert response == {
        'notifications': [
            {
                'channel_id': -1,
                'dm_id': 1,
                'notification_message': "peppapig added you to joesmith, marrymae, peppapig"
            }
        ]
    } 

    notification_input = {"token": marry_mae_token}
    response = requests.get(f'{BASE_URL}/notifications/get/v1', params = notification_input).json()
    assert response == {
        'notifications': [
            {
                'channel_id': -1,
                'dm_id': 1,
                'notification_message': "peppapig added you to joesmith, marrymae, peppapig"
            },
            {
                'channel_id': -1,
                'dm_id': 0,
                'notification_message': "joesmith added you to darronmike, joesmith, marrymae"
            }
        ]
    }  

'''
Test Tagged in a DM Message Notifications
'''

def test_tagged_message_to_dm(setup_dm):

    joe_smith_token, marry_mae_token, _, joe_dm_data = setup_dm

    # Create another user Peppa Pig
    user_info = {"email": "peppapig@gmail.com", "password": "delicious23", "name_first": "Peppa", "name_last": "Pig"}
    peppa_pig_data = requests.post(f'{BASE_URL}/auth/register/v2', json = user_info).json()

    # Joe Smith sends a message to DM which tages Peppa Pig
    message_send_input = {"token": joe_smith_token, "dm_id": joe_dm_data['dm_id'], "message": "Hi @peppapig"}
    response = requests.post(f'{BASE_URL}/message/senddm/v1', json = message_send_input)
    assert response.status_code in [200, 201]

    # Peppa should not receive any notification that Joe tagged her in a message since Peppa is not a part of the channel
    notification_input = {"token": peppa_pig_data['token']}
    response = requests.get(f'{BASE_URL}/notifications/get/v1', params = notification_input).json()
    assert response == {'notifications': []}

    # Joe Smith sends a message to DM which tags Marry Mae
    message_send_input = {"token": joe_smith_token, "dm_id": joe_dm_data['dm_id'], "message": "Hi @marrymae"}
    response = requests.post(f'{BASE_URL}/message/senddm/v1', json = message_send_input)
    assert response.status_code in [200, 201]

    # Marry has two notifications
    notification_input = {"token": marry_mae_token}
    response = requests.get(f'{BASE_URL}/notifications/get/v1', params = notification_input).json()
    assert response == {
        'notifications': [
            {
                'channel_id': -1,
                'dm_id': 0,
                'notification_message': "joesmith tagged you in darronmike, joesmith, marrymae: Hi @marrymae"
            },
            {
                'channel_id': -1,
                'dm_id': 0,
                'notification_message': "joesmith added you to darronmike, joesmith, marrymae"
            }
        ]
    }

def test_tagged_message_to_dm_over_20(setup_dm):

    joe_smith_token, marry_mae_token, _, joe_dm_data = setup_dm

    # Marry has one notification
    notification_input = {"token": marry_mae_token}
    response = requests.get(f'{BASE_URL}/notifications/get/v1', params = notification_input).json()
    assert response == {
        'notifications': [
            {
                'channel_id': -1,
                'dm_id': 0,
                'notification_message': "joesmith added you to darronmike, joesmith, marrymae"
            }
        ]
    }

    for num in range(0,30):
        message_senddm_input = {"token": joe_smith_token, "dm_id": joe_dm_data['dm_id'], "message": f"Hi @marrymae! {num}"}
        response = requests.post(f'{BASE_URL}/message/senddm/v1', json = message_senddm_input)
        assert response.status_code in [200, 201]
        
    # Marry has twenty recent notification
    notification_input = {"token": marry_mae_token}
    response = requests.get(f'{BASE_URL}/notifications/get/v1', params = notification_input).json()

    assert response == {
        'notifications': [
            {'channel_id': -1, 'dm_id': 0, 'notification_message': "joesmith tagged you in darronmike, joesmith, marrymae: Hi @marrymae! 29"},
            {'channel_id': -1, 'dm_id': 0, 'notification_message': "joesmith tagged you in darronmike, joesmith, marrymae: Hi @marrymae! 28"},
            {'channel_id': -1, 'dm_id': 0, 'notification_message': "joesmith tagged you in darronmike, joesmith, marrymae: Hi @marrymae! 27"},
            {'channel_id': -1, 'dm_id': 0, 'notification_message': "joesmith tagged you in darronmike, joesmith, marrymae: Hi @marrymae! 26"},
            {'channel_id': -1, 'dm_id': 0, 'notification_message': "joesmith tagged you in darronmike, joesmith, marrymae: Hi @marrymae! 25"},
            {'channel_id': -1, 'dm_id': 0, 'notification_message': "joesmith tagged you in darronmike, joesmith, marrymae: Hi @marrymae! 24"},
            {'channel_id': -1, 'dm_id': 0, 'notification_message': "joesmith tagged you in darronmike, joesmith, marrymae: Hi @marrymae! 23"},
            {'channel_id': -1, 'dm_id': 0, 'notification_message': "joesmith tagged you in darronmike, joesmith, marrymae: Hi @marrymae! 22"},
            {'channel_id': -1, 'dm_id': 0, 'notification_message': "joesmith tagged you in darronmike, joesmith, marrymae: Hi @marrymae! 21"},
            {'channel_id': -1, 'dm_id': 0, 'notification_message': "joesmith tagged you in darronmike, joesmith, marrymae: Hi @marrymae! 20"},
            {'channel_id': -1, 'dm_id': 0, 'notification_message': "joesmith tagged you in darronmike, joesmith, marrymae: Hi @marrymae! 19"},
            {'channel_id': -1, 'dm_id': 0, 'notification_message': "joesmith tagged you in darronmike, joesmith, marrymae: Hi @marrymae! 18"},
            {'channel_id': -1, 'dm_id': 0, 'notification_message': "joesmith tagged you in darronmike, joesmith, marrymae: Hi @marrymae! 17"},
            {'channel_id': -1, 'dm_id': 0, 'notification_message': "joesmith tagged you in darronmike, joesmith, marrymae: Hi @marrymae! 16"},
            {'channel_id': -1, 'dm_id': 0, 'notification_message': "joesmith tagged you in darronmike, joesmith, marrymae: Hi @marrymae! 15"},
            {'channel_id': -1, 'dm_id': 0, 'notification_message': "joesmith tagged you in darronmike, joesmith, marrymae: Hi @marrymae! 14"},
            {'channel_id': -1, 'dm_id': 0, 'notification_message': "joesmith tagged you in darronmike, joesmith, marrymae: Hi @marrymae! 13"},
            {'channel_id': -1, 'dm_id': 0, 'notification_message': "joesmith tagged you in darronmike, joesmith, marrymae: Hi @marrymae! 12"},
            {'channel_id': -1, 'dm_id': 0, 'notification_message': "joesmith tagged you in darronmike, joesmith, marrymae: Hi @marrymae! 11"},
            {'channel_id': -1, 'dm_id': 0, 'notification_message': "joesmith tagged you in darronmike, joesmith, marrymae: Hi @marrymae! 10"}
        ]
    }

def test_tagging_themself_in_messagesdm(setup_dm):

    joe_smith_token, _, _, joe_dm_data = setup_dm

    # Ensure Joe has no notifications at the moment
    notification_input = {"token": joe_smith_token}
    response = requests.get(f'{BASE_URL}/notifications/get/v1', params = notification_input).json()
    assert response == {'notifications': []}

    # Joe sends a message which tags himself, he should not get a notification
    message_send_input = {"token": joe_smith_token, "dm_id": joe_dm_data['dm_id'], "message": "Hi @joesmith!"}
    response = requests.post(f'{BASE_URL}/message/senddm/v1', json = message_send_input)
    assert response.status_code in [200, 201]

    # Ensure Joe has no notifications at the moment
    notification_input = {"token": joe_smith_token}
    response = requests.get(f'{BASE_URL}/notifications/get/v1', params = notification_input).json()
    assert response == {'notifications': []}

def test_sendlaterdm_notification(setup_dm):

    joe_smith_token, marry_mae_token, _, joe_dm_data = setup_dm

    # Ensure Joe has no notifications at the moment
    notification_input = {"token": joe_smith_token}
    response = requests.get(f'{BASE_URL}/notifications/get/v1', params = notification_input).json()
    assert response == {'notifications': []}

    # Marry sends a message for later
    message_later_time = int(datetime.now(timezone.utc).timestamp()) + 2
    message_send_input = {"token": marry_mae_token, "dm_id": joe_dm_data['dm_id'], "message": "Hi @joesmith!", "time_sent": message_later_time}
    response = requests.post(f'{BASE_URL}/message/sendlaterdm/v1', json = message_send_input)
    assert response.status_code in [200, 201]

    # Ensure Joe has no notifications at the moment
    notification_input = {"token": joe_smith_token}
    response = requests.get(f'{BASE_URL}/notifications/get/v1', params = notification_input).json()
    assert response == {'notifications': []}    

    time.sleep(3)

    # After the message_later_time Joe has one notification
    notification_input = {"token": joe_smith_token}
    response = requests.get(f'{BASE_URL}/notifications/get/v1', params = notification_input).json()
    assert response == {
        'notifications': [
            {
                'channel_id': -1,
                'dm_id': 0,
                'notification_message': "marrymae tagged you in darronmike, joesmith, marrymae: Hi @joesmith!"
            },
        ]
    }