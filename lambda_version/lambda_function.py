import json
from datetime import datetime

import boto3

s3 = boto3.client("s3")
S3_BUCKET_NAME = "s3-harshitahindonia-demobucket"


def classify_ticket(ticket_text):
    if not ticket_text or not ticket_text.strip():
        raise ValueError("Ticket text cannot be empty.")

    text = ticket_text.lower()

    category = "general"
    priority = "low"

    if any(word in text for word in ["login", "log in", "password", "signin", "sign in", "otp"]):
        category = "login"
    elif any(word in text for word in ["billing", "payment", "refund", "charged", "invoice"]):
        category = "billing"
    elif any(word in text for word in ["claim", "settlement", "reimbursement"]):
        category = "claim"
    elif any(word in text for word in ["policy", "coverage", "renewal", "document"]):
        category = "policy"

    if any(word in text for word in ["urgent", "asap", "critical", "not working", "error"]):
        priority = "high"
    elif any(word in text for word in ["today", "important", "issue", "unable"]):
        priority = "medium"

    return {
        "category": category,
        "priority": priority
    }


def upload_to_s3(data):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    key = f"tickets/lambda_ticket_{timestamp}.json"

    s3.put_object(
        Bucket=S3_BUCKET_NAME,
        Key=key,
        Body=json.dumps(data, indent=4),
        ContentType="application/json"
    )

    return f"s3://{S3_BUCKET_NAME}/{key}"


def lambda_handler(event, context):
    try:
        body = event.get("body")

        if isinstance(body, str):
            body = json.loads(body)
        elif body is None:
            body = event

        ticket = body.get("ticket", "").strip()

        if not ticket:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Ticket text is required"})
            }

        result = classify_ticket(ticket)

        output = {
            "ticket": ticket,
            "category": result["category"],
            "priority": result["priority"],
            "timestamp": datetime.now().isoformat()
        }

        s3_path = upload_to_s3(output)
        output["s3_path"] = s3_path

        return {
            "statusCode": 200,
            "body": json.dumps(output)
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }