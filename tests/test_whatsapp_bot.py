import os
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class WhatsappBotStartupTests(unittest.TestCase):
    def test_whatsapp_bot_starts_without_module_not_found(self):
        env = os.environ.copy()
        env["WHATSAPP_SKIP_SERVER"] = "1"

        result = subprocess.run(
            [sys.executable, "whatsapp/whatsapp_bot.py"],
            cwd=str(ROOT),
            capture_output=True,
            text=True,
            timeout=30,
            env=env,
        )

        self.assertEqual(result.returncode, 0,
                         msg=result.stdout + result.stderr)
        self.assertIn("Local WhatsApp handler simulation", result.stdout)


if __name__ == "__main__":
    unittest.main()
