# PASS 46.3 — Windows, GitHub, and Render Instructions

## Windows test commands

Open Command Prompt in the project folder, then run:

```bat
cd /d C:\PROJECTS\Bill_XRay_Next
python -m unittest tests.test_sb1570_pa1040395_current_law -v
python -m unittest discover -s tests -p "test_*.py"
python SMOKE_TEST_PASS_46_3.py
```

Or double-click:

```text
ONE_CLICK_PASS_46_3.bat
```

Every command must end successfully before GitHub staging.

## Exact GitHub commands

```bat
cd /d C:\PROJECTS\Bill_XRay_Next
git status --short
git add README.md ONE_CLICK_PASS_46_3.bat SMOKE_TEST_PASS_46_3.py PATCH_PASS_46_3_CURRENT_LAW.py PASS_46_3_CURRENT_LAW.patch docs/PASS_46_SB1570_REPORT.md docs/PASS_46_3_WINDOWS_GITHUB_RENDER.md public/app.js public/business-lens.js public/data.js public/index.html public/styles.css public/transformation-examples.js public/transformation.js sources/sb1570_public_act_receipts.json PSI_SB1570_HANDOFF/BUSINESS_DEVELOPMENT_LENS_MACHINE.json PSI_SB1570_HANDOFF/EXECUTIVE_SUMMARY_FOR_TOM.md PSI_SB1570_HANDOFF/SB1570_PLAIN_ENGLISH.md PSI_SB1570_HANDOFF/SOURCES.md PSI_SB1570_HANDOFF/START_HERE_FOR_PSI.md PSI_SB1570_HANDOFF/STATUTORY_RULES.json tests/test_sb1570_pa1040395_current_law.py
git diff --cached --check
git status --short
git commit -m "PASS 46.3 correct SB 1570 current municipal selection law"
git push origin main
```

Do not use `git add .` for this narrow pass. Review the staged list before committing.

## Render verification checklist

Render should auto-deploy the `main` branch to the existing static site.

- Confirm the deployed commit matches the new GitHub commit.
- Confirm Render reports `Live` with no build or publish error.
- Open `https://bill-xray-uapi.onrender.com/` and press `Ctrl+F5`.
- Confirm all five bill tabs remain present.
- Select **IL SB 1570**.
- Confirm **CURRENT LAW CHECKED THROUGH P.A. 104-0395** is visible.
- Open both visible source links and confirm they reach official Illinois General Assembly pages for P.A. 103-0491 and P.A. 104-0395.
- Read the selection paragraph: ordinary municipal shortlist **2–6**; a sole Phase I respondent may proceed only through municipal discretion and a best-interest finding.
- Open **CHECK MY HOMEWORK** and inspect the municipal shortlist receipt, both official source links, both limitations, and the amendment excerpt.
- Open **HOW THIS BECAME HUMAN** and confirm the SB 1570 source line names both P.A. 103-0491 and P.A. 104-0395.
- Open **ILLINOIS BUSINESS DEVELOPMENT LENS** and confirm its current-law banner, both source links, ordinary rule, single-response exception, and legally separate school pathway.
- Switch to TCJA, IRA, ACA, and CHIPS; confirm none shows the Illinois current-law banner or business-development lens.
- Confirm browser developer console shows no JavaScript errors.

Official sources:

- Foundation: https://www.ilga.gov/Legislation/PublicActs/PrinterFriendly/103-0491
- Current municipal amendment: https://www.ilga.gov/Legislation/PublicActs/PrinterFriendly/104-0395
