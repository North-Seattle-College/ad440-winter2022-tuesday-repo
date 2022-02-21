#!/bin/bash

SCRIPT_PATH=$(dirname "$0")

# import validateInitials from common.lib
# shellcheck disable=SC1091
. "$SCRIPT_PATH/../common.lib"

INITIALS_PROMPT="What are your initials? ('q' to quit)"

initials="$1"
region="$2"
skipPrompt=false

while :; do
  # get and validate user initials if not passed as arg
  if [[ -z "$initials" ]]; then
    printf "%s\n" "$INITIALS_PROMPT" >&1
    printf "%s" "> " >&1
    while read -r initials && [ "$initials" != "q" ]; do
      if validateInitials "$initials"; then
        region="us-west-2"
        break
      fi
      printf "%s\n" "$INITIALS_PROMPT" >&1
      printf "%s" "> " >&1
    done
  elif validateInitials "$initials"; then
    if [[ -z "$region" ]]; then
      region="us-west-2"
    elif ! validateRegion "$region"; then
      break
    fi

    skipPrompt=true
    answer=y
  else
    break
  fi

  if [[ "$initials" == "q" ]]; then
    printf '%s\n' "Done" >&1
    break
  fi

    # folderName="./backend/data/simpleLambda"

    # converts initials to lowercase and remove spaces
    formattedInitials="$(echo "${initials}" | tr -d '[:space:]' | tr '[:upper:]' '[:lower:]')"
    todayDate=$(date +'%Y%m%d')
    # generates a random string https://unix.stackexchange.com/questions/230673/how-to-generate-a-random-string
    randomString=$(cat /dev/urandom | base64 | tr -dc 'a-z0-9' | fold -w 5 | head -n 1) 
    uniqueName=$formattedInitials-$randomString-$todayDate
    lambdaName=$uniqueName-lambda
    bucketName=$uniqueName-bucket
    stackName=$uniqueName-stack
    lambdaTemplate="./backend/simpleLambda/makeLambdaFunction.yml"



    if [ "$skipPrompt" = false ]; then
    # show user name of bucket and stack, get confirmation to create resources
    printf "%s\n" "Your S3 bucket, Lambda function and CloudFormation stack will be named as follows:" \
            "folder name: $folderName" \
            "bucket: $bucketName" \
            "lambda: $lambdaName" \
            "stack: $stackName" \
            "Create S3 bucket, Lambda function and CloudFormation stack? (y/n)" 
    printf "%s" "> " >&1
    while read -r answer && [ "$answer" != "q" ]; do
      if [ "${answer:0:1}" == "y" ] || [ "${answer:0:1}" == "n" ]; then
        break
      else
        printf "%s\n" "Create bucket? (y/n)" >&1
        printf "%s" "> " >&1
      fi
    done
  fi


    if [ "$answer" == "y" ]; then
      printf '%s\n' "aws s3 mb s3://$bucketName"
      # creates the S3 bucket
      aws s3 mb s3://$bucketName

      printf '%s\n' "aws cloudformation package --template-file $lambdaTemplate --s3-bucket $bucketName --output-template-file packagedTemplate.yml"
      # uploads the code file to the S3 bucket and returns a template file with the bucket name
      aws cloudformation package --template-file $lambdaTemplate --s3-bucket $bucketName --output-template-file ./devops/makeLambdaFunction/packagedTemplate.yml

      printf '%s\n' "aws cloudformation deploy --region $region --template-file packagedTemplate.yml --stack-name $stackName --parameter-overrides LambdaName=$lambdaName --capabilities CAPABILITY_NAMED_IAM"
      # deploys the stack
      aws cloudformation deploy --region $region --template-file ./devops/makeLambdaFunction/packagedTemplate.yml --stack-name $stackName --parameter-overrides LambdaName=$lambdaName --capabilities CAPABILITY_NAMED_IAM

      printf '%s\n' "aws s3 rm s3://$bucketName --recursive"
      # empties the S3 bucket
      aws s3 rm s3://$bucketName --recursive

      printf '%s\n' "aws s3api delete-bucket --bucket $bucketName --region $region" 
      # deletes the S3 bucket
      aws s3api delete-bucket --bucket $bucketName --region $region

      break
    elif [ "$answer" == "n" ]; then
      break
    else
      printf "%s\n" "Create lambda? (y/n)"
    fi
  printf '%s\n' "Done" 
done 
