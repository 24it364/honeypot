from fastapi import FastAPI, Header, HTTPException
from detector import detect_scam
from extractor import extract
from agent import agent_reply
import requests

app = FastAPI()

sessions = {}

@app.post("/honeypot")
def honeypot(data: dict, x_api_key: str = Header(None)):

    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")

    session_id = data["sessionId"]
    text = data["message"]["text"]

    if session_id not in sessions:
        sessions[session_id] = {
            "messages": 0,
            "intel": {
                "upiIds": [],
                "phoneNumbers": [],
                "bankAccounts": [],
                "phishingLinks": [],
                "suspiciousKeywords": []
            }
        }

    sessions[session_id]["messages"] += 1

    scam = detect_scam(text)

    if scam:
        found = extract(text)

        for k in found:
            sessions[session_id]["intel"][k] += found[k]

        reply = agent_reply()

        if sessions[session_id]["messages"] >= 5:
            send_to_guvi(session_id)

        return {
            "status": "success",
            "reply": reply
        }

    return {
        "status": "safe",
        "reply": "Okay"
    }


def send_to_guvi(session_id):

    payload = {
        "sessionId": session_id,
        "scamDetected": True,
        "totalMessagesExchanged": sessions[session_id]["messages"],
        "extractedIntelligence": sessions[session_id]["intel"],
        "agentNotes": "Scammer used urgency tactics"
    }

    try:
        requests.post(
            "https://hackathon.guvi.in/api/updateHoneyPotFinalResult",
            json=payload,
            timeout=5
        )
    except:
        pass
