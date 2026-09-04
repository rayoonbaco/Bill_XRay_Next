"""Apply the narrow SB 1570 current-law correction with a timestamped backup.

Place this script and PASS_46_3_CURRENT_LAW.patch in the Bill_XRay_Next root,
then run: python PATCH_PASS_46_3_CURRENT_LAW.py
"""
from datetime import datetime
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
PATCH = ROOT / "PASS_46_3_CURRENT_LAW.patch"
MARKER = "CURRENT LAW CHECKED THROUGH P.A. 104-0395"


def main():
    if not PATCH.is_file():
        raise SystemExit(f"Missing patch file: {PATCH.name}")

    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup = ROOT.parent / f"{ROOT.name}_BACKUP_BEFORE_PASS_46_3_{stamp}"
    shutil.copytree(ROOT, backup)
    print(f"Timestamped backup created: {backup}")

    data_file = ROOT / "public" / "data.js"
    if data_file.is_file() and MARKER in data_file.read_text(encoding="utf-8"):
        print("PASS 46.3 is already applied; no project files were changed.")
        return 0

    check = subprocess.run(
        ["git", "apply", "--check", str(PATCH)], cwd=ROOT, text=True,
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT
    )
    if check.returncode:
        print(check.stdout)
        print("Patch check failed. The timestamped backup is untouched.")
        return check.returncode

    applied = subprocess.run(["git", "apply", str(PATCH)], cwd=ROOT)
    if applied.returncode:
        print("Patch application failed. Restore from the timestamped backup if needed.")
        return applied.returncode

    print("PASS 46.3 applied. Run ONE_CLICK_PASS_46_3.bat next.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
