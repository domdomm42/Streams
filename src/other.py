from src.data_store import data_store

def clear_v1():
    data = data_store.get()
    data['users'] = []
    data['emails'] = []
    data['passwords'] = []
    data['first_names'] = []
    data['last_names'] = []
    data['user_handles'] = []
    data_store.set(data)
