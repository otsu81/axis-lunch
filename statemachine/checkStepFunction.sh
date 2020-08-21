#!/bin/bash

STEP_ARN=$(aws cloudformation describe-stacks --query 'Stacks[?StackName==`'$STACK_NAME'`].[Outputs[?OutputKey==`StatemachineArn`].OutputValue]' --output text)
echo Stepfunction ARN: $STEP_ARN

EXEC_ARN=$(aws stepfunctions start-execution --state-machine-arn $STEP_ARN --query 'executionArn' --output text)
echo Execution ARN: $EXEC_ARN

STATUS=$(aws stepfunctions describe-execution --execution-arn $EXEC_ARN --query 'status' --output text)

while [ "$STATUS" == "RUNNING" ]
do
    echo Running...
    sleep 1
    STATUS=$(aws stepfunctions describe-execution --execution-arn $EXEC_ARN --query 'status' --output text)
done

aws stepfunctions describe-execution --execution-arn $EXEC_ARN

if [ "$STATUS" != "SUCCEEDED" ]
then
    echo Step function failed to finish
    exit 1
fi