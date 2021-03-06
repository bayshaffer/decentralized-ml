import time
from datetime import datetime, timedelta
import uuid
import os
import boto3

import state
from message import LibraryType


def store_update(type, message, with_weights=True):
    """
    Stores an update in DynamoDB. If weights are present, it stores them in S3.
    """
    print("[{0}]: {1}".format(type, message))

    if state.state["test"] \
            or state.state["library_type"] == LibraryType.IOS_TEXT.value:
        return

    if with_weights:
        try:
            repo_id = state.state["repo_id"]
            session_id = state.state["session_id"]
            round = state.state["current_round"]
            s3 = boto3.resource("s3")
            weights_s3_key = "{0}/{1}/{2}/model.h5"
            weights_s3_key = weights_s3_key.format(repo_id, session_id, round)
            object = s3.Object("updatestore", weights_s3_key)
            h5_model_path = state.state["h5_model_path"]
            object.put(Body=open(h5_model_path, "rb"))
        except Exception as e:
            print("S3 Error: {0}".format(e))

    try:
        dynamodb = boto3.resource("dynamodb", region_name="us-west-1")
        table = dynamodb.Table("UpdateStore")
        current_time = datetime.now()
        item = {
            "Id": str(uuid.uuid4()),
            "RepoId": state.state["repo_id"],
            "CreationTime": int(current_time.timestamp()),
            "ExpirationTime": int((current_time + timedelta(days=3)).timestamp()),
            "ContentType": type,
            "SessionId": state.state["session_id"],
            "Content": repr(message),
        }
        if with_weights:
            item["WeightsS3Key"] = "s3://updatestore/" + weights_s3_key
        table.put_item(Item=item)
    except Exception as e:
        print("DB Error: {0}".format(e))
