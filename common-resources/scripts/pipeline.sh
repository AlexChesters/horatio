set -e

aws cloudformation deploy \
  --template-file ci/codepipeline.yml \
  --stack-name codepipeline-horatio-common-resources \
  --capabilities CAPABILITY_IAM \
  --region eu-west-1 \
  --profile accounts-janitor
