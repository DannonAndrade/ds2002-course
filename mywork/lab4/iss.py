#!/usr/bin/env python3

import sys
import os
import json
import logging
from typing import Dict, Any

import requests
import pandas as pd

URL = "http://api.open-notify.org/iss-now.json"

formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logging.basicConfig(level=logging.INFO, handlers=[console_handler])
logger = logging.getLogger(__name__)


def parse_args() -> str:
    try:
        return sys.argv[1]
    except IndexError:
        logger.error(f"Usage: python {sys.argv[0]} <csv_file>")
        sys.exit(1)


def extract(url: str, json_file: str) -> Dict[str, Any]:
    logger.info(f"Getting data from {url}")
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        with open(json_file, "w") as fh:
            json.dump(data, fh, indent=2)
        logger.info(f"Extracted raw data and saved to {json_file}")
        return data
    except requests.exceptions.HTTPError as e:
        logger.error("HTTP error occurred: %s", e)
    except requests.exceptions.RequestException as e:
        logger.error("A request error occurred: %s", e)
    except Exception as e:
        logger.error("An unexpected error occurred: %s", e)
    return {}


def transform(record: Dict[str, Any]) -> pd.DataFrame:
    logger.info("Transforming JSON record to tabular format...")

    if not record:
        logger.error("No JSON record provided to transform")
        return pd.DataFrame()

    df = pd.json_normalize([record])
    df.columns = df.columns.str.replace("iss_position.", "")

    out = pd.DataFrame()
    out["timestamp"] = df.get("timestamp")
    try:
        out["datetime"] = pd.to_datetime(out["timestamp"], unit="s").dt.strftime("%Y-%m-%d %H:%M:%S")
    except Exception:
        out["datetime"] = ""
    out["latitude"] = df.get("latitude")
    out["longitude"] = df.get("longitude")

    logger.info(f"Transformed: {len(out)} row(s) × {len(out.columns)} column(s)")
    return out.reset_index(drop=True)


def load(df: pd.DataFrame, csv_file: str) -> None:
    if df.empty:
        logger.error("No data to load; DataFrame is empty")
        return

    exists = os.path.exists(csv_file)
    try:
        if exists:
            df.to_csv(csv_file, mode="a", header=False, index=False)
            logger.info(f"Appended {len(df)} row(s) to {csv_file}")
        else:
            parent = os.path.dirname(csv_file)
            if parent and not os.path.exists(parent):
                os.makedirs(parent, exist_ok=True)
            df.to_csv(csv_file, index=False)
            logger.info(f"Created {csv_file} with {len(df)} row(s)")
    except Exception as e:
        logger.error("Error loading data to CSV: %s", e)


def main() -> None:
    logger.info("ETL PIPELINE: ISS Tracker")

    csv_file = parse_args()
    json_file = f"{csv_file}.raw.json"

    raw = extract(URL, json_file)
    if not raw:
        logger.error("Extraction failed; exiting")
        sys.exit(1)

    df = transform(raw)
    if df.empty:
        logger.error("No transformed data; exiting")
        sys.exit(1)

    load(df, csv_file)
    logger.info(f"Processed {len(df)} record(s)")


if __name__ == "__main__":
    main()




