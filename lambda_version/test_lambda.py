from lambda_function import lambda_handler

event = {
    "body": '{"ticket": "I cannot log in to my account and this is urgent"}'
}

response = lambda_handler(event, None)
print(response)