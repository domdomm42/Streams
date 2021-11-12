import pytest
import requests
from src.config import *
from src.auth_auth_helpers import SECRET


from datetime import datetime, timezone
BASE_URL = url

INPUTERROR = 400
ACCESSERROR = 403

@pytest.fixture
def setup():
    requests.delete(f'{BASE_URL}/clear/v1')

    #Create User Joe
    user_info = {'email': 'joe123@gmail.com', 'password': 'password', 'name_first': 'Joe', 'name_last': 'Smith'}
    joe_token = {'token': requests.post(f'{BASE_URL}/auth/register/v2', json = user_info).json()['token']}
    #Create User Marry
    user_info = {'email': 'marry123@gmail.com', 'password': 'password', 'name_first': 'Marry', 'name_last': 'Smith'}
    marry_token = {'token': requests.post(f'{BASE_URL}/auth/register/v2', json = user_info).json()['token']}
    #Create user Sam
    user_info = {'email': 'sam123@gmail.com', 'password': 'password', 'name_first': 'Sam', 'name_last': 'Smith'}
    sam_token = {'token': requests.post(f'{BASE_URL}/auth/register/v2', json = user_info).json()['token']}

    # Create a DM by Joe that include mary
    dm1_info = {'token': joe_token['token'], 'u_ids': [1]}
    dm1_id = {'dm_id': requests.post(f'{BASE_URL}/dm/create/v1', json = dm1_info).json()['dm_id']}

    return dm1_id['dm_id'], joe_token['token'], marry_token['token'], sam_token['token']


'''
INVALIDITY TESTS FOR DM_CREATE
'''

def test_dm_create_invalid_token():
    requests.delete(f'{BASE_URL}/clear/v1')

    # Tests a nonexistant user trying to access the function 
    u_ids = [0, 1, 2]
    dm_creation = {"token": '-1', "u_ids": u_ids}
    response_create = requests.post(f'{BASE_URL}/dm/create/v1', json = dm_creation)
    response_create_data = response_create.json()
    assert response_create_data['code'] == ACCESSERROR

def test_dm_create_invalid_list():
    requests.delete(f'{BASE_URL}/clear/v1')
    user_info = {'email': 'joe123@gmail.com', 'password': 'password', 'name_first': 'Joe', 'name_last': 'Smith'}
    joe_token = {'token': requests.post(f'{BASE_URL}/auth/register/v2', json = user_info).json()['token']}

    # Uses a list of users that do no exist to prompt input error
    u_ids = [0, 1, 2]
    dm_creation = {"token": joe_token['token'], "u_ids": u_ids}
    response_create = requests.post(f'{BASE_URL}/dm/create/v1', json = dm_creation)
    response_create_data = response_create.json()
    assert response_create_data['code'] == INPUTERROR

'''
INVALIDITY TESTS FOR DM_LIST
'''

def test_dm_list_invalid_token():
    requests.delete(f'{BASE_URL}/clear/v1')

    # Tests a nonexistant user trying to access the function 
    dm_list = {"token": '-1'}
    response_create = requests.get(f'{BASE_URL}/dm/list/v1', params = dm_list)
    response_create_data = response_create.json()
    assert response_create_data['code'] == ACCESSERROR


'''
INVALIDITY TESTS FOR DM_REMOVE
'''

def test_dm_remove_invalid_token():
    requests.delete(f'{BASE_URL}/clear/v1')

    # Tests a nonexistant user trying to access the function, raising AccessError if not 
    dm_remove = {"token": '-1', "dm_id": 1}
    response_create = requests.delete(f'{BASE_URL}/dm/remove/v1', json = dm_remove)
    response_create_data = response_create.json()
    assert response_create_data['code'] == ACCESSERROR

def test_dm_invalid_dm_id(setup):
    _, joe, _, _ = setup

    # Tests a nonexistant dm trying to get removed, raising InputError if not 
    dm_remove = {"token": joe, "dm_id": 1}
    response_create = requests.delete(f'{BASE_URL}/dm/remove/v1', json = dm_remove)
    response_create_data = response_create.json()
    assert response_create_data['code'] == INPUTERROR

