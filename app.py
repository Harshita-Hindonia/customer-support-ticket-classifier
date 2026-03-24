import json
import os
from datetime import datetime

import logging
logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

import boto3
from classifier import classify_ticket


S3_BUCKET_NAME = "s3-harshitahindonia-demobucket"


def read_ticket():
    with open("sample.txt", "r", encoding="utf-8") as file:
        return file.read().strip()


def save_json(data):
    os.makedirs("output", exist_ok=True)

    filename = f"ticket_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    filepath = os.path.join("output", filename)

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

    return filepath


def upload_to_s3(filepath):
    s3 = boto3.client("s3")
    key = f"tickets/{os.path.basename(filepath)}"
    s3.upload_file(filepath, S3_BUCKET_NAME, key)
    print(f"Uploaded to S3 → s3://{S3_BUCKET_NAME}/{key}")


def main():
    try:
        with open("sample.txt", "r", encoding="utf-8") as file:
            content = file.read()

        tickets = [t.strip() for t in content.split("\n\n") if t.strip()]

        print(f"Total tickets found: {len(tickets)}\n")
        logging.info(f"Total tickets: {len(tickets)}")

        for i, ticket in enumerate(tickets, start=1):
            try:
                print(f"Processing Ticket {i}...")
                logging.info(f"Processing Ticket {i}")

                result = classify_ticket(ticket)

                print(f"Category: {result['category']}")
                print(f"Priority: {result['priority']}")

                data = {
                    "ticket": ticket,
                    "category": result["category"],
                    "priority": result["priority"],
                    "timestamp": datetime.now().isoformat()
                }

                filepath = save_json(data)
                print(f"Saved locally → {filepath}")

                upload_to_s3(filepath)

                logging.info(f"Success Ticket {i}")

            except Exception as e:
                print(f"Error in Ticket {i}: {e}")
                logging.error(f"Error in Ticket {i}: {e}")

            print("-" * 40)

    except Exception as e:
        print(f"Critical Error: {e}")
        logging.critical(f"Critical Error: {e}")


if __name__ == "__main__":
    main()