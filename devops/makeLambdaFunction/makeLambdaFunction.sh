# !/bin/sh

NUM=2
RANDOM_STRING=$(cat /dev/urandom | base64 | tr -dc 'a-z0-9' | fold -w 5 | head -n 1)
INITIALS_PROMPT="Please enter your first and last initial (or 'q' to quit)"
LAMBDA_TEMPLATE="./makeLambdaFunction.yml"

while :
  do
    # get and validate user initials
    printf "%s\n" "$INITIALS_PROMPT" 
    while read initials && [ "$initials" != "q" ];
      do
        if [ -z "$initials" ]; then
          printf '%s\n' "Error: initials can't be empty" 
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

    formattedInitials="$(echo "${initials}" | tr -d '[:space:]' | tr '[:upper:]' '[:lower:]')"
    todayDate=$(date +'%Y%m%d')
    uniqueName=$formattedInitials-$RANDOM_STRING-$todayDate

    lambdaName=$uniqueName-lambda
    stackName=$uniqueName-stack

    printf "%s\n" "Your lambda function and stack will be named as follows:" \
            "    - lambda: $lambdaName" \
            "    - stack: $stackName" \
            "Create lambda function and stack? (y/n)" 
    while read answer && [ "$answer" != "q" ];
      do
        if [ "${answer:0:1}" == "y" ]; then
          printf '%s\n' "aws cloudformation deploy --template-file $LAMBDA_TEMPLATE --stack-name $stackName --parameter-overrides LambdaName=$lambdaName --capabilities CAPABILITY_NAMED_IAM"
          aws cloudformation deploy --template-file $LAMBDA_TEMPLATE --stack-name $stackName --parameter-overrides LambdaName=$lambdaName --capabilities CAPABILITY_NAMED_IAM
          break
        elif [ "${answer:0:1}" == "n" ]; then
          break
        else
          printf "%s\n" "Create lambda? (y/n)"
        fi
      done
    printf '%s\n' "Done" 
    break
  done 

