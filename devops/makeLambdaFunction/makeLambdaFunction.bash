#!/bin/sh
INITIALS_PROMPT="Please enter your first and last initial (or 'q' to quit)"
NUM=2

while :
  do
    # get and validate user initials
    printf "%s\n" "$INITIALS_PROMPT" 
    while read initials && [ "$initials" != "q" ];
      do
        # checks to see if string is null or has zero length
        if [ -z "$initials" ]; then
          printf '%s\n' "Error: initials can't be empty" 
        # checks to see if the string matches the requested pattern
        elif [[ "${initials}" =~ [^a-zA-Z] ]]; then
          printf '%s\n' "Error: initials must only contain letters, a-z"
        elif [[ "${#initials}" != $NUM ]]; then
          printf '%s\n' "Error: initials must be $NUM characters"
        else
          break
        fi
          printf "%s\n" "$INITIALS_PROMPT" 
      done

    if [ "$initials" == "q" ]; then
      printf '%s\n' "Done"
      break
    fi



    fileName="index.zip"
    regionName="us-west-2"


    # converts initials to lowercase and remove spaces
    formattedInitials="$(echo "${initials}" | tr -d '[:space:]' | tr '[:upper:]' '[:lower:]')"
    todayDate=$(date +'%Y%m%d')
    # generates a random string https://unix.stackexchange.com/questions/230673/how-to-generate-a-random-string
    randomString=$(cat /dev/urandom | base64 | tr -dc 'a-z0-9' | fold -w 5 | head -n 1) 
    uniqueName=$formattedInitials-$randomString-$todayDate
    lambdaName=$uniqueName-lambda
    bucketName=$uniqueName-bucket
    stackName=$uniqueName-stack

    printf "%s\n" "Your S3 bucket, Lambda function and CloudFormation stack will be named as follows:" \
            "file name: $fileName" \
            "bucket: $bucketName" \
            "lambda: $lambdaName" \
            "stack: $stackName" \
            "Create S3 bucket, Lambda function and CloudFormation stack? (y/n)" 

    lambdaTemplate="./makeLambdaFunction.yml"
    while read answer && [ "$answer" != "q" ];
      do
        if [ "$answer" == "y" ]; then
          printf '%s\n' "aws s3 mb s3://$bucketName"
          # creates the S3 bucket
          aws s3 mb s3://$bucketName

          printf '%s\n' "aws s3 cp $fileName s3://$bucketName"
          # adds the file to the S3 bucket
          aws s3 cp $fileName s3://$bucketName

          printf '%s\n' "aws cloudformation package --template-file $lambdaTemplate --s3-bucket $bucketName --output-template-file packagedTemplate.yml"
          # uploads the code file to the S3 bucket and returns a template file with the bucket name
          aws cloudformation package --template-file $lambdaTemplate --s3-bucket $bucketName --output-template-file packagedTemplate.yml
          
          printf '%s\n' "aws cloudformation deploy --template-file packagedTemplate.yml --stack-name $stackName --parameter-overrides LambdaName=$lambdaName --capabilities CAPABILITY_NAMED_IAM"
          # deploys the stack
          aws cloudformation deploy --template-file packagedTemplate.yml --stack-name $stackName --parameter-overrides LambdaName=$lambdaName --capabilities CAPABILITY_NAMED_IAM
         
          printf '%s\n' "aws s3 rm s3://$bucketName --recursive"
          # empties the S3 bucket
          aws s3 rm s3://$bucketName --recursive

          printf '%s\n' "aws s3api delete-bucket --bucket $bucketName --region $regionName" 
          # deletes the S3 bucket
          aws s3api delete-bucket --bucket $bucketName --region $regionName

          break
        elif [ "$answer" == "n" ]; then
          break
        else
          printf "%s\n" "Create lambda? (y/n)"
        fi
      done
    printf '%s\n' "Done" 
    break
  done 

