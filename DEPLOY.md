# Deploy Bill X-Ray on Render

Bill X-Ray's public product is a static site in `public/`.

## Render Blueprint (recommended)

1. Push this repository to GitHub.
2. In Render, choose **New > Blueprint**.
3. Connect the GitHub repository.
4. Render will detect the root `render.yaml` file.
5. Create the Blueprint.

The Blueprint publishes `./public` as a static site. No runtime server or dependency installation is required.

## Manual Static Site alternative

If you prefer **New > Static Site** in Render:

- Build command: `echo "No build required"`
- Publish directory: `public`

## Local preview

On Windows, double-click `START_BILL_XRAY_PUBLIC.bat`.

Or open `public/index.html` directly in a browser.
