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