from gql.dsl import DSLSchema, DSLMutation, DSLInlineFragment, DSLMetaField
from random_username.generate import generate_username

from aws_utils import create_user, GROUP_SYSADMIN, get_gql_client, query_gql, AWSUtils
from conftest import TestContext
from utils import str_utils
from utils.common import Singleton


class PortalUtils(metaclass=Singleton):
    def __init__(self, ctx: TestContext):
        self.ctx = ctx
        self.aws = AWSUtils(ctx)
        self.sysadmin = create_user(ctx=ctx, groups=[GROUP_SYSADMIN], do_auth=False)

    def authenticate_sysadmin(self):
        self.sysadmin = self.aws.authenticate(self.sysadmin)
