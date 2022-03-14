# !/bin/bash
INITIALS_PROMPT="Please enter your first and last initial (or 'q' to quit)"
NUM=2
initials=$1
    
  # converts initials to lowercase and remove spaces
  formattedInitials="$(echo "${initials}" | tr -d '[:space:]' | tr '[:upper:]' '[:lower:]')"
  todayDate=$(date +'%Y%m%d')
  OPENSSL_STRING=$(openssl rand -hex 3)
  RANDOM_STRING=${OPENSSL_STRING:0:5}
  uniqueName=$formattedInitials-$RANDOM_STRING-$todayDate
  instanceName=$uniqueName-instance
  initials="$1"
  answer=y

    printf "%s\n" "Your Sagemaker Instance:" \
            "instance: $instanceName" \
            "stack: $stackName" \
            "Create instance and stack? (y/n)" >&1

    aws sagemaker create-notebook-instance \
      --notebook-instance-name $instanceName \
      --instance-type "ml.t2.medium" \
      --role-arn "arn:aws:iam::061431082068:role/tsm-sagemaker-notebook-stack-ExecutionRole-1RUW7XNE8MJNL" \
      --default-code-repository "sagemaker-sentiment-analysis"

echo "INSTANCE_NAME=$instanceName" >> "$GITHUB_ENV"