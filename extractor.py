import re

def extract(text):
    return {
        "upiIds": re.findall(r"\w+@\w+", text),
        "phoneNumbers": re.findall(r"\d{10}", text),
        "bankAccounts": re.findall(r"\d{12,16}", text),
        "phishingLinks": re.findall(r"https?://\S+", text),
        "suspiciousKeywords": []
    }
