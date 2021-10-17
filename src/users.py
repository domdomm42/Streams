

# Users functions


# List of all users
@APP.route("/users/all/v1", methods=['GET'])
def user_all_v1(token):

    store = data_store.get()

    user = []

    for x in token:

        
        user.append({'u_id': owners, 'email': user_email, 'name_first': user_first_name, 'name_last': user_last_name, 'handle_str': user_handles})



    data_store.set(store)



    return dumps{user}


# List of all valid users
@APP.route("/users/profile/v1", methods=['GET'])
def user_profile_v1(token, u_id):

    store = data_store.get()

    user = []

    for x in ['channels']['all_members']
        
        if u_id >= len(store['users']['user_handles']):
            user.append({'u_id': owners, 'email': user_email, 'name_first': user_first_name, 'name_last': user_last_name, 'handle_str': user_handles})

    
    
    data_store.set(store)

    
    
    return dumps{user}






# Update name
@APP.route("/users/profile/setname/v1", methods=['PUT'])
def user_profile_setname_v1(token, name_first, name_last):

    store = data_store.get()


    new_name = {'name_first': name_first, 'name_last': name_last}

    token[users].update(new_name)
    
    
    data_store.set(store)



    return {}




# Update email
@APP.route("/users/profile/setemail/v1", methods=['PUT'])
def user_profile_setemail_v1(token, email):
    
    store = data_store.get()
    
    
    new_email = {'email': email}


    token[users].update(new_email)
    
    
    
    
    data_store.set(store)


    return {}



# Update handle
@APP.route("/users/profile/sethandle/v1", methods=['PUT'])
def user_profile_sethandle_v1(toke, handle_str):

    store = data_store.get()



    new_handle = {'handle_str': user_handles}


    token[users].update(new_handle)











    # del {​'user_id': user_id, 'session_id': session_id}​ in store['logged_in_users']

    # store['logged_in_users'].remove({​'user_id': user_id, 'session_id': session_id}​)


    data_store.set(store)

    return {}









# IT2


@APP.route("/channel/leave/v1", methods=['POST'])
def channel_leave_v1(token, channel_id):
    
    del token['channels']['all_members'][channel_id]
    
    
    return {}
