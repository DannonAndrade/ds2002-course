import boto3

def upload_file(bucket, file_name, public=False):
    s3 = boto3.client('s3', region_name='us-east-1')

    with open(file_name, 'rb') as f:
        if public:
            s3.put_object(
                Bucket=bucket,
                Key=file_name,
                Body=f,
                ACL='public-read'
            )
        else:
            s3.put_object(
                Bucket=bucket,
                Key=file_name,
                Body=f
            )

    print("Upload complete")

def presign(bucket, file_name):
    s3 = boto3.client('s3', region_name='us-east-1')

    url = s3.generate_presigned_url(
        'get_object',
        Params={'Bucket': bucket, 'Key': file_name},
        ExpiresIn=3600
    )

    print("Presigned URL:", url)

if __name__ == "__main__":
    bucket = "ds2002-ddz2pt"

    upload_file(bucket, "cloud.jpg", public=False)
    upload_file(bucket, "cloud.jpg", public=True)
    presign(bucket, "cloud.jpg")
