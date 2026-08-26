import subprocess,sys
from pathlib import Path
root=Path(__file__).resolve().parent
cmd=[sys.executable,'-m','unittest','discover','-s','tests','-p','test_*.py']
r=subprocess.run(cmd,cwd=root)
raise SystemExit(r.returncode)
