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
        'emails': [],
        'passwords': [],
        'first_names': [],
        'last_names': [],
        'user_handles': [],
    },
    
    # The channel_id is the index of the channel in the list
    # Make a list inside the list, for example for channel_id = 0,
    # the 0th index of all_members is a list of strings/numbers containing
    # all the members
    'channels': [
        {
            'channel_id':[]
            'name':[]
            'owner_members':[
                {
                    'emails': [],
                    'passwords': [],
                    'first_names': [],
                    'last_names': [],
                    'user_handles': [] 
                }
            ]
            'all_members':[
                {
                    'emails': [],
                    'passwords': [],
                    'first_names': [],
                    'last_names': [],
                    'user_handles': []
                }
            ]
            'message':[
                {
                    'message_id':[]
                    'user_id':[]
                    'message':[]
                    'time_created':[]
                }
            ]

        }
    ]
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

