import logging as log
import os

import boto3

from lambdas import init_lambda
from lambdas.services.db_manager import with_db_session, get_app_db
from lambdas.utils import validators
from lambdas.utils.common import RequestException
from models import UserAccount

aws_client = boto3.client(
    "cognito-idp", region_name=os.environ.get("AWS_REGION"))

init_lambda()


def get_aws_list(values: list[str]):
    result = ','.join(values)
    return f"[{result}]"


def create_user(username, password, email, groups: list[str], add_user_db: bool = True):
    user_pool_id = os.environ.get("USERPOOL_ID")
    client_id = os.environ.get("CLIENT_ID")
    aws_client.admin_create_user(
        UserPoolId=user_pool_id,
        Username=username,
        UserAttributes=[
            {"Name": "email", "Value": email},
            {"Name": "email_verified", "Value": "true"},
            {"Name": "custom:groups", "Value": get_aws_list(groups)},
        ],
        MessageAction="SUPPRESS",
        DesiredDeliveryMediums=["EMAIL"],
        TemporaryPassword=password,
    )

    aws_client.admin_set_user_password(
        UserPoolId=user_pool_id,
        Username=username,
        Password=password,
        Permanent=True
    )

    if add_user_db is True:
        db = get_app_db()

        user = UserAccount(
            user_name=username,
            name=username,
            email=email
        )
        db.session.add(user)
        db.session.commit()

    return {'username': username, 'status': 'Created', 'userPoolId': user_pool_id, 'clientId': client_id}


@with_db_session
def handler(event, _context):
    action = validators.get_event_value(
        event,
        "action",
        allowed_values=["create_user", "delete_user",
                        "create_org", "delete_org"],
    )

    if action == "create_user":
        username = validators.get_event_value(event, "username")
        log.debug("creating user %s", username)
        email = validators.get_event_value(event, "email")
        password = validators.get_event_value(event, "password")
        groups = validators.get_event_value(event, "groups")
        add_user_db = event.get("addUserToDb", True)
        return create_user(username=username,
                           password=password,
                           email=email,
                           groups=groups,
                           add_user_db=add_user_db
                           )

    raise RequestException("Unknown action")