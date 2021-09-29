import pytest
from src.data_store import data_store


def channel_invite_v1(auth_user_id, channel_id, u_id):
    store = data_store.get()
    # Check
    check_invalid_channel_id(channel_id)
    check_invalid_u_id(u_id)
    check_member_u_id(channel_id, u_id)

    check_autorised_id(u_id)

    # Store

    #store['channels']['owner_user_id'].append(auth_user_id)
    #store['channels']['u_id'].append(u_id)

    store['channels']['all_members'][channel_id].append(u_id)


    data_store.set(store)
    return {

    }


# store['channels']['channel_id']['name'],
#
#
# all_members.append(auth_user_id)

def channel_details_v1(auth_user_id, channel_id):
    return {
        'name': 'Hayden',
        'owner_members': [
            {
                'u_id': 1,
                'email': 'example@gmail.com',
                'name_first': 'Hayden',
                'name_last': 'Jacobs',
                'handle_str': 'haydenjacobs',
            }
        ],
        'all_members': [
            {
                'u_id': 1,
                'email': 'example@gmail.com',
                'name_first': 'Hayden',
                'name_last': 'Jacobs',
                #'handle_str': 'haydenjacobs', store = data_store.get()
    }
    ],
    }

    def channel_messages_v1(auth_user_id, channel_id, start):

        store = data_store.get()
        # Check
        check_invalid_channel_id(channel_id)
        check_invalid_start(channel_id, start)

        check_autorised_id(u_id)

        # Loop
        messages_list = []
        place = start
        for message in intial_object['channels']['messages'][0]:
            messages_list.append(message)
            place += 1
            if place == 50:
                break
        if place < 50:
            place = -1

        return {
            'message': message,
            'start': start,
            'end': place
        }

    def channel_join_v1(auth_user_id, channel_id):
        return {
        }

    # InputError
    # Check invalid channel_id
    def check_invalid_channel_id(channel_id):
        if store['channels'].has_key(channel_id) == True:
            pass
        else:
            raise InputError('Invalid channel id')

    # Check invalid u_id
    def check_invalid_u_id(u_id):
        if store['channels'].has_key(u_id) == True:
            pass
        else:
            raise InputError('Invalid u id')

    # Check member u_id
    def check_member_u_id(channel_id, u_id):
        if (u_id in channel_id.values()) == True:
            pass
        else:
            raise InputError('Permission dinined!')

    # Check start
    def check_invalid_start(channel_id, start):
        if start <= len(['channel_id']['messages']):
            pass
        else:
            raise InputError('Permission dinined!')

    # AccessError
    # Check authorised
    def check_autorised_id(u_id):
        if u_id in channels.values() == True:
            pass
        else:
            raise AccessError('Permission dinined!')

