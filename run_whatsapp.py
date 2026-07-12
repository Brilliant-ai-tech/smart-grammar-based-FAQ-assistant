import runpy
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

runpy.run_path(str(ROOT_DIR / "whatsapp" / "whatsapp_bot.py"),
               run_name="__main__")
