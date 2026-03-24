import json
import os
from datetime import datetime

import boto3
from classifier import classify_ticket


S3_BUCKET_NAME = "s3-harshitahindonia-demobucket"


def read_ticket():
    print("Enter customer support ticket:")
    return input("> ")


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
    ticket = read_ticket()

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


if __name__ == "__main__":
    main()