def test_dm_unoriginal_owner(setup):
    dm_id, _, marry, _ = setup

    # Tests if an unauthorused user can remove a function, raising AccessError if not
    dm_remove = {'token': marry, 'dm_id': dm_id}
    response_create = requests.delete(f'{BASE_URL}/dm/remove/v1', json = dm_remove)
    response_create_data = response_create.json()
    assert response_create_data['code'] == ACCESSERROR

'''
INVALIDITY TEST FOR DM_DETAILS
'''
def test_details_invalid_dm(setup):
    _, joe, _, _ = setup

    # Tests a nonexistant dm trying to get info from, raising InputError if unable to
    dm_details = {"token": joe, "dm_id": 1}
    response_create = requests.get(f'{BASE_URL}/dm/details/v1', params = dm_details)
    response_create_data = response_create.json()
    assert response_create_data['code'] == INPUTERROR

def test_details_invalid_token():
    requests.delete(f'{BASE_URL}/clear/v1')

    # Tests a nonexistant user trying to access the function, raising AccessError if unable 
    dm_details = {"token": '-1', "dm_id": 1}
    response_create = requests.get(f'{BASE_URL}/dm/details/v1', params = dm_details)
    response_create_data = response_create.json()
    assert response_create_data['code'] == ACCESSERROR

def test_details_not_member(setup):
    _, _, _, sam = setup

    # Tests if an unauthorised user (person who is not member of dm) can access the function, raising AccessError if not
    dm_details = {"token": sam, "dm_id": 0}
    response_create = requests.get(f'{BASE_URL}/dm/details/v1', params = dm_details)
    response_create_data = response_create.json()
    assert response_create_data['code'] == ACCESSERROR

'''
INVALIDITY TESTS FOR DM_LEAVE
'''
def test_leave_invalid_dm(setup):
    _, joe, _, _ = setup

    # Tests a nonexistant dm trying to get left from, raising InputError if unable to
    dm_leave = {"token": joe, "dm_id": 1}
    response_create = requests.post(f'{BASE_URL}/dm/leave/v1', json = dm_leave)
    response_create_data = response_create.json()
    assert response_create_data['code'] == INPUTERROR

def test_leave_invalid_token():
    requests.delete(f'{BASE_URL}/clear/v1')

    # Tests a nonexistant user trying to access the function, raising AccessError if unable
    dm_leave = {"token": '-1', "dm_id": 1}
    response_create = requests.post(f'{BASE_URL}/dm/leave/v1', json = dm_leave)
    response_create_data = response_create.json()
    assert response_create_data['code'] == ACCESSERROR

def test_leave_not_member(setup):
    _, _, _, sam = setup

    # Tests if an unauthorised user (person who is not member of dm) can access the function, raising AccessError if not
    dm_leave = {"token": sam, "dm_id": 0}
    response_create = requests.post(f'{BASE_URL}/dm/leave/v1', json = dm_leave)
    response_create_data = response_create.json()
    assert response_create_data['code'] == ACCESSERROR

'''
INVALIDITY TESTS FOR DM_MESSAGES
'''

def test_messages_invalid_dm_id(setup):
    _, joe, _, _ = setup

    # Tests if a nonexistent dm is being called, raises InputError if so
    dm_messages = {"token": joe, "dm_id": 1, 'start': 0}
    response_create = requests.get(f'{BASE_URL}/dm/messages/v1', params = dm_messages)
    response_create_data = response_create.json()
    assert response_create_data['code'] == INPUTERROR

def test_messages_invalid_token():
    requests.delete(f'{BASE_URL}/clear/v1')

    # Tests a nonexistant user trying to access the function, raising AccessError if unable
    dm_messages = {"token": '-1', "dm_id": 1, 'start': 0}
    response_create = requests.get(f'{BASE_URL}/dm/messages/v1', params = dm_messages)
    response_create_data = response_create.json()
    assert response_create_data['code'] == ACCESSERROR

def test_messages_invalid_start(setup):
    _, joe, _, _ = setup

    # Tests if start is greater than the number of messages in the dm (here being 0 messages)
    dm_messages = {"token": joe, "dm_id": 0, 'start': 5}
    response_create = requests.get(f'{BASE_URL}/dm/messages/v1', params = dm_messages)
    response_create_data = response_create.json()
    assert response_create_data['code'] == INPUTERROR

