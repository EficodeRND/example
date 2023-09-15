from gql.dsl import DSLSchema, DSLQuery

from aws_utils import create_user, get_gql_client, query_gql, GROUP_SYSADMIN, GROUP_USER


def test_get_user_information(ctx):
    user_1 = create_user(ctx=ctx, groups=[GROUP_SYSADMIN])
    user_2 = create_user(ctx=ctx, groups=[GROUP_USER])

    client = get_gql_client(ctx=ctx, user=user_1)
    ds: DSLSchema = DSLSchema(client.schema)
    query = DSLQuery(
        ds.Query.user().select(
            ds.UserAccount.userName,
            ds.UserAccount.email
        )
    )

    result = query_gql(client=client, query=query)
    assert result['user']['userName'] == user_1.username
    assert result['user'].get('email') is None

    client = get_gql_client(ctx=ctx, user=user_2)
    result = query_gql(client=client, query=query)
    assert result['user']['userName'] == user_2.username
    assert result['user'].get('email') is None


def test_sysadmin_get_user_information(ctx):
    user_1 = create_user(ctx=ctx, groups=[GROUP_USER])
    sysadmin = create_user(ctx=ctx, groups=[GROUP_SYSADMIN])

    client = get_gql_client(ctx=ctx, user=sysadmin)
    ds: DSLSchema = DSLSchema(client.schema)
    query = DSLQuery(
        ds.Query.getUser(userName=user_1.username).select(
            ds.UserAccount.userName,
            ds.UserAccount.email
        )
    )

    result = query_gql(client=client, query=query)
    assert result['getUser']['userName'] == user_1.username
    assert result['getUser'].get('email') == user_1.email
    faulty_query = DSLQuery(
        ds.Query.getUser(userName="thisdoesn'texistforsure").select(
            ds.UserAccount.userName,
            ds.UserAccount.email
        )
    )

    result = query_gql(client=client, query=faulty_query)
    assert result[0]['errorType'] == 'TypeError'

    client = get_gql_client(ctx=ctx, user=user_1)
    result = query_gql(client=client, query=query)
    assert result[0]['errorType'] == 'Unauthorized'
