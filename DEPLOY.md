# Deploy Bill X-Ray to Render

This repository is a dependency-free static site. The authoritative publish directory is `public/`.

## Existing Render service

1. Replace the contents of the connected GitHub repository with this package and commit the change.
2. In Render, confirm **Build Command** is `echo "Bill X-Ray is a static site; no build step required."` and **Publish Directory** is `public`.
3. The existing Blueprint-managed service is `bill-xray-uapi`; `render.yaml` supplies the same settings.
4. Deploy the latest commit, then open the production URL.
5. Confirm five bill buttons appear, choose **IL SB 1570**, open **CHECK MY HOMEWORK**, and repeat a spot check on the other four bills.

Do not point an existing FastAPI/uvicorn service at this package without intentionally changing it to a Static Site.
