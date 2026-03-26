import boto3
import argparse
import os
import logging

logging.basicConfig(level=logging.INFO)

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_folder")
    parser.add_argument("destination")
    return parser.parse_args()

def upload(input_folder, destination):
    try:
        s3 = boto3.client('s3', region_name='us-east-1')

        bucket, prefix = destination.split('/', 1)

        for file in os.listdir(input_folder):
            if file.startswith("results") and file.endswith(".csv"):
                path = os.path.join(input_folder, file)

                s3.upload_file(
                    path,
                    bucket,
                    f"{prefix}/{file}"
                )

                logging.info(f"Uploaded {file}")

    except Exception as e:
        logging.error(f"Error: {e}")

def main():
    args = parse_args()
    upload(args.input_folder, args.destination)
    logging.info("Done")

if __name__ == "__main__":
    main()
