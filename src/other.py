from src.data_store import data_store
from src.auth_auth_helpers import reset_session_tracker
from src.message import reset_message_id_tracker

def clear_v1():
    '''
    This function access all fields in the data structure from data_store
    and empties all of them to the original state at the beginning of the code.

    Arguements:
        N/A
    Exceptions:
        N/A
    Returns:
        Empty dictionary {} every time    
    '''

    reset_session_tracker()
    reset_message_id_tracker()

    store = data_store.get()
    
    store = {
        'logged_in_users': [],

        'users': {
            'user_id': [],
            'emails': [],
            'passwords': [],
            'first_names': [],
            'last_names': [],
            'user_handles': [],
            'is_global_owner':[],
            'removed_user': [],
            'permissions': [],
            'password_reset_code': [], 
            'notifications': [], 
            'channels_joined': [],   
            'dms_joined': [],
            'messages_sent': [],
            'channels_user_data': [],
            'dms_user_data': [],
            'messages_sent_user_data': [],
            'involvement_rate': [], 
            'profile_img_url': [],
        },

        'channels': {
            'channel_id': [],
            'channel_name': [],
            'owner_user_id': [],
            'is_public': [],
            'all_members': [],
            'messages': [],
            'is_standup_active': [],
            'standup_time_finish': [],
            'standup_messages': []
        },

        'messages': [],

        'dms': {
            'dm_id': [],
            'owner_user_id': [],
            'dm_name': [],
            'all_members': [],
            'messages': [],
        },

        'channels_exist': 0, 
        'dms_exist': 0,     
        'messages_exist': 0,   
        'workspace_stat_channels': [],
        'workspace_stat_dms': [],
        'workspace_stat_messages': [],
        'utilization_rate': 0
    }

    data_store.set(store)

    return 