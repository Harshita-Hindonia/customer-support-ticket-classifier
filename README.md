# Customer Support Ticket Classifier

A beginner-friendly Python + AWS project that classifies customer support tickets by category and priority, saves the output as JSON locally, and uploads the file to Amazon S3.

## Features
- Accepts customer support ticket text as input
- Classifies ticket into:
  - login
  - billing
  - claim
  - policy
  - general
- Assigns priority:
  - high
  - medium
  - low
- Saves result as JSON locally
- Uploads JSON file to Amazon S3 using boto3

## Tech Stack
- Python
- AWS S3
- boto3
- Git/GitHub

## Project Structure
```bash
customer-support-ticket-classifier/
│
├── app.py
├── classifier.py
├── requirements.txt
├── README.md
├── .gitignore
├── sample.txt
└── output/