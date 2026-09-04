from pathlib import Path
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import json
import subprocess
import sys
import threading
from urllib.request import urlopen

root = Path(__file__).resolve().parent
raw = (root / "public" / "data.js").read_text(encoding="utf-8").strip()
data = json.loads(raw[len("window.BXR_DATA = "):-1])
sb = data["sb1570"]

assert len(data) == 5
assert sb["current_law_status"] == "CURRENT LAW CHECKED THROUGH P.A. 104-0395"
assert "best interest" in json.dumps(sb).lower()
assert "single-respondent option appears in the school provision" not in json.dumps(sb).lower()

for asset in ("index.html", "styles.css", "data.js", "transformation.js", "transformation-examples.js", "business-lens.js", "app.js"):
    assert (root / "public" / asset).is_file(), asset

# Serve the actual Render publish directory and request every browser asset over HTTP.
handler = partial(SimpleHTTPRequestHandler, directory=str(root / "public"))
server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
thread = threading.Thread(target=server.serve_forever, daemon=True)
thread.start()
try:
    base = f"http://127.0.0.1:{server.server_port}"
    for asset in ("index.html", "styles.css", "data.js", "transformation.js", "transformation-examples.js", "business-lens.js", "app.js"):
        with urlopen(f"{base}/{asset}", timeout=5) as response:
            body = response.read()
            assert response.status == 200 and body, asset
finally:
    server.shutdown()
    server.server_close()

result = subprocess.run(
    [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-p", "test_*.py"],
    cwd=root,
)
raise SystemExit(result.returncode)
