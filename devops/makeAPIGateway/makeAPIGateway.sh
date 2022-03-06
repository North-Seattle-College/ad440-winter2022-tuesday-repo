# !/bin/sh
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


    # converts initials to lowercase and remove spaces
    formattedInitials="$(echo "${initials}" | tr -d '[:space:]' | tr '[:upper:]' '[:lower:]')"
    todayDate=$(date +'%Y%m%d')
    OPENSSL_STRING=$(openssl rand -hex 3)
    RANDOM_STRING=${OPENSSL_STRING:0:5}
    uniqueName=$formattedInitials-$RANDOM_STRING-$todayDate
    APIName=$uniqueName-api
    stackName=$uniqueName-stack

    printf "%s\n" "Your API and stack will be named as follows:" \
            "api: $lambdaName" \
            "stack: $stackName" \
            "Create API? (y/n)" 

    apiTemplate="./makeAPIGateway.yml"
    while read answer && [ "$answer" != "q" ];
      do
        if [ "$answer" == "y" ]; then
          printf '%s\n' "aws cloudformation deploy --template-file $apiTemplate --stack-name $stackName --parameter-overrrides APIName=$APIName"
          aws cloudformation deploy --template-file $apiTemplate --stack-name $stackName --parameter-overrides APIName=$APIName
          break
        elif [ "$answer" == "n" ]; then
          break
        else
          printf "%s\n" "Create API? (y/n)"
        fi
      done
    printf '%s\n' "Done" 
    break
  done 
