from src.data_store import data_store

def channels_list_v1(auth_user_id):
    new_list = {'channels':[]}

    store = data_store.get()
    i = 0
    for members in store['channels']['all_members']:
        name = store['channels']['name'][i]
        new_dict = { 'channel_id': i, 'name': name}

        if auth_user_id in members:
            new_list['channels'].append(new_dict)

        i += 1

    return new_list

def channels_listall_v1(auth_user_id):
    new_list = {'channels':[]}

    store = data_store.get()
    i = 0
    for name in store['channels']['name']:
        
        new_dict = {'channel_id': i, 'name': name}
        new_list['channels'].append(new_dict)

        i += 1

    return new_list

def channels_create_v1(auth_user_id, name, is_public):
    return {
        'channel_id': 1,
    }
