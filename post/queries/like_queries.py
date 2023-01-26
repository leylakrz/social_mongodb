from datetime import datetime
from typing import Union

import pymongo
from bson import ObjectId

from utils.clients.mongodb import get_collection
from utils.decorators import invalid_id_handler

like_collection_name = "like"


@invalid_id_handler
def list_like(post_id: str, last_show_id: Union[None, str] = None, ):
    filter_clause = {"post_id": ObjectId(post_id)}
    if last_show_id:
        filter_clause["_id"] = {"$lt": ObjectId(last_show_id), }

    cursor = get_collection(like_collection_name).find(
        filter=filter_clause,
        projection={"_id": {"$toString": "$_id"},
                    "user_name": "$user_name",
                    "created_at": "$created_at", },
        sort=[("_id", pymongo.DESCENDING)])
    return list(cursor)


@invalid_id_handler
def create_like(post_id: str, user_name: str, ):
    get_collection(like_collection_name).find_one_and_update(
        {"post_id": ObjectId(post_id), "user_name": user_name, },
        {"$setOnInsert": {"created_at": datetime.now()}},
        upsert=True,
    )
