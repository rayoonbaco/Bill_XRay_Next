from pathlib import Path
import json, subprocess, sys

root=Path(__file__).resolve().parent
raw=(root/'public'/'data.js').read_text(encoding='utf-8').strip()
data=json.loads(raw[len('window.BXR_DATA = '):-1])
assert len(data)==5 and 'sb1570' in data
assert len(data['sb1570']['receipts'])==13
assert 'data-bill="sb1570"' in (root/'public'/'index.html').read_text(encoding='utf-8')
result=subprocess.run([sys.executable,'-m','unittest','discover','-s','tests','-p','test_*.py'],cwd=root)
raise SystemExit(result.returncode)
