import re

SCAM_KEYWORDS = [
    "account",
    "blocked",
    "verify",
    "urgent",
    "upi",
    "bank",
    "suspend",
    "limited",
    "click"
]

def detect_scam(text):
    text = text.lower()

    for word in SCAM_KEYWORDS:
        if word in text:
            return True

    return False
