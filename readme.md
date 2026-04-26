# EBay E2E Test Framework - Ness assignment
### Author: Shavit Pollak

## Overview
This project contains end-to-end tests for eBay, designed to verify core functionalities like searching for products, adding items to the cart, and asserting cart totals. The framework is built with Python, using `pytest` for test execution and `Playwright` for browser automation.

## Working Assumptions
* When logging in, if ebay presents the test a "Verify you are a human" page, the test will fail.
* If the account the test uses is not pre-verified, the test might fail due to ebay requiring verification.
* If the user already has something in the cart, the test might fail.
* If a window pops up asking where to send the invitation, the test might fail.

## Getting Started

### Prerequisites
- Python 3.8+
- pip (Python package manager)

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/ebay-e2e-tests-assignment.git
cd ebay-e2e-tests-assignment
```

### 2. Set Up a Virtual Environment (Recommended)
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows, use `.venv\Scripts\activate`
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Install Playwright Browsers
This command installs the necessary browser binaries for Playwright.
```bash
playwright install
```

## Running the Tests
To execute the test suite, run `pytest` from the root of the project:
```bash
pytest
```

## Allure Reports
This project uses Allure to generate detailed test reports.

### Generating the Report
To run the tests and generate Allure report data, use the following command:
```bash
pytest --alluredir=allure-results
```

### Viewing the Report
To view the interactive Allure report, run:
```bash
allure serve allure-results
```
This will start a local web server and open the report in your default browser.

## Configuration
The test configuration is managed in `data/config.json`. You can modify the following parameters:
- `username`: Your eBay login username.
- `password`: Your eBay login password.
- `search_query`: The product to search for.
- `max_price`: The maximum price for items to be added to the cart.
- `items_limit`: The maximum number of items to add to the cart.
