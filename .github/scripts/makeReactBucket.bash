#!/bin/bash

function validateInitials() {
  MIN=2
  MAX=5

  initials=$1

  if [ -z "$initials" ]; then
    printf '%s\n' "Error: initials can't be empty" >&2
    return 1
  elif [[ "${initials}" =~ [^a-zA-Z] ]]; then
    printf '%s\n' "Error: initials must only contain letters, a-z" >&2
    return 1
  elif [[ "${#initials}" < $MIN ]]; then
    printf '%s\n' "Error: initials must be at least $MIN characters" >&2
    return 1
  elif [[ "${#initials}" > $MAX ]]; then
    printf '%s\n' "Error: initials must be no more than $MAX characters" >&2
    return 1
  fi
  return 0
}

function validateRegion() {
  REGIONS=("us-east-2" "us-east-1" "us-west-1" "us-west-2" "af-south-1" "ap-east-1" "ap-southeast-3" "ap-south-1" "ap-northeast-3" "ap-northeast-2" "ap-southeast-1" "ap-southeast-2" "ap-northeast-1" "ca-central-1" "cn-north-1" "cn-northwest-1" "eu-central-1" "eu-west-1" "eu-west-2" "eu-south-1" "eu-west-3" "eu-north-1" "me-south-1" "sa-east-1")
  region=$1

  if [[ " ${REGIONS[*]} " =~ ${region} ]]; then
    return 0
  fi
  printf '%s\n\n' "Error: $region is not a valid region." >&2
  printf '%s\n' "region must be one of the following: ${REGIONS[*]}" >&2
  return 1
}

OPENSSL_STRING=$(openssl rand -hex 3)
RANDOM_STRING=${OPENSSL_STRING:0:5}
BUCKET_TEMPLATE=".github/scripts/makeReactBucket.yml"
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

  if [[ "${answer:0:1}" == "y" ]]; then
    printf '%s\n' "aws cloudformation deploy --region $region --template-file $BUCKET_TEMPLATE --stack-name $stackName --parameter-overrides BucketName=$bucketName" >&1
    aws cloudformation deploy --region $region --template-file "$BUCKET_TEMPLATE" --stack-name "$stackName" --parameter-overrides BucketName="$bucketName"
  fi
  printf '%s\n' "Setting BUCKET_NAME environment variable to $bucketName" >&1
  printf '%s\n' "Done" >&1
  break
done

echo "BUCKET_NAME=$bucketName" >> "$GITHUB_ENV"
