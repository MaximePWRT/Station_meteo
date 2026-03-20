#!/usr/bin/env python3
from pathlib import Path
import subprocess
import sys


def main() -> int:
    setup_script = Path(__file__).with_name("setup_raspberry_pi.sh")
    if not setup_script.exists():
        print(f"Missing setup script: {setup_script}", file=sys.stderr)
        return 1

    result = subprocess.run(["bash", str(setup_script)])
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())