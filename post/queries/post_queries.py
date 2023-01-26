from datetime import datetime
from typing import Union

import pymongo
from bson import ObjectId

from utils.clients.mongodb import get_collection
from utils.decorators import invalid_id_handler

post_collection_name = "post"


@invalid_id_handler
def list_post(last_show_id: Union[None, str] = None, user_name: Union[None, str] = None):
    filter_clause = {}
    if last_show_id:
        filter_clause["_id"] = {"$lt": ObjectId(last_show_id), }
    if user_name:
        filter_clause["user_name"] = user_name

    cursor = get_collection(post_collection_name).find(
        filter=filter_clause,
        projection={"_id": {"$toString": "$_id"},
                    "user_name": "$user_name",
                    "text": "$text",
                    "created_at": "$created_at", },
        sort=[("_id", pymongo.DESCENDING)])
    return list(cursor)


def create_post(user_name: str, text: str, ):
    data = {
        "user_name": user_name,
        "text": text,
        "created_at": datetime.now()
    }
    result = get_collection(post_collection_name).insert_one(data)
    data["_id"] = str(result.inserted_id)
    return data


@invalid_id_handler
def retrieve_post(obj_id):
    return get_collection(post_collection_name).find_one(
        filter={"_id": ObjectId(obj_id)},
        projection={"_id": {"$toString": "$_id"},
                    "user_name": "$user_name",
                    "text": "$text",
                    "created_at": "$created_at", }, )


@invalid_id_handler
def check_post_exists(post_id: str, user_name: Union[str, None] = None) -> bool:
    filter_clause = {"_id": ObjectId(post_id)}
    if user_name:
        filter_clause["user_name"] = {"$ne": user_name}
    return get_collection(post_collection_name).find_one(filter=filter_clause) is not None