def test_messages_not_member(setup):
    _, _, _, sam = setup

    # Tests if an unauthorised user (person who is not member of dm) can access the function, raising AccessError if not
    dm_messages = {"token": sam, "dm_id": 0, 'start': 0}
    response_create = requests.get(f'{BASE_URL}/dm/messages/v1', params = dm_messages)
    response_create_data = response_create.json()
    assert response_create_data['code'] == ACCESSERROR

'''
INVALIDITY TESTS FOR MESSAGE REACT & UNREACT
'''
def test_react_invalid_token():
    requests.delete(f'{BASE_URL}/clear/v1')

    # Tests a nonexistant user trying to access the function, raising AccessError if unable
    dm_react = {"token": '-1', "message_id": 1, 'react_id': 1}
    response_create = requests.get(f'{BASE_URL}/message/react/v1', params = dm_react)
    response_create_data = response_create.json()
    assert response_create_data['code'] == ACCESSERROR

def test_unreact_invalid_token():
    requests.delete(f'{BASE_URL}/clear/v1')

    # Tests a nonexistant user trying to access the function, raising AccessError if unable
    dm_unreact = {"token": '-1', "message_id": 1, 'react_id': 1}
    response_create = requests.get(f'{BASE_URL}/message/unreact/v1', params = dm_unreact)
    response_create_data = response_create.json()
    assert response_create_data['code'] == ACCESSERROR

def test_unreact_invalid_message_id(setup):
    _, joe, _, _ = setup

    # Tests react where the message does not exist
    dm_react = {"token": joe, "message_id": 1, "react_id": 1}
    response_create = requests.get(f'{BASE_URL}/message/react/v1', params = dm_react)
    response_create_data = response_create.json()
    assert response_create_data['code'] == INPUTERROR

def test_invalid_message_id_unreact(setup):
    _, joe, _, _ = setup

    # Tests unreact where the message does not exist
    dm_unreact = {"token": joe, "message_id": 1, "react_id": 1}
    response_create = requests.get(f'{BASE_URL}/message/unreact/v1', params = dm_unreact)
    response_create_data = response_create.json()
    assert response_create_data['code'] == INPUTERROR

def test_invalid_react_id_react(setup):
    _, joe, _, _ = setup

    # Tests a react id that does not exist
    dm_react = {"token": joe, "message_id": 1, "react_id": 2}
    response_create = requests.get(f'{BASE_URL}/message/react/v1', params = dm_react)
    response_create_data = response_create.json()
    assert response_create_data['code'] == INPUTERROR

def test_invalid_react_id_unreact(setup):
    _, joe, _, _ = setup

    # Tests a react id that does not exist
    dm_unreact = {"token": joe, "message_id": 1, "react_id": 2}
    response_create = requests.get(f'{BASE_URL}/message/unreact/v1', params = dm_unreact)
    response_create_data = response_create.json()
    assert response_create_data['code'] == INPUTERROR

def test_invalid_react(setup):
    dm1, joe, _, _ = setup

    # Tests if a message can be reacted twice
    dm_message = {'token': joe, 'dm_id': dm1, 'message': 'big'}
    response_create = requests.get(f'{BASE_URL}/message/senddm/v1', params = dm_message).json()

    dm_react = {"token": joe, "message_id": response_create, "react_id": 1}
    requests.get(f'{BASE_URL}/message/react/v1', params = dm_react)
    
    dm_react = {"token": joe, "message_id": response_create, "react_id": 1}
    response_create = requests.get(f'{BASE_URL}/message/react/v1', params = dm_react).json()
    assert response_create['code'] == INPUTERROR

def test_invalid_unreact(setup):
    dm1, joe, _, _ = setup

    # Tests if a message that has no react can be unreacted
    dm_message = {'token': joe, 'dm_id': dm1, 'message': 'big'}
    response_create = requests.get(f'{BASE_URL}/message/senddm/v1', params = dm_message).json()
    
    dm_unreact = {"token": joe, "message_id": response_create, "react_id": 1}
    response_create = requests.get(f'{BASE_URL}/message/unreact/v1', params = dm_unreact).json()
    assert response_create['code'] == INPUTERROR
