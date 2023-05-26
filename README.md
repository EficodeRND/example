Added integration testing to .github/workflows/python_backend_build.yml

On repository root run
- `yarn`
- `cd backend`
- `python3.9 -m venv venv`
- `source venv/bin/activate`
- `pip install -r requirements.txt`
- `pip install -r requirements_dev.txt`
- `yarn deploy_arm`
  - The layer is not created

```
2023-04-13 14:54:20 2023-04-13T11:54:20.816  WARN --- [functhread48] l.s.c.e.template_deployer  : Error calling <bound method ClientCreator._create_api_method.<locals>._api_call of <botocore.client.Lambda object at 0xffff48aede10>> with params: {'Content': {'S3Bucket': 'example-local-serverlessdeploymentbuck-80f1dc43', 'S3Key': 'serverless/example/local/1681386839838-2023-04-13T11:53:59.838Z/pythonRequirements.zip'}, 'LayerName': 'example-local-python-requirements', 'Description': 'Python requirements generated by serverless-python-requirements.', 'CompatibleRuntimes': ['python3.9']} for resource: {'Type': 'AWS::Lambda::LayerVersion', 'LogicalResourceId': 'PythonRequirementsLambdaLayer', 'Properties': {'Content': {'S3Bucket': 'example-local-serverlessdeploymentbuck-80f1dc43', 'S3Key': 'serverless/example/local/1681386839838-2023-04-13T11:53:59.838Z/pythonRequirements.zip'}, 'LayerName': 'example-local-python-requirements', 'Description': 'Python requirements generated by serverless-python-requirements.', 'CompatibleRuntimes': ['python3.9']}, '_state_': {}}
2023-04-13 14:54:20 2023-04-13T11:54:20.817 DEBUG --- [functhread48] l.s.c.e.template_deployer  : Error applying changes for CloudFormation stack "example-local": An error occurred (InternalError) when calling the PublishLayerVersion operation (reached max retries: 4): exception while calling lambda.PublishLayerVersion: Traceback (most recent call last):
2023-04-13 14:54:20   File "/opt/code/localstack/.venv/lib/python3.10/site-packages/localstack/aws/chain.py", line 90, in handle
2023-04-13 14:54:20     handler(self, self.context, response)
2023-04-13 14:54:20   File "/opt/code/localstack/.venv/lib/python3.10/site-packages/localstack/aws/handlers/service.py", line 123, in __call__
2023-04-13 14:54:20     handler(chain, context, response)
2023-04-13 14:54:20   File "/opt/code/localstack/.venv/lib/python3.10/site-packages/localstack/aws/handlers/service.py", line 93, in __call__
2023-04-13 14:54:20     skeleton_response = self.skeleton.invoke(context)
2023-04-13 14:54:20   File "/opt/code/localstack/.venv/lib/python3.10/site-packages/localstack/aws/skeleton.py", line 154, in invoke
2023-04-13 14:54:20     return self.dispatch_request(context, instance)
2023-04-13 14:54:20   File "/opt/code/localstack/.venv/lib/python3.10/site-packages/localstack/aws/skeleton.py", line 166, in dispatch_request
2023-04-13 14:54:20     result = handler(context, instance) or {}
2023-04-13 14:54:20   File "/opt/code/localstack/.venv/lib/python3.10/site-packages/localstack/aws/skeleton.py", line 118, in __call__
2023-04-13 14:54:20     return self.fn(*args, **kwargs)
2023-04-13 14:54:20   File "/opt/code/localstack/.venv/lib/python3.10/site-packages/localstack/services/awslambda/provider.py", line 2933, in publish_layer_version
2023-04-13 14:54:20     code = store_s3_bucket_archive(
2023-04-13 14:54:20   File "/opt/code/localstack/.venv/lib/python3.10/site-packages/localstack/services/awslambda/invocation/lambda_service.py", line 589, in store_s3_bucket_archive
2023-04-13 14:54:20     archive_file = s3_client.get_object(Bucket=archive_bucket, Key=archive_key, **kwargs)[
2023-04-13 14:54:20   File "/opt/code/localstack/.venv/lib/python3.10/site-packages/botocore/client.py", line 530, in _api_call
2023-04-13 14:54:20     return self._make_api_call(operation_name, kwargs)
2023-04-13 14:54:20   File "/opt/code/localstack/.venv/lib/python3.10/site-packages/botocore/client.py", line 960, in _make_api_call
2023-04-13 14:54:20     raise error_class(parsed_response, operation_name)
2023-04-13 14:54:20 botocore.errorfactory.NoSuchKey: An error occurred (NoSuchKey) when calling the GetObject operation: The specified key does not exist.
2023-04-13 14:54:20  Traceback (most recent call last):
2023-04-13 14:54:20   File "/opt/code/localstack/.venv/lib/python3.10/site-packages/localstack/services/cloudformation/engine/template_deployer.py", line 1336, in _run
2023-04-13 14:54:20     self.do_apply_changes_in_loop(changes, stack)
2023-04-13 14:54:20   File "/opt/code/localstack/.venv/lib/python3.10/site-packages/localstack/services/cloudformation/engine/template_deployer.py", line 1413, in do_apply_changes_in_loop
2023-04-13 14:54:20     self.apply_change(change, stack=stack)
2023-04-13 14:54:20   File "/opt/code/localstack/.venv/lib/python3.10/site-packages/localstack/services/cloudformation/engine/template_deployer.py", line 1495, in apply_change
2023-04-13 14:54:20     result = execute_resource_action(resource_id, self, ACTION_CREATE)
2023-04-13 14:54:20   File "/opt/code/localstack/.venv/lib/python3.10/site-packages/localstack/services/cloudformation/engine/template_deployer.py", line 743, in execute_resource_action
2023-04-13 14:54:20     result = configure_resource_via_sdk(
2023-04-13 14:54:20   File "/opt/code/localstack/.venv/lib/python3.10/site-packages/localstack/services/cloudformation/engine/template_deployer.py", line 867, in configure_resource_via_sdk
2023-04-13 14:54:20     raise e
2023-04-13 14:54:20   File "/opt/code/localstack/.venv/lib/python3.10/site-packages/localstack/services/cloudformation/engine/template_deployer.py", line 850, in configure_resource_via_sdk
2023-04-13 14:54:20     result = function(**params)
2023-04-13 14:54:20   File "/opt/code/localstack/.venv/lib/python3.10/site-packages/botocore/client.py", line 530, in _api_call
2023-04-13 14:54:20     return self._make_api_call(operation_name, kwargs)
2023-04-13 14:54:20   File "/opt/code/localstack/.venv/lib/python3.10/site-packages/botocore/client.py", line 960, in _make_api_call
2023-04-13 14:54:20     raise error_class(parsed_response, operation_name)
2023-04-13 14:54:20 botocore.exceptions.ClientError: An error occurred (InternalError) when calling the PublishLayerVersion operation (reached max retries: 4): exception while calling lambda.PublishLayerVersion: Traceback (most recent call last):
2023-04-13 14:54:20   File "/opt/code/localstack/.venv/lib/python3.10/site-packages/localstack/aws/chain.py", line 90, in handle
2023-04-13 14:54:20     handler(self, self.context, response)
2023-04-13 14:54:20   File "/opt/code/localstack/.venv/lib/python3.10/site-packages/localstack/aws/handlers/service.py", line 123, in __call__
2023-04-13 14:54:20     handler(chain, context, response)
2023-04-13 14:54:20   File "/opt/code/localstack/.venv/lib/python3.10/site-packages/localstack/aws/handlers/service.py", line 93, in __call__
2023-04-13 14:54:20     skeleton_response = self.skeleton.invoke(context)
2023-04-13 14:54:20   File "/opt/code/localstack/.venv/lib/python3.10/site-packages/localstack/aws/skeleton.py", line 154, in invoke
2023-04-13 14:54:20     return self.dispatch_request(context, instance)
2023-04-13 14:54:20   File "/opt/code/localstack/.venv/lib/python3.10/site-packages/localstack/aws/skeleton.py", line 166, in dispatch_request
2023-04-13 14:54:20     result = handler(context, instance) or {}
2023-04-13 14:54:20   File "/opt/code/localstack/.venv/lib/python3.10/site-packages/localstack/aws/skeleton.py", line 118, in __call__
2023-04-13 14:54:20     return self.fn(*args, **kwargs)
2023-04-13 14:54:20   File "/opt/code/localstack/.venv/lib/python3.10/site-packages/localstack/services/awslambda/provider.py", line 2933, in publish_layer_version
2023-04-13 14:54:20     code = store_s3_bucket_archive(
2023-04-13 14:54:20   File "/opt/code/localstack/.venv/lib/python3.10/site-packages/localstack/services/awslambda/invocation/lambda_service.py", line 589, in store_s3_bucket_archive
2023-04-13 14:54:20     archive_file = s3_client.get_object(Bucket=archive_bucket, Key=archive_key, **kwargs)[
2023-04-13 14:54:20   File "/opt/code/localstack/.venv/lib/python3.10/site-packages/botocore/client.py", line 530, in _api_call
2023-04-13 14:54:20     return self._make_api_call(operation_name, kwargs)
2023-04-13 14:54:20   File "/opt/code/localstack/.venv/lib/python3.10/site-packages/botocore/client.py", line 960, in _make_api_call
2023-04-13 14:54:20     raise error_class(parsed_response, operation_name)
2023-04-13 14:54:20 botocore.errorfactory.NoSuchKey: An error occurred (NoSuchKey) when calling the GetObject operation: The specified key does not exist.
2023-04-13 14:54:20 
2023-04-13 14:54:20 
```

