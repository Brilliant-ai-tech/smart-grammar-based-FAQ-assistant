"""
main.py
-------
Command-line demo of the DeKUT SCS&IT Smart FAQ Assistant.

Usage:
    python main.py                     interactive text chat
    python main.py --voice-out         also speak each reply aloud (needs speakers)
    python main.py --query "..."       classify a single query and exit (for grading/demo)
"""
import argparse
from grammar.parser import QueryParser
from responses.response_bank import generate_response

BANNER = """
==========================================================
 DeKUT School of Computer Science & IT
 Smart Grammar-Based FAQ Assistant (COD / Dean's Office)
==========================================================
Type your question below (or 'exit' to quit).
"""


def run_single(text, speak_reply=False):
    parser = QueryParser()
    parsed = parser.parse(text)
    reply = generate_response(parsed)
    print(f"\nCategory   : {parsed.category}  (confidence={parsed.confidence})")
    print(f"Keywords   : {', '.join(parsed.matched_keywords) if parsed.matched_keywords else '-'}")
    if parsed.slots:
        print(f"Slots      : {parsed.slots}")
    print(f"Response   : {reply}\n")
    if speak_reply:
        from voice.voice_interface import speak
        try:
            speak(reply)
        except Exception as e:
            print(f"[voice output unavailable: {e}]")
    return parsed, reply


def run_interactive(speak_reply=False):
    print(BANNER)
    parser = QueryParser()
    while True:
        try:
            text = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break
        if text.lower() in {"exit", "quit"}:
            print("Goodbye!")
            break
        if not text:
            continue
        parsed = parser.parse(text)
        reply = generate_response(parsed)
        print(f"Assistant [{parsed.category}]: {reply}\n")
        if speak_reply:
            from voice.voice_interface import speak
            try:
                speak(reply)
            except Exception as e:
                print(f"[voice output unavailable: {e}]")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="DeKUT SCS&IT Smart FAQ Assistant")
    ap.add_argument("--voice-out", action="store_true", help="speak replies aloud")
    ap.add_argument("--query", type=str, default=None, help="classify a single query and exit")
    args = ap.parse_args()

    if args.query:
        run_single(args.query, speak_reply=args.voice_out)
    else:
        run_interactive(speak_reply=args.voice_out)