'''
INVALIDITY TESTS FOR MESSAGE PIN & UNPIN
'''
def test_pin_invalid_token():
    requests.delete(f'{BASE_URL}/clear/v1')

    # Tests a nonexistant user trying to access the function, raising AccessError if unable
    dm_pin = {"token": '-1', "message_id": 1}
    response_create = requests.get(f'{BASE_URL}/message/pin/v1', params = dm_pin)
    response_create_data = response_create.json()
    assert response_create_data['code'] == ACCESSERROR

def test_pin_invalid_token():
    requests.delete(f'{BASE_URL}/clear/v1')

    # Tests a nonexistant user trying to access the function, raising AccessError if unable
    dm_unpin = {"token": '-1', "message_id": 1}
    response_create = requests.get(f'{BASE_URL}/message/unpin/v1', params = dm_unpin)
    response_create_data = response_create.json()
    assert response_create_data['code'] == ACCESSERROR

def test_pin_invalid_message_id(setup):
    _, joe, _, _ = setup

    # Tests pin where a message does no exist
    dm_pin = {"token": joe, "message_id": 1}
    response_create = requests.get(f'{BASE_URL}/message/pin/v1', params = dm_pin)
    response_create_data = response_create.json()
    assert response_create_data['code'] == INPUTERROR

def test_unpin_invalid_message_id(setup):
    _, joe, _, _ = setup

    # Tests unpin where a message does no exist
    dm_unpin = {"token": joe, "message_id": 1}
    response_create = requests.get(f'{BASE_URL}/message/unpin/v1', params = dm_unpin)
    response_create_data = response_create.json()
    assert response_create_data['code'] == INPUTERROR    

def test_pin_not_owner(setup):
    dm1, joe, marry, _ = setup

    # Tests a message pin where the caller is not the owner of the dm/channel
    dm_message = {'token': joe, 'dm_id': dm1, 'message': 'big'}
    response_create = requests.get(f'{BASE_URL}/message/senddm/v1', params = dm_message).json()

    dm_pin = {"token": marry, "message_id": response_create}
    response_create = requests.get(f'{BASE_URL}/message/pin/v1', params = dm_pin)
    response_create_data = response_create.json()
    assert response_create_data['code'] == ACCESSERROR 

def test_unpin_not_owner(setup):
    dm1, joe, marry, _ = setup

    # Tests a message pin where the caller is not the owner of the dm/channel
    dm_message = {'token': joe, 'dm_id': dm1, 'message': 'big'}
    response_create = requests.get(f'{BASE_URL}/message/senddm/v1', params = dm_message).json()

    dm_unpin = {"token": marry, "message_id": response_create}
    response_create = requests.get(f'{BASE_URL}/message/unpin/v1', params = dm_unpin)
    response_create_data = response_create.json()
    assert response_create_data['code'] == ACCESSERROR

def test_already_pinned(setup):
    dm1, joe, _, _ = setup

    # Tests a message that is pinned raising inputerror
    dm_message = {'token': joe, 'dm_id': dm1, 'message': 'big'}
    response_create = requests.get(f'{BASE_URL}/message/senddm/v1', params = dm_message).json()

    dm_pin = {"token": joe, "message_id": response_create}
    response_create = requests.get(f'{BASE_URL}/message/pin/v1', params = dm_pin)

    dm_pin = {"token": joe, "message_id": response_create}
    response_create = requests.get(f'{BASE_URL}/message/pin/v1', params = dm_pin).json()
    assert response_create['code'] == INPUTERROR

def test_already_unpinned(setup):
    dm1, joe, _, _ = setup

    # Tests a message that has no pin raising inputerror
    dm_message = {'token': joe, 'dm_id': dm1, 'message': 'big'}
    response_create = requests.get(f'{BASE_URL}/message/senddm/v1', params = dm_message).json()

    dm_unpin = {"token": joe, "message_id": response_create}
    response_create = requests.get(f'{BASE_URL}/message/unpin/v1', params = dm_unpin)
    response_create_data = response_create.json()
    assert response_create_data['code'] == INPUTERROR

'''
INVALIDITY TESTS FOR SEARCH
'''

