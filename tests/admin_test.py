import pytest
import requests
import jwt
from src.auth import auth_login_v1, auth_register_v1, auth_logout_v1
from src.error import InputError, AccessError
from src.other import clear_v1
from src.config import *
from src.auth_auth_helpers import SECRET
from src.data_store import *
from src.admin import *

BASE_URL = url

def test_simple_user_delete():
    auth_register_v1('domdomdom14@gmail.com', 'passwordDD', 'Oudom', 'Lim')
    auth_register_v1('domdomdom14@gmail.com', 'passwordDD', 'Oudom', 'Lim')

