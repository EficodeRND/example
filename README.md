On repository root run
- `yarn`
- `cd backend`
- `python3.11 -m venv venv`
- `source venv/bin/activate`
- `pip install -r requirements.txt`
- `pip install -r requirements_dev.txt`
- `yarn deploy_arm`
- `invoke alltests`

Result:
test_users fails on `test_get_user_information` and `test_sysadmin_get_user_information`.

An exert from the error:
```
content-type;host;x-amz-date;x-amz-target
4cf4ba2d1e141720f04c197f74f68afd46f09e49a241c8cadab37dcff8d65627
2024-01-04 12:33:07,109 DEBUG (auth.py:428) - StringToSign:
AWS4-HMAC-SHA256
20240104T103307Z
20240104/us-east-1/cognito-idp/aws4_request
1c619333b1788bfe514be162d2bbda6c5128ad43f7a62f9e05da2055b4774fc0
2024-01-04 12:33:07,109 DEBUG (auth.py:430) - Signature:
27bf278cb55a165ea4f80d5c675949c5c88d4eb96721287baea01c17571cc92a
2024-01-04 12:33:07,109 DEBUG (hooks.py:238) - Event request-created.cognito-identity-provider.AdminInitiateAuth: calling handler <function add_retry_headers at 0x10411c040>
2024-01-04 12:33:07,109 DEBUG (endpoint.py:265) - Sending http request: <AWSPreparedRequest stream_output=False, method=POST, url=http://localhost:4566/, headers={'X-Amz-Target': b'AWSCognitoIdentityProviderService.AdminInitiateAuth', 'Content-Type': b'application/x-amz-json-1.1', 'User-Agent': b'Boto3/1.34.12 md/Botocore#1.34.12 ua/2.0 os/macos#23.1.0 md/arch#arm64 lang/python#3.11.6 md/pyimpl#CPython cfg/retry-mode#legacy Botocore/1.34.12', 'X-Amz-Date': b'20240104T103307Z', 'Authorization': b'AWS4-HMAC-SHA256 Credential=AKIAVVIMTBSRAPUTYQ4H/20240104/us-east-1/cognito-idp/aws4_request, SignedHeaders=content-type;host;x-amz-date;x-amz-target, Signature=27bf278cb55a165ea4f80d5c675949c5c88d4eb96721287baea01c17571cc92a', 'amz-sdk-invocation-id': b'8ad53f6b-d270-40b6-bff8-48002f39e690', 'amz-sdk-request': b'attempt=1', 'Content-Length': '279'}>
2024-01-04 12:33:07,109 DEBUG (connectionpool.py:293) - Resetting dropped connection: localhost
2024-01-04 12:33:07,115 DEBUG (connectionpool.py:547) - http://localhost:4566 "POST / HTTP/1.1" 400 163
2024-01-04 12:33:07,115 DEBUG (parsers.py:240) - Response headers: {'Content-Type': 'application/json', 'X-Amzn-Errortype': 'ResourceNotFoundException', 'Content-Length': '163', 'x-amzn-requestid': 'ba717b58-3d82-4105-b98a-39f294032b80', 'Connection': 'close', 'date': 'Thu, 04 Jan 2024 10:33:07 GMT', 'server': 'hypercorn-h11'}
2024-01-04 12:33:07,115 DEBUG (parsers.py:241) - Response body:
b'{"__type": "ResourceNotFoundException", "message": "Unable to find user pool client with ID us-east-1_dbba14c6ca0a42e093681ca9744491ad-jip8bb6v41xdce4zuex05wsh24"}'
2024-01-04 12:33:07,115 DEBUG (parsers.py:240) - Response headers: {'Content-Type': 'application/json', 'X-Amzn-Errortype': 'ResourceNotFoundException', 'Content-Length': '163', 'x-amzn-requestid': 'ba717b58-3d82-4105-b98a-39f294032b80', 'Connection': 'close', 'date': 'Thu, 04 Jan 2024 10:33:07 GMT', 'server': 'hypercorn-h11'}
2024-01-04 12:33:07,115 DEBUG (parsers.py:241) - Response body:
b'{"__type": "ResourceNotFoundException", "message": "Unable to find user pool client with ID us-east-1_dbba14c6ca0a42e093681ca9744491ad-jip8bb6v41xdce4zuex05wsh24"}'
2024-01-04 12:33:07,115 DEBUG (hooks.py:238) - Event needs-retry.cognito-identity-provider.AdminInitiateAuth: calling handler <botocore.retryhandler.RetryHandler object at 0x1057ab8d0>
2024-01-04 12:33:07,115 DEBUG (retryhandler.py:211) - No retry needed.
```

Obs.: The latest localstack-pro docker image that this error does not happen is `sha256:fd995574675fea976a8ebd5325ed256bcc6cdb1d41167ab2304e5ffab27676ee`. 