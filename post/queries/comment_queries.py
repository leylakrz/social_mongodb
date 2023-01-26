from datetime import datetime
from typing import Union

import pymongo
from bson import ObjectId

from utils.clients.mongodb import get_collection
from utils.decorators import invalid_id_handler

comment_collection_name = "comment"


@invalid_id_handler
def list_comment(post_id: str, last_show_id: Union[None, str] = None, ):
    filter_clause = {"post_id": ObjectId(post_id)}
    if last_show_id:
        filter_clause["_id"] = {"$lt": ObjectId(last_show_id), }

    cursor = get_collection(comment_collection_name).find(
        filter=filter_clause,
        projection={"_id": {"$toString": "$_id"},
                    "user_name": "$user_name",
                    "text": "$text",
                    "created_at": "$created_at", },
        sort=[("_id", pymongo.DESCENDING)])
    return list(cursor)


@invalid_id_handler
def create_comment(post_id: str, user_name: str, text: str):
    data = {
        "post_id": ObjectId(post_id),
        "user_name": user_name,
        "text": text,
        "created_at": datetime.now()
    }
    result = get_collection(comment_collection_name).insert_one(data)
    data["_id"] = str(result.inserted_id)
    del data["post_id"]
    return data