def test_invalid_token_search():
    requests.delete(f'{BASE_URL}/clear/v1')

    # Tests a nonexistant user trying to access the function, raising AccessError if unable
    search = {"token": '-1', "query_str": "big"}
    response_create = requests.get(f'{BASE_URL}/search/v1', params = search)
    response_create_data = response_create.json()
    assert response_create_data['code'] == ACCESSERROR

def test_short_string_search(setup):
    _, joe, _, _ = setup

    # Tests an empty query string
    search = {"token": joe, "query_str": ""}
    response_create = requests.get(f'{BASE_URL}/search/v1', params = search)
    response_create_data = response_create.json()
    assert response_create_data['code'] == INPUTERROR

def test_long_string_search(setup):
    _, joe, _, _ = setup
    string = 'bigbigbigbigbigbig' * 10

    # Tests a 1000+ character string 
    search = {"token": joe, "query_str": string}
    response_create = requests.get(f'{BASE_URL}/search/v1', params = search)
    response_create_data = response_create.json()
    assert response_create_data['code'] == INPUTERROR

'''
SAMPLE TESTING FOR DM_CREATE
'''

def test_simple_dm_create(setup):

    # Tests a single call of the create file from setup
    dm1, _, _, _= setup
    assert dm1 == 0

def test_multiple_dm_create(setup):
    dm1, _, marry, _= setup
    # Creates two concurrent dm's and their returned values
    dm1_info = {'token': marry, 'u_ids': [0, 1]}
    dm2 = {'dm_id': requests.post(f'{BASE_URL}/dm/create/v1', json = dm1_info).json()['dm_id']}
    assert dm1 == 0  
    assert dm2['dm_id'] == 1

'''
SAMPLE TESTING FOR DM_LIST
'''    
def test_simple_dm_list(setup):
    _, joe, _, _ = setup

    # Tests a single call of the list function of one present dm
    dm_list = {"token": joe}
    response_create = requests.get(f'{BASE_URL}/dm/list/v1', params = dm_list)
    response_create_data = response_create.json()
    assert response_create_data['dms'] == [
        {'dm_id': 0, 'name': 'joesmith, marrysmith'}
    ]

'''
SAMPLE TESTING FOR DM_REMOVE
''' 
def test_simple_dm_remove(setup):
    _, joe, marry, _ = setup

    # Uses list function to identify if dm created in setup was removed
    dm_remove = {'token': joe, 'dm_id': 0}
    response_create = requests.delete(f'{BASE_URL}/dm/remove/v1', json = dm_remove)

    dm_list = {"token": marry}
    response_create = requests.get(f'{BASE_URL}/dm/list/v1', params = dm_list)
    response_create_data = response_create.json()
    assert response_create_data['dms'] == []

def test_multple_dm_remove(setup):
    _, joe, marry, _ = setup

    # Uses list function to identify if dm created in setup was removed
    dm_remove = {'token': joe, 'dm_id': 0}
    response_create = requests.delete(f'{BASE_URL}/dm/remove/v1', json = dm_remove)

    dm_list = {"token": marry}
    response_create = requests.get(f'{BASE_URL}/dm/list/v1', params = dm_list)
    response_create_data = response_create.json()
    assert response_create_data['dms'] == []
'''
SAMPLE TESTING FOR DM_DETAILS
'''
def test_simple_dm_details(setup):
    _, joe, _, _ = setup

    # Tests a single call of the details function of one present dm
    dm_details = {"token": joe, "dm_id": 0}
    response_create = requests.get(f'{BASE_URL}/dm/details/v1', params = dm_details)
    response_create_data = response_create.json()
    assert response_create_data['name'] == 'joesmith, marrysmith' 
    assert response_create_data['members'] == [
        {
            'u_id': 1,
            'email': 'marry123@gmail.com',
            'name_first': 'Marry', 
            'name_last': 'Smith',
            'handle_str': 'marrysmith'
        },
        {
            'u_id': 0,
            'email': 'joe123@gmail.com',
            'name_first': 'Joe', 
            'name_last': 'Smith',
            'handle_str':  'joesmith'
        }
    ]
'''
SAMPLE TESTING FOR DM_LEAVE
'''

def test_simple_dm_leave(setup):
    _, joe, marry, _ = setup

    # Tests a single call of the leave function for the owner of the dm joe
    dm_leave = {"token": joe, "dm_id": 0}
    requests.post(f'{BASE_URL}/dm/leave/v1', json = dm_leave)
    
    # As marry is the only remaining member, details should only show her but keep the same dm name 
    dm_details = {"token": marry, "dm_id": 0}
    response_create = requests.get(f'{BASE_URL}/dm/details/v1', params = dm_details)
    response_create_data = response_create.json()
    assert response_create_data['name'] == 'joesmith, marrysmith' 
    assert response_create_data['members'] == [
        {
            'u_id': 1,
            'email': 'marry123@gmail.com',
            'name_first': 'Marry', 
            'name_last': 'Smith',
            'handle_str': 'marrysmith'
        }
    ]

def test_multiple_dm_leave(setup):
    _, joe, marry, _ = setup

    # Tests two calls of the leave function for the owner of the dm joe and marry
    dm_leave = {"token": joe, "dm_id": 0}
    response_create = requests.post(f'{BASE_URL}/dm/leave/v1', json = dm_leave)
    response_create_data = response_create.json()
    
    dm_leave = {"token": marry, "dm_id": 0}
    response_create = requests.post(f'{BASE_URL}/dm/leave/v1', json = dm_leave)
    response_create_data = response_create.json()
    # As marry is the only remaining member she cannot access the dm 
    dm_details = {"token": marry, "dm_id": 0}
    response_create = requests.get(f'{BASE_URL}/dm/details/v1', params = dm_details)
    response_create_data = response_create.json()
    
    assert response_create_data['code'] == ACCESSERROR

'''
SAMPLE TESTING FOR DM_MESSAGES
'''

def test_simple_dm_messages(setup):
    _, joe, marry, _ = setup

    # sends two messages from joe and marry
    send_dm1 = {'token': joe, 'dm_id': 0, 'message': 'big tings bruv'}
    send_dm2 = {'token': marry, 'dm_id': 0, 'message': 'small tings bruv'}

    # records the time and id of each message sent
    response_create = requests.post(f'{BASE_URL}/message/senddm/v1', json = send_dm1)
    timestamp1 = int(datetime.now(timezone.utc).timestamp())
    message_id1 = response_create.json()['message_id']
    
    response_create = requests.post(f'{BASE_URL}/message/senddm/v1', json = send_dm2)
    timestamp2 = int(datetime.now(timezone.utc).timestamp())
    message_id2 = response_create.json()['message_id']
   
    # Calls the messages function a single time with correct variables
    dm_messages = {"token": joe, "dm_id": 0, 'start': 0}
    response_create = requests.get(f'{BASE_URL}/dm/messages/v1', params = dm_messages)
    response_create_data = response_create.json()

    assert response_create_data['start'] == 0
    assert response_create_data['end'] == -1
    assert response_create_data['messages'] == [
        {
            'message_id': message_id2,
            'u_id': 1,
            'message': 'small tings bruv',
            'time_created': timestamp1,
            'reacts': {
                'react_id': 1,
                'u_ids': [],
                'is_this_user_reacted': False
            },
            'is_pinned': False
        },
        {
            'message_id': message_id1,
            'u_id': 0,
            'message': 'big tings bruv',
            'time_created': timestamp2,
            'reacts': {
                'react_id': 1,
                'u_ids': [],
                'is_this_user_reacted': False
            },
            'is_pinned': False
        } 
    ]

def test_multiple_dm_messages(setup):
    _, joe, _, _ = setup
    i = 0
    while i < 55:
        # sends messages from joe to dm_1
        send_dm1 = {'token': joe, 'dm_id': 0, 'message': 'big'}
        print(requests.post(f'{BASE_URL}/message/senddm/v1', json = send_dm1).json())

        i += 1
     # Calls the messages function a single time with correct variables
    dm_messages = {"token": joe, "dm_id": 0, 'start': 0}
    response_create = requests.get(f'{BASE_URL}/dm/messages/v1', params = dm_messages)
    response_create_data = response_create.json()
    
    assert response_create_data['start'] == 0
    assert response_create_data['end'] == 50   










