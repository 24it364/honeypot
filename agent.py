import random

REPLIES = [
    "Why is my account being blocked?",
    "I don’t understand, can you explain?",
    "Okay what should I do now?",
    "Is there any other option?",
    "Please help me, I’m worried.",
    "I already have UPI, what next?",
    "Can you guide me step by step?"
]

def agent_reply():
    return random.choice(REPLIES)