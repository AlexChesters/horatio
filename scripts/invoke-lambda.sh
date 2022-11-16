set -e

OUTPUT=$(aws lambda invoke \
  --function-name $1 \
  --log-type Tail \
  --profile accounts-janitor \
  lambda_invoke_output.log)

echo $OUTPUT | jq -r .LogResult | base64 --decode
