#!/bin/bash

SCRIPT_PATH=$(dirname "$0")

# import validateInitials from common.lib
# shellcheck disable=SC1091
. "$SCRIPT_PATH/../common.lib"

RANDOM_STRING=$(cat /dev/urandom | base64 | tr -dc 'a-z0-9' | fold -w 5 | head -n 1)
BUCKET_TEMPLATE="$SCRIPT_PATH/makeReactBucket.yml"
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

  if [ "$initials" == "q" ]; then
    printf '%s\n' "Done" >&1
    break
  fi

  formattedInitials="$(echo "${initials}" | tr -d '[:space:]' | tr '[:upper:]' '[:lower:]')"
  todayDate=$(date +'%Y%m%d')
  uniqueName=$formattedInitials-$RANDOM_STRING-$todayDate

  bucketName=$uniqueName-bucket
  stackName=$uniqueName-stack

  if [ "$skipPrompt" = false ]; then
    # show user name of bucket and stack, get confirmation to create resources
    printf "%s\n" "Your bucket and stack will be named as follows:" \
      "    - bucket: $bucketName" \
      "    - stack: $stackName" \
      "Create bucket and stack? (y/n)" >&1
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

  if [ "${answer:0:1}" == "y" ]; then
    printf '%s\n' "aws cloudformation deploy --region $region --template-file $BUCKET_TEMPLATE --stack-name $stackName --parameter-overrides BucketName=$bucketName" >&1
    aws cloudformation deploy --region $region --template-file "$BUCKET_TEMPLATE" --stack-name "$stackName" --parameter-overrides BucketName="$bucketName"
  fi
  printf '%s\n' "Done" >&1
  break
done
