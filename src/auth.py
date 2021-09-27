from src.data_store import data_store
from src.error import InputError

import re

def auth_login_v1(email, password):

    if check_valid_email(email) == 1 and check_valid_password(password) == 1:

        for x in store["users"]["emails"]:
            email_list.append(x)

        for y in store["users"]["user_handles"]:
            user_handles_list.append(y)

        for idx in email_list:
            if email == email_list[idx]:
                break
            else:
                counter = counter + 1
    
        counter = counter + 1

        return user_handles_list[counter]

    else:
        raise InputError('Wrong email and/or password!')


def auth_register_v1(email, password, name_first, name_last):

    store = data_store.get()

    # Check all inputs
    check_email(email)
    check_password(password)
    check_first_name(name_first)
    check_last_name(name_last)

    # Store all the data
    store['users']['emails'].append(email)
    store['users']['passwords'].append(password)
    store['users']['first_names'].append(name_first)
    store['users']['last_names'].append(name_last)

    data_store.set(store)

    # Create user_handle and store in data_store, return auth_user_id
    # NOTE: auth_user_id is the index of the user in the list
    auth_user_id = create_user_handle(name_first, name_last)

    return auth_user_id


# --- Check email ---
# This function takes in an email (string) and checks if email is
# in the correct format and unique
# This function returns a unique user_handle
def check_email(email):

    store = data_store.get()

    regex = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$'

    print(store['users']['emails'])

    if re.fullmatch(regex, email) and email not in store['users']['emails']:
        pass
    else:
        raise InputError('Invalid email!')

# --- Check password ---
# This function takes in a password (string) and checks if the 
# password is >= 6 characters
# This function does not return anything
def check_password(password):
    if len(password) >= 6:
        pass
    else: 
        raise InputError('Invalid password!')

# --- Check first name ---
# This function takes in the user's first name (string) and checks 
# if the first name is between 1 and 50 characters inclusive
# This function does not return anything
def check_first_name(name_first):
    if len(name_first) >= 1 and len(name_first) <= 50:
        pass
    else: 
        raise InputError('Invalid first name!')

# --- Check last name ---
# This function takes in the user's last name (string) and checks 
# if the last name is between 1 and 50 characters inclusive
# This function does not return anything
def check_last_name(name_last):
    if len(name_last) >= 1 and len(name_last) <= 50:
        pass
    else:
        raise Exception('Invalid last name!')

# --- Create user_handle ---
# This function takes in the user's first and last name (strings)
# and creates a unique user_handle (string)
# This function returns the auth_user_id (int)
def create_user_handle(name_first, name_last):

    user_handle = (name_first.lower() + name_last.lower())[0:19]

    # Obtain data
    store = data_store.get()
    
    # Check if the user_handle is unique,
    # If user_handle is not unique, then the function will add
    # a number at the end of the function
    user_handle_copy = user_handle
    i = 1
    while user_handle in store['users']['user_handles']:
        user_handle = user_handle_copy + str(i)
        i += 1
    
    store['users']['user_handles'].append(user_handle)
    auth_user_id = store['users']['user_handles'].index(user_handle)

    data_store.set(store)

    #print(store)
    return auth_user_id

# --- Checks if email is registered ---
# This function takes in an email and checks if
# email used to log in is registed. If email
# is not stored, return error.

def check_valid_email(email):

    store = data_store.get()
    email_list = []
    check = 0

    # Loops through registered email and adds it to a list.
    for x in store["users"]["emails"]:
        email_list.append(x)

    # Checks if list contains the email given
    # If email is in the list, a 1 is given
    # If the loop reaches the end and the email isn't present
    # The 'check' stays at 0.
    for y in email_list:
        if y == email:
            check = 1
        else:
            pass
    
    if check != 1:
        raise InputError('Email not registered!')

# --- Checks if password matches registered email ---
# This function takes in password and check if 
# password matches the registered email, if it doesn't, return
# Error.

def check_valid_password(email, password):
    email_list = []
    password_list = []
    check = 0

    # Loops through registered email and adds it
    # to the list.
    for x in store["users"]["emails"]:
        email_list.append(x)

    # Loops through stored password and adds it
    # to the list.
    for y in store["users"]["passwords"]:
        password_list.append(y)

    # Finds the index of the email,
    for idx in email_list:
        if email == email_list[idx]:
            break
        else:
            counter = counter + 1
    
    # 1 is added as for loop stops prematurely.
    counter = counter + 1

    # As password has the same index as email
    # password_list[counter] gives us the password(if correct).
    if password == password_list[counter]:
        return 1
    else:
        raise InputError('Invalid Password!')
        

# Debugging + Testing purposes
if __name__ == '__main__':

    # Testing
    # auth_register_v1('joe123@gmail.com', 'password', 'Joe', 'Smith')
    # auth_register_v1('joe1233@gmail.com', 'password', 'Joe', 'Smith')


    # Testing create_user_handle works correctly for people with the same name
    # create_user_handle('Joe', 'Jimsfkjhydsyfdysfdyhs')
    # create_user_handle('Joe', 'Jimsfkjhydsyfdysfdyhs')
    # create_user_handle('Joe', 'Jimsfkjhydsyfdysfdyhs')
    # create_user_handle('Joe', 'Jimsfkjhydsyfdysfdyhs')
    pass
    