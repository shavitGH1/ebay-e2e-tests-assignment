# EBay E2E Test Framework - Ness assignment
### Author: Shavit Pollak

## Working Assumptions
* When logging in, if ebay presents the test a "Verify you are a human" page, the test will fail.
* If the account the test uses is not pre-verified, the test might fail due to ebay requiring verification.
* If the user already has something in the cart, the test might fail.
* If a window pops up asking where to send the invitation, the test might fail.

## Setup & Execution
**Prerequisites:**
* Python 3.8+
* pip (Python package manager)

# Installation:
# 1. Install dependencies
pip install playwright pytest pytest-playwright allure-pytest
# 2. Install Playwright Chromium browser


playwright install chromium

# Running the Tests:
# 1. Run tests and generate results
pytest --alluredir=allure-results
# 2. Open the visual Allure report
allure serve allure-results