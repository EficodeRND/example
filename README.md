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
test_users fails on `tests/integration/test_users.py::test_get_user_information - Assertion...`
because user email address is retrieved with role USER even if it's allowed for group SYSADMIN only on the graphql schema


