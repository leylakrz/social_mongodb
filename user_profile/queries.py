from utils.clients.mongodb import get_collection

user_profile_collection_name = "user_profile"


def check_user_name_exists(user_name):
    return get_collection(user_profile_collection_name).find_one({"user_name": user_name}) is not None

def create_user(user_name):
    return get_collection(user_profile_collection_name).insert_one({"user_name": user_name})