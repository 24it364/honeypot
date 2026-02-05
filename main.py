from fastapi import FastAPI, Header, HTTPException
from detector import detect_scam
from extractor import extract
from agent import agent_reply
import requests
import os

app = FastAPI()

# Use environment variable for API key
API_KEY = os.getenv("API_KEY", "123456")

sessions = {}

@app.get("/")
def read_root():
    return {"message": "HONEYPOT API is running!"}

@app.get("/status")
def status():
    return {"activeSessions": len(sessions)}

@app.post("/honeypot")
def honeypot(data: dict, x_api_key: str = Header(None)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")

    session = data.get("sessionId")
    text = data.get("message", {}).get("text", "")

    if not session:
        raise HTTPException(status_code=400, detail="sessionId missing")

    if session not in sessions:
        sessions[session] = {
            "messages": 0,
            "intel": {
                "upiIds": [],
                "phoneNumbers": [],
                "phishingLinks": [],
                "bankAccounts": [],
                "suspiciousKeywords": []
            }
        }

    sessions[session]["messages"] += 1

    scam = detect_scam(text)

    if scam:
        found = extract(text)
        for k in found:
            if k in sessions[session]["intel"]:
                sessions[session]["intel"][k] += found[k]

        reply = agent_reply()

        if sessions[session]["messages"] >= 5:
            send_to_guvi(session)

        return {"status": "success", "reply": reply}

    return {"status": "safe", "reply": "Okay"}

def send_to_guvi(session):
    payload = {
        "sessionId": session,
        "scamDetected": True,
        "totalMessagesExchanged": sessions[session]["messages"],
        "extractedIntelligence": sessions[session]["intel"],
        "agentNotes": "Used urgency tactics"
    }

    try:
        requests.post(
            "https://hackathon.guvi.in/api/updateHoneyPotFinalResult",
            json=payload,
            timeout=5
        )
    except requests.exceptions.RequestException as e:
        print(f"Failed to send to GUVI: {e}")
