from src.data_store import data_store
from src.error import InputError

import re

def auth_login_v1(email, password):
    return {
        'auth_user_id': 1,
    }

def auth_register_v1(email, password, name_first, name_last):

    



    return {
        'auth_user_id': 1,
    }

# def check(email):

#     regex = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$'

#     try:
#         re.fullmatch(regex, email)
#         return email
#     except Exception as e:





# Debugging purposes
#if __name__ == '__main__':
    