"""
config.py  —  Emotiv Cortex API Configuration
==============================================
Loads credentials and runtime settings from a `.env` file in the same
directory.  Copy `.env.example` → `.env` and fill in your values before
running any example script.

Usage in example scripts
------------------------
    from config import (
        CLIENT_ID, CLIENT_SECRET,
        HEADSET_ID, DEBUG, DEBIT,
        EXPORT_FOLDER
    )
"""

import os
from pathlib import Path

# ---------------------------------------------------------------------------
# Load .env from the same directory as this file
# ---------------------------------------------------------------------------
try:
    from dotenv import load_dotenv
    _env_path = Path(__file__).resolve().parent / ".env"
    if _env_path.exists():
        load_dotenv(_env_path)
    else:
        # Silently skip if .env is absent — environment variables might be set
        # by the shell / CI pipeline instead.
        pass
except ImportError:
    # python-dotenv is optional; without it, rely on shell environment vars.
    pass

# ---------------------------------------------------------------------------
# Required credentials
# ---------------------------------------------------------------------------

CLIENT_ID: str = os.getenv("EMOTIV_CLIENT_ID", "")
"""Your Cortex App Client ID.  Register at https://emotiv.gitbook.io/cortex-api"""

CLIENT_SECRET: str = os.getenv("EMOTIV_CLIENT_SECRET", "")
"""Your Cortex App Client Secret."""

# ---------------------------------------------------------------------------
# Optional settings — all have safe defaults
# ---------------------------------------------------------------------------

HEADSET_ID: str = os.getenv("EMOTIV_HEADSET_ID", "")
"""
Target EPOC X headset ID.
Leave blank to auto-select the first available headset.
Example:  EPOCX-12345678
"""

LICENSE: str = os.getenv("EMOTIV_LICENSE", "")
"""Enterprise license key (leave blank if not required)."""

DEBIT: int = int(os.getenv("EMOTIV_DEBIT", "10"))
"""Number of sessions to debit from your plan per run."""

DEBUG: bool = os.getenv("EMOTIV_DEBUG", "false").lower() in ("1", "true", "yes")
"""Set to True for verbose WebSocket / JSON-RPC logging."""

EXPORT_FOLDER: str = os.getenv("EMOTIV_EXPORT_FOLDER", str(Path.home() / "cortex_exports"))
"""
Local folder where exported CSVs / EDF files are saved.
The folder will be created automatically if it does not exist.
"""

# ---------------------------------------------------------------------------
# Validation helper
# ---------------------------------------------------------------------------

def validate() -> None:
    """
    Raise a clear RuntimeError when mandatory credentials are missing.
    Call this at the top of each example script's ``main()`` function.

    Example::

        from config import validate
        validate()
    """
    missing = []
    if not CLIENT_ID:
        missing.append("EMOTIV_CLIENT_ID")
    if not CLIENT_SECRET:
        missing.append("EMOTIV_CLIENT_SECRET")

    if missing:
        raise RuntimeError(
            "\n"
            "═══════════════════════════════════════════════════════════════╗\n"
            "  Missing Cortex credentials!                                  \n"
            "  Please copy `.env.example` → `.env` and fill in:            \n"
            f"    {', '.join(missing)}                                       \n"
            "  See: https://emotiv.gitbook.io/cortex-api#create-a-cortex-app\n"
            "═══════════════════════════════════════════════════════════════╝\n"
        )

    # Ensure export folder exists
    Path(EXPORT_FOLDER).mkdir(parents=True, exist_ok=True)


# ---------------------------------------------------------------------------
# Quick self-test — run this file directly to verify your config is loaded
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("=== Emotiv Cortex Configuration ===")
    for key, val in [
        ("CLIENT_ID",     CLIENT_ID or "(not set)"),
        ("CLIENT_SECRET", ("*" * len(CLIENT_SECRET)) if CLIENT_SECRET else "(not set)"),
        ("HEADSET_ID",    HEADSET_ID or "(auto-detect)"),
        ("LICENSE",       LICENSE or "(none)"),
        ("DEBIT",         DEBIT),
        ("DEBUG",         DEBUG),
        ("EXPORT_FOLDER", EXPORT_FOLDER),
    ]:
        print(f"  {key:<16} : {val}")

    try:
        validate()
        print("\n✔  Configuration looks good!")
    except RuntimeError as e:
        print(e)
