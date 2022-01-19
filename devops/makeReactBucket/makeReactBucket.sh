# !/bin/sh

MIN=2
MAX=5
RANDOM_STRING=$(cat /dev/urandom | base64 | tr -dc 'a-z0-9' | fold -w 5 | head -n 1)
INITIALS_PROMPT="What are your initials? ('q' to quit)"
BUCKET_TEMPLATE="./makeReactBucket/makeReactBucket.json"

exitLoop=false
hasError=false

printf "%s\n" "$INITIALS_PROMPT"
printf "%s" "> "
while read initials && [ "$exitLoop" != true ] && [ "$initials" != "q" ];
  do
    if [ -z "$initials" ]; then
      printf '%s\n' "Error: Initials can't be empty" >&2
    elif [[ "${initials}" =~ [^a-zA-Z] ]]; then
      printf '%s\n' "Error: Initials must only contain letters, a-z\n" >&2
    elif [[ "${#initials}" < $MIN ]]; then
      printf '%s\n' "Error: initials must be at least $MIN characters long\n" >&2
    elif [[ "${#initials}" > $MAX ]]; then
      printf '%s\n' "Error: initials must be no more than $MAX characters long\n" >&2
    else
      break
    fi
      printf "%s\n" "$INITIALS_PROMPT"
      printf "%s" "> "
  done

formattedInitials="$(echo "${initials}" | tr -d '[:space:]' | tr '[:upper:]' '[:lower:]')"
todayDate=$(date +'%Y%m%d')

uniqueName=$formattedInitials-$RANDOM_STRING-$todayDate
bucketName=$uniqueName-bucket
stackName=$uniqueName-stack

printf "%s\n" "Your bucket and stack will be named as follows:" \
        "    - bucket: $bucketName" \
        "    - stack: $stackName\n\nCreate bucket? (y/n)"
while read answer;
  do  
    printf '%s\n' "answerrrr ${answer:0:1}" >&2

    if [ "${answer:0:1}" == "y" ]; then
      printf '%s\n' "Making..." >&2
      printf '%s\n' "aws cloudformation deploy --template-file ./makeReactBucket.json --stack-name $stackName --parameter-overrides BucketName=$bucketName" >&2
      aws cloudformation deploy --template-file $BUCKET_TEMPLATE --stack-name $stackName --parameter-overrides BucketName=$bucketName
      exit 1
    elif [ "${answer:0:1}" == "n" ]; then
      printf '%s\n' "Done" >&2
      exit 1
    fi
  done