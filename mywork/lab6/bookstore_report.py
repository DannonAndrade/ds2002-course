import os
from pymongo import MongoClient


MONGODB_ATLAS_URL = os.getenv("MONGODB_ATLAS_URL")
MONGODB_ATLAS_USER = os.getenv("MONGODB_ATLAS_USER")
MONGODB_ATLAS_PWD = os.getenv("MONGODB_ATLAS_PWD")


def main():

    uri = f"mongodb+srv://{MONGODB_ATLAS_USER}:{MONGODB_ATLAS_PWD}@{MONGODB_ATLAS_URL.split('//')[1]}"

    client = MongoClient(uri)

    db = client["bookstore"]
    authors = db["authors"]

    total = authors.count_documents({})

    print("BOOKSTORE AUTHOR REPORT")
    print("----------------------")
    print(f"Total authors: {total}\n")

    for author in authors.find({}, {"_id":0,"name":1,"nationality":1}):
        print(f"{author['name']} - {author['nationality']}")

    client.close()


if __name__ == "__main__":
    main()
