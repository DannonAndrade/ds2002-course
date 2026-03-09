#!/usr/bin/env python3

import sys
import os
import logging
from datetime import datetime
from typing import Dict, Any

import requests
import mysql.connector

URL = "http://api.open-notify.org/iss-now.json"

MY_ID = "ddz2pt"
MY_NAME = "Dannon Andrade"

DB_HOST = os.environ.get("DBHOST")
DB_USER = os.environ.get("DBUSER")
DB_PASS = os.environ.get("DBPASS")
DB_NAME = "iss"

formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logging.basicConfig(level=logging.INFO, handlers=[console_handler])
logger = logging.getLogger(__name__)

def get_connection():
    db = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASS,
        database=DB_NAME
    )
    return db
def extract(url: str) -> Dict[str, Any]:
    logger.info(f"Getting data from {url}")
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        logger.info("Extracted data from API successfully")
        return data
    except requests.exceptions.HTTPError as e:
        logger.error("HTTP error occurred: %s", e)
    except requests.exceptions.RequestException as e:
        logger.error("A request error occurred: %s", e)
    except Exception as e:
        logger.error("An unexpected error occurred: %s", e)
    return {}


def register_reporter(table, reporter_id, reporter_name):
    db = get_connection()
    cursor = db.cursor()

    try:
        check = "SELECT reporter_id FROM " + table + " WHERE reporter_id = %s"
        cursor.execute(check, (reporter_id,))
        result = cursor.fetchone()

        if result is None:
            insert = "INSERT INTO " + table + " (reporter_id, reporter_name) VALUES (%s, %s)"
            cursor.execute(insert, (reporter_id, reporter_name))
            db.commit()
            logger.info(f"Registered new reporter: {reporter_id}")
        else:
            logger.info(f"Reporter '{reporter_id}' already registered, skipping")

    except Exception as e:
        logger.error("Error in register_reporter: %s", e)

    finally:
        cursor.close()
        db.close()


def load(data: Dict[str, Any], reporter_id: str) -> None:
    if not data:
        logger.error("No data to load")
        return

    db = get_connection()
    cursor = db.cursor()

    try:
        message   = data["message"]
        lat       = data["iss_position"]["latitude"]
        lon       = data["iss_position"]["longitude"]

        ts = datetime.utcfromtimestamp(data["timestamp"])
        timestamp_str = ts.strftime("%Y-%m-%d %H:%M:%S")

        insert = """
            INSERT INTO locations (message, latitude, longitude, timestamp, reporter_id)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(insert, (message, lat, lon, timestamp_str, reporter_id))
        db.commit()
        logger.info(f"Inserted location: lat={lat}, lon={lon} at {timestamp_str}")

    except Exception as e:
        logger.error("Error inserting into locations: %s", e)

    finally:
        cursor.close()
        db.close()


def main() -> None:
    logger.info("ETL PIPELINE: ISS Tracker")

    register_reporter("reporters", MY_ID, MY_NAME)

    raw = extract(URL)
    if not raw:
        logger.error("Extraction failed; exiting")
        sys.exit(1)

    load(raw, MY_ID)
    logger.info("Done!")


if __name__ == "__main__":
    main()