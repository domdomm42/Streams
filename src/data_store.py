'''
data_store.py

This contains a definition for a Datastore class which you should use to store your data.
You don't need to understand how it works at this point, just how to use it :)

The data_store variable is global, meaning that so long as you import it into any
python file in src, you can access its contents.

Example usage:

    from data_store import data_store

    store = data_store.get()
    print(store) # Prints { 'names': ['Nick', 'Emily', 'Hayden', 'Rob'] }

    names = store['names']

    names.remove('Rob')
    names.append('Jake')
    names.sort()

    print(store) # Prints { 'names': ['Emily', 'Hayden', 'Jake', 'Nick'] }
    data_store.set(store)
'''

## YOU SHOULD MODIFY THIS OBJECT BELOW
initial_object = {

    # The auth_user_id is the index of the user in the list
    'users': {
        'token': [],
        'user_id': [],
        'logged_in': [],
        'emails': [],
        'passwords': [],
        'first_names': [],
        'last_names': [],
        'user_handles': [],
        'is_global_owner': [],
    },


    # The channel_id is the index of the channel in the list
    # Make a list inside the list, for example for channel_id = 0,
    # the 0th index of all_members is a list of strings/numbers containing
    # all the members
    'channels': {
        'channel_id': [], #NEW
        'channel_name': [],
        'owner_user_id': [],
        'is_public': [],
        'all_members': [],
        'messages': []
    },

    # Contains the messages of all the channels and DMs
    'messages': {
        'message_id': [], #NEW
        'u_id': [],
        'message': [],
        'time_created': [],
        
    },

    # DMS // Group Chats
    'dms': {
        'dm_id': [], #NEW
        'owner_user_id': [],
        'dm_name': [],
        'all_members': [],
        'messages': [], 
    },

    #BY USING INDEX FOR THE ID, if we remove a message, all the messages after gets shifted to the left
    # WHICH IS BAD

    # dm_create, sending messages and creating user and creating channel will assign their ID,
    #which will be the ID of the last index + 1
}


## YOU SHOULD MODIFY THIS OBJECT ABOVE

class Datastore:
    def __init__(self):
        self.__store = initial_object

    def get(self):
        return self.__store

    def set(self, store):
        if not isinstance(store, dict):
            raise TypeError('store must be of type dictionary')
        self.__store = store

print('Loading Datastore...')

global data_store
data_store = Datastore()
