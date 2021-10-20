from src.data_store import data_store

# Users functions


# List of all users
def user_all_v1(token):


    user_id = check_and_get_user_id(token)

    store = data_store.get()

    user = []

    for x in store['users']['u_id']:

        
        user.append({'u_id': owners, 'email': user_email, 'name_first': user_first_name, 'name_last': user_last_name, 'handle_str': user_handles})



    data_store.set(store)



    return {user}


# List of all valid users
def user_profile_v1(token, u_id):

    user_id = check_and_get_user_id(token)


    store = data_store.get()

    user = []

    for x in store['users']['u_id']:
        
        if u_id < len(store['users']['user_handles']):
            user.append({'u_id': owners, 'email': user_email, 'name_first': user_first_name, 'name_last': user_last_name, 'handle_str': user_handles})

    
    
    data_store.set(store)

    
    
    return {user}






# Update name
def user_profile_setname_v1(token, name_first, name_last):

    user_id = check_and_get_user_id(token)

    store = data_store.get()


    new_name = {'name_first': name_first, 'name_last': name_last}

    store['users']['u_id'].update(new_name)
    
    
    data_store.set(store)



    return {}




# Update email
def user_profile_setemail_v1(token, email):
    
    user_id = check_and_get_user_id(token)


    store = data_store.get()
    
    
    new_email = {'email': email}


    store['users']['u_id'].update(new_email)
    
    
    
    
    data_store.set(store)


    return {}



# Update handle
def user_profile_sethandle_v1(toke, handle_str):

    user_id = check_and_get_user_id(token)


    store = data_store.get()



    new_handle = {'handle_str': user_handles}


    store['users']['u_id'].update(new_handle)


    data_store.set(store)

    return {}



# Check Functions