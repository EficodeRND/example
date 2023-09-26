On repository root run
- `yarn`
- `cd backend`
- `python3.9 -m venv lambda_venv`
- `source lambda_venv/bin/activate`
- For ARM CPUs `pip install --platform=manylinux2014_aarch64 --only-binary=:all: -r requirements.txt --target lambda_venv/lib/python3.9/site-packages`
- For x86 CPUs `pip install --platform=manylinux2014_x86_64 --only-binary=:all: -r requirements.txt --target lambda_venv/lib/python3.9/site-packages`
- `deactivate`
- `python3.9 -m venv venv`
- `source venv/bin/activate`
- `pip install -r requirements.txt`
- `pip install -r requirements_dev.txt`
- For ARM CPUs `yarn deploy_arm`
- For x86 CPUs `yarn deploy`
- `invoke alltests`

Check logs of generateReport lambda. 
- `yarn logs generateReport`
Contains Unauthorized error that should not be there (IAM authorization). This works in AWS (have not tested this branch in AWS but our own code which is mostly the same)


## Troubleshooting

If DB migrations are not going though (they are run when calling `yarn deploy`) check which port DB uses and set that port (if not 4510) in `backend/lambdas/services/db_manager.py` line 13 and run
```
yarn createdb
yarn migratedb
```
