import json
import logging as log
import os
from dataclasses import dataclass
from typing import Generator
from uuid import uuid4

import boto3
from gql.transport.aiohttp import AIOHTTPTransport
from gql.transport.appsync_auth import AppSyncJWTAuthentication
from gql.transport.appsync_websockets import AppSyncWebsocketsTransport
from random_username.generate import generate_username

from tests.integration.conftest import TestContext
from utils import gql_utils
from utils.common import Singleton
from utils.gql_utils import query_gql

from gql import gql, Client

GROUP_SYSADMIN: str = 'LOCAL_SYSADMIN'
GROUP_USER: str = 'LOCAL_USER'

ALL_GROUPS: list[str] = [GROUP_SYSADMIN, GROUP_USER]


@dataclass
class User:
    username: str
    password: str
    email: str
    user_pool_id: str
    client_id: str
    token: str = None


class AWSUtils(metaclass=Singleton):

    def __init__(self, ctx: TestContext):
        self.ctx = ctx
        self.session = boto3.Session(profile_name="serverless")
        self.lambda_client = self.session.client(
            "lambda",
            endpoint_url=ctx.endpoint_url,
            region_name=ctx.region
        )
        self.cognito_client = self.session.client(
            "cognito-idp",
            endpoint_url=ctx.endpoint_url,
            region_name=ctx.region
        )

        log.info("CURRENT DIR: %s", os.getcwd())

        if os.path.isdir('lambdas'):
            base_path = ''
        elif os.path.isdir('backend'):
            base_path = 'backend/'
        elif os.path.isdir('../../lambdas'):
            base_path = '../../'
        else:
            base_path = '../../../'

        log.info("PATH: %s", base_path)

        self.schema = gql_utils.get_graphql_schema(base_path=base_path)
        log.info(f"""Effective Schema:
        
        {self.schema}
        
        """)

    def call_lambda(self, payload: dict, function_name: str):
        json_payload = json.dumps(payload)
        resp = self.lambda_client.invoke(
            FunctionName=function_name,
            InvocationType='RequestResponse',
            Payload=json_payload)
        if resp.get('StatusCode', None) == 200:
            return json.loads(resp['Payload'].read().decode("utf-8"))

        raise Exception(f"Call to lambda {function_name} failed")

    def authenticate(self, user: User):
        response = self.cognito_client.admin_initiate_auth(
            UserPoolId=user.user_pool_id,
            ClientId=user.client_id,
            AuthFlow='USER_PASSWORD_AUTH',
            AuthParameters={
                'USERNAME': user.username,
                'PASSWORD': str(user.password)
            }
        )
        user.token = response['AuthenticationResult']['IdToken']
        return user

    def destroy(self):
        self.ctx = None
        self.session = None
        self.lambda_client = None
        AWSUtils._instances = {}


def create_user(ctx: TestContext,
                username: str = None,
                password: str = None,
                groups: list[str] = None,
                do_auth: bool = True,
                add_user_to_db: bool = True):

    if username is None:
        username = generate_username()[0]

    if password is None:
        password = f"A{uuid4()}"

    if groups is None:
        groups = ALL_GROUPS

    email = f"{username}@example.com.invalid"
    payload = {
        "action": "create_user",
        "username": username,
        "email": email,
        "password": password,
        "groups": groups,
        "addUserToDb": add_user_to_db,
    }

    aws = AWSUtils(ctx)
    result = aws.call_lambda(
        payload=payload, function_name='example-local-devTestHelper')
    user = User(username=username, password=password, email=email,
                user_pool_id=result['userPoolId'], client_id=result['clientId'])
    if do_auth:
        user = authenticate(ctx=ctx, user=user)
    return user


def authenticate(ctx: TestContext, user: User) -> User:
    aws = AWSUtils(ctx)
    return aws.authenticate(user)


def get_gql_client(ctx: TestContext, user: User) -> Client:
    auth = AppSyncJWTAuthentication(
        host=ctx.host,
        jwt=user.token,
    )
    transport = AIOHTTPTransport(url=ctx.graphql_url, auth=auth)
    aws = AWSUtils(ctx=ctx)
    return Client(transport=transport, fetch_schema_from_transport=False, schema=aws.schema, execute_timeout=20)


def do_gql(ctx: TestContext, user: User, query):
    client = get_gql_client(ctx, user)
    return query_gql(client=client, query=query)


def subscribe(query: str, ctx: TestContext, user: User, params: dict = None) -> Generator:
    auth = AppSyncJWTAuthentication(
        host=ctx.host,
        jwt=user.token,
    )
    transport = AppSyncWebsocketsTransport(
        url=ctx.graphql_ws, auth=auth, connect_timeout=60, close_timeout=60, ack_timeout=60)

    client = Client(transport=transport,
                    fetch_schema_from_transport=False,
                    schema=AWSUtils(ctx=ctx).schema,
                    execute_timeout=60
                    )

    return client.subscribe(gql(query), variable_values=params)
