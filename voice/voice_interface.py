"""
voice_interface.py
-------------------
Voice input/output layer for the DeKUT SCS&IT FAQ assistant.

- Text-to-Speech (TTS): pyttsx3, an OFFLINE engine (wraps espeak-ng on
  Linux, SAPI5 on Windows, NSSpeechSynthesizer on macOS). Chosen over
  cloud TTS (e.g. gTTS/Google Cloud TTS) so the assistant keeps working
  on campus with limited connectivity - a explicit requirement implied by
  "accessible via both text and voice" for a student-facing tool.
- Speech-to-Text (STT): SpeechRecognition, configurable to use the offline
  Sphinx engine or (when internet is available) the Google Web Speech API
  for higher accuracy. Optional generative-AI refinement (e.g. passing the
  raw STT transcript through an LLM to fix disfluencies) is supported via
  `refine_transcript()` and is OFF by default, per the brief's "optional"
  Generative-AI integration.

This module is written to run standalone on a student's machine with a
microphone/speakers; in this project's automated sandbox (no audio
hardware) `demo_tts_to_file()` still produces a real .wav file to prove
the pipeline works end-to-end.
"""
import os

try:
    import pyttsx3
    _PYTTSX3_AVAILABLE = True
except ImportError:
    _PYTTSX3_AVAILABLE = False

try:
    import speech_recognition as sr
    _SR_AVAILABLE = True
except ImportError:
    _SR_AVAILABLE = False


def speak(text, out_path=None, rate=165):
    """
    Convert text to speech. If out_path is given, saves audio to that file
    (works headless, no speakers needed - used for the WhatsApp voice-note
    reply feature). Otherwise plays audio immediately through speakers.
    """
    if not _PYTTSX3_AVAILABLE:
        raise RuntimeError("pyttsx3 not installed. Run: pip install pyttsx3")

    engine = pyttsx3.init(driverName="espeak")
    engine.setProperty("rate", rate)

    if out_path:
        engine.save_to_file(text, out_path)
        engine.runAndWait()
        return out_path
    else:
        engine.say(text)
        engine.runAndWait()
        return None


def listen(timeout=5, engine="google"):
    """
    Capture audio from the default microphone and transcribe it.
    engine: 'google' (needs internet, higher accuracy) or 'sphinx' (offline).
    Returns the transcribed text, or None if nothing was understood.
    NOTE: requires a real microphone; not runnable in this sandbox.
    """
    if not _SR_AVAILABLE:
        raise RuntimeError("SpeechRecognition not installed. Run: pip install SpeechRecognition")

    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source, timeout=timeout)

    try:
        if engine == "sphinx":
            return recognizer.recognize_sphinx(audio)
        return recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        return None
    except sr.RequestError as e:
        raise RuntimeError(f"STT service error: {e}")


def refine_transcript(raw_text, llm_call=None):
    """
    OPTIONAL generative-AI refinement step (per brief: "Utilize generative
    AI tools to support ... natural language refinement"). Pass any
    callable llm_call(prompt) -> str (e.g. a wrapper around Claude/GPT) to
    clean up disfluencies from raw STT output before it reaches the parser.
    If no llm_call is supplied, the raw transcript is returned unchanged so
    the pipeline degrades gracefully without an AI dependency.
    """
    if llm_call is None:
        return raw_text
    prompt = (
        "Clean up this speech-to-text transcript of a student query to the "
        "COD/Dean's office. Fix disfluencies and obvious mis-transcriptions "
        "only; do not change the meaning or add content.\n\n"
        f"Transcript: {raw_text}"
    )
    return llm_call(prompt)


def demo_tts_to_file(text, out_path="results/demo_response.wav"):
    """Utility used by tests/README to prove the TTS pipeline works."""
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    return speak(text, out_path=out_path)


if __name__ == "__main__":
    sample = ("Thank you for reaching out to the COD office. Results for Data "
               "Structures are typically released within two weeks of the exam date.")
    path = demo_tts_to_file(sample)
    print(f"TTS demo audio written to: {path}")
