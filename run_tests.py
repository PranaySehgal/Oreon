import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
TESTS_DIR = ROOT / "tests"


def main() -> int:
    cmd = [sys.executable, "-m", "pytest", "-q", str(TESTS_DIR)]
    print(f"Running tests from {ROOT}")
    result = subprocess.run(cmd, cwd=ROOT, check=False)
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
