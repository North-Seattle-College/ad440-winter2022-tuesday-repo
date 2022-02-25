# !/bin/bash
INITIALS_PROMPT="Please enter your first and last initial (or 'q' to quit)"
NUM=2
initials=$1

    #if [ "$initials" == "q" ]; then
    #  printf '%s\n' "Done"
     # break
    #fi
    
  # converts initials to lowercase and remove spaces
  formattedInitials="$(echo "${initials}" | tr -d '[:space:]' | tr '[:upper:]' '[:lower:]')"
  todayDate=$(date +'%Y%m%d')
  OPENSSL_STRING=$(openssl rand -hex 3)
  RANDOM_STRING=${OPENSSL_STRING:0:5}
  uniqueName=$formattedInitials-$RANDOM_STRING-$todayDate
  lambdaName=$uniqueName-lambda
  stackName=$uniqueName-stack
  initials="$1"
  answer=y

    printf "%s\n" "Your lambda function and stack will be named as follows:" \
            "lambda: $lambdaName" \
            "stack: $stackName" \
            "Create lambda function and stack? (y/n)" 

    lambdaTemplate=".github/scripts/makeLambdaFunction.yml"

    aws cloudformation deploy --region us-west-2 --template-file $lambdaTemplate --stack-name 'tempName' --parameter-overrides LambdaName=$lambdaName --capabilities CAPABILITY_NAMED_IAM
   
    while read answer && [ "$answer" != "q" ];
      do
        if [ "$answer" == "y" ]; then
          printf '%s\n' "aws cloudformation deploy --template-file $lambdaTemplate --stack-name $stackName --parameter-overrides LambdaName=$lambdaName --capabilities CAPABILITY_NAMED_IAM"
          aws cloudformation deploy --template-file $lambdaTemplate --stack-name $stackName --parameter-overrides LambdaName=$lambdaName --capabilities CAPABILITY_NAMED_IAM
          break
        elif [ "$answer" == "n" ]; then
          break
        else
          printf "%s\n" "Create lambda? (y/n)"
        fi
      done
    printf '%s\n' "Done"  

echo "FUNCTION_NAME=$lambdaName" >> "$GITHUB_ENV"