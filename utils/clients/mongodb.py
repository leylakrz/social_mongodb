from pymongo import MongoClient

from social.settings import MONGODB_HOST, MONGODB_DATABASE, MONGODB_PASSWORD, MONGODB_USERNAME, MONGODB_PORT


def get_mongo_client():
    if MONGODB_USERNAME and MONGODB_PASSWORD:
        client = MongoClient(
            f'mongodb://{MONGODB_USERNAME}:{MONGODB_PASSWORD}@{MONGODB_HOST}:{MONGODB_PORT}/')
    else:
        client = MongoClient(
            f'mongodb://{MONGODB_HOST}:{MONGODB_PORT}/')
    if MONGODB_DATABASE:
        return client[MONGODB_DATABASE]
    else:
        return client


def get_collection(collection_name: str):
    return get_mongo_client()[collection_name]
