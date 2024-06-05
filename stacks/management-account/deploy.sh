set -e

aws cloudformation deploy \
  --template-file horatio-list-accounts-role.yml \
  --stack-name horatio-list-accounts-role \
  --capabilities CAPABILITY_NAMED_IAM \
  --region eu-west-1 \
  --profile management
