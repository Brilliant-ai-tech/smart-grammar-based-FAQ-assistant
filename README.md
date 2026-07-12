# DeKUT SCS&IT Smart Grammar-Based FAQ Assistant

A voice- and text-based FAQ assistant that models student queries to the
Chair of Department (COD) and Dean of the School of Computer Science & IT
using a formal Context-Free Grammar, classifies them into 13 categories,
generates simulated office responses, speaks replies aloud, and integrates
with WhatsApp.

## Project structure

```
data/queries.json            45 authentic student queries (gold-labelled)
grammar/lexicon.py           shared vocabulary -> single source of truth
grammar/cfg_grammar.py       formal NLTK CFG (27 rule lines / 40+ productions)
grammar/parser.py            grammar-driven QueryParser (classifier + slots)
responses/response_bank.py   simulated Dean/COD response templates
voice/voice_interface.py     offline TTS (pyttsx3/espeak-ng) + STT (SpeechRecognition)
whatsapp/whatsapp_bot.py     Flask + Twilio WhatsApp webhook
evaluate.py                  runs the classifier over the dataset, reports accuracy
tests/test_refactor_demo.py  left-recursion + ambiguity refactor demonstration
main.py                      CLI demo (text chat, optional spoken replies)
results/                     evaluation_results.csv, demo_response.wav
```

## Setup

```bash
pip install -r requirements.txt
# Linux TTS backend for pyttsx3:
sudo apt-get install espeak-ng
```

## Run it

```bash
# Interactive text chat
python main.py

# Single query, with the CFG classification shown
python main.py --query "When will my CAT results for Data Structures be released?"

# Same, but also speak the reply aloud
python main.py --query "..." --voice-out

# Re-run the grammar and see it formally parse all 13 category templates
python -m grammar.cfg_grammar

# Re-run the full accuracy evaluation over all 45 dataset queries
python evaluate.py

# See the left-recursion / ambiguity refactor proof
python -m tests.test_refactor_demo

# Simulate WhatsApp messages locally (no network required)
python run_whatsapp.py

# Run the real WhatsApp webhook (needs a Twilio account + ngrok, see
# whatsapp/whatsapp_bot.py header comment for the full walkthrough)
python run_whatsapp.py
```

## Connect to Twilio WhatsApp


1. Start the bot locally:
   ```bash
   python run_whatsapp.py
   ```
2. In another terminal, expose the local app with ngrok:
   ```bash
   ngrok http 5000
   ```
3. Copy the forwarding URL from ngrok and set it as the webhook for your Twilio WhatsApp sandbox or number.
   Use this path:
   ```text
   https://<your-ngrok-id>.ngrok.io/whatsapp
   ```
4. Join the Twilio WhatsApp sandbox from your phone and send a message to the sandbox number.
   The bot should reply automatically.

## Headline results (see the full project report for details)

- 45 authentic queries collected across 13 FAQ categories.
- CFG: 27 rule lines / 40+ individual productions, all 13 canonical
  category templates parse with exactly one tree each (verified, no
  ambiguity in the final grammar).
- Classifier accuracy: 84.4% before the priority-weighting refactor,
  93.3% after (42/45 correct) - see `results/evaluation_results.csv`.
- TTS pipeline verified end-to-end (`results/demo_response.wav`).
- WhatsApp webhook logic verified locally via
  `whatsapp.simulate_incoming_message()`; deployment steps for a live
  Twilio sandbox are documented in `whatsapp/whatsapp_bot.py`.
