#!/bin/bash

FILE=$1
BUCKET=$2
EXPIRATION=$3

# Upload file
aws s3 cp $FILE s3://$BUCKET/

# Generate presigned URL
aws s3 presign s3://$BUCKET/$FILE --expires-in $EXPIRATION
