"""
whatsapp_bot.py
----------------
WhatsApp integration for the DeKUT SCS&IT FAQ assistant, built on Twilio's
WhatsApp Business API (the standard, low-friction way to prototype a
WhatsApp bot without owning a WhatsApp Business Cloud API app review).

HOW THIS PLUGS TOGETHER
------------------------
WhatsApp user --> Twilio WhatsApp number --> this Flask webhook (/whatsapp)
    --> grammar.parser.QueryParser (classifies + extracts slots)
    --> responses.response_bank.generate_response (simulated office reply)
    --> TwiML <Message> reply --> back to Twilio --> WhatsApp user

RUNNING THIS FOR REAL (steps for the project demo/viva)
--------------------------------------------------------
1. Create a free Twilio account and join the WhatsApp Sandbox
   (Console -> Messaging -> Try it out -> Send a WhatsApp message).
2. `pip install flask twilio` (already in requirements.txt).
3. Run this file:  `python whatsapp/whatsapp_bot.py`  (starts on port 5000).
4. Expose it publicly for Twilio to reach, e.g. `ngrok http 5000`.
5. In the Twilio console, set the Sandbox's "WHEN A MESSAGE COMES IN"
   webhook to `https://<ngrok-id>.ngrok.io/whatsapp`.
6. WhatsApp the Twilio sandbox number with a query, e.g. "When will my
   CAT results for Data Structures be released?" and receive the
   simulated COD/Dean office reply automatically.

This module cannot be exercised live inside this offline sandbox (no
outbound access to Twilio/WhatsApp), so `simulate_incoming_message()` at
the bottom drives the exact same webhook handler function locally to
prove the logic end-to-end without needing a network call.
"""
from responses.response_bank import generate_response
from grammar.parser import QueryParser
from twilio.twiml.messaging_response import MessagingResponse
from flask import Flask, request
import os
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))


app = Flask(__name__)
parser = QueryParser()

WELCOME_MESSAGE = (
    "Hello! You've reached the DeKUT School of Computer Science & IT FAQ "
    "Assistant. Ask me about results, attachment, registration, timetables, "
    "supervision, deferment, fees, transfers, recommendation letters, or lab "
    "issues, and I'll route you to the right guidance from the COD/Dean's office."
)


def handle_query(text):
    """Core handler shared by the Flask route and the local simulator."""
    text = (text or "").strip()
    if not text or text.lower() in {"hi", "hello", "start", "menu"}:
        return WELCOME_MESSAGE
    parsed = parser.parse(text)
    reply = generate_response(parsed)
    if parsed.category == "UNCLASSIFIED":
        return reply
    return f"[{parsed.category.replace('_', ' ').title()}]\n{reply}"


@app.route("/", methods=["GET"])
def health_check():
    return "DeKUT FAQ WhatsApp bot is running.", 200


@app.route("/whatsapp", methods=["POST"])
def whatsapp_webhook():
    incoming_msg = request.values.get("Body", "")
    reply_text = handle_query(incoming_msg)

    twiml = MessagingResponse()
    twiml.message(reply_text)
    return str(twiml)


def simulate_incoming_message(text):
    """
    Drives handle_query() exactly as the Flask route would, without
    needing a live Twilio webhook call - used for local testing/demo.
    """
    return handle_query(text)


if __name__ == "__main__":
    # Local demo (no network needed):
    demo_texts = [
        "hi",
        "Good morning, when will my CAT results for Data Structures be released?",
        "I want to apply for deferment of my studies this semester.",
    ]
    print("=== Local WhatsApp handler simulation (no network required) ===\n")
    for t in demo_texts:
        print(f"Student: {t}")
        print(f"Bot: {simulate_incoming_message(t)}\n")

    if os.environ.get("WHATSAPP_SKIP_SERVER") == "1":
        raise SystemExit(0)

    host = os.environ.get("HOST", "0.0.0.0")
    port = int(os.environ.get("PORT", "5000"))
    app.run(host=host, port=port)
