# EBay E2E Test Framework - Ness assignment
### Author: Shavit Pollak

## Overview
This project contains end-to-end tests for eBay, designed to verify core functionalities like searching for products, adding items to the cart, and asserting cart totals. The framework is built with Python, using `pytest` for test execution and `Playwright` for browser automation.

## Architecture and Design

This test infrastructure is built upon a robust and scalable architecture that emphasizes separation of concerns, reusability, and maintainability.

### Core Technologies
- **`pytest`**: A powerful test runner that provides fixtures, detailed reporting, and a rich ecosystem of plugins.
- **`Playwright`**: A modern browser automation library that enables reliable and fast cross-browser testing.
- **`Allure`**: A flexible and visually appealing reporting tool that provides detailed insights into test execution.

### Directory Structure
The project is organized into the following directories:
- **`tests/`**: Contains the test scripts that define the test scenarios and assertions.
- **`pages/`**: Implements the Page Object Model (POM), with each file representing a page or a significant component of the application.
- **`utils/`**: Provides utility functions, such as helper methods for common page interactions.
- **`data/`**: Stores externalized test data, such as login credentials and search queries, in a `ebay_search_and_cart.json` file.

## Data-Driven Design
The framework follows a data-driven approach, where test data is decoupled from the test logic. The `data/ebay_search_and_cart.json` file centralizes all the data needed for the tests, such as:
- Login credentials
- Search queries
- Price ranges
- Item limits

**Benefits:**
- **Easy Maintenance**: Test data can be updated without modifying the test code.
- **Scalability**: New test cases with different data can be easily added by extending the configuration file.
- **Reusability**: The same test logic can be executed with multiple datasets.

## Page Object Model (POM)
The project heavily relies on the Page Object Model (POM), a design pattern that creates an object repository for UI elements.

- **`BasePage`**: A base class (`pages/base_page.py`) that all other page objects inherit from. It contains common functionalities like navigation and taking screenshots, promoting code reuse.
- **Page-Specific Classes**: Each page in the application (e.g., `SearchPage`, `ProductPage`, `CartPage`) has its own class that encapsulates the locators and methods specific to that page.

**Benefits:**
- **Readability**: Test scripts are clean and easy to understand, as they call high-level methods on the page objects (e.g., `search_page.search_items_by_name_under_price(...)`).
- **Maintainability**: If the UI changes, only the corresponding page object needs to be updated, without touching the test scripts. This significantly reduces maintenance efforts.

## Object-Oriented Programming (OOP)
The framework is designed using OOP principles to create a well-structured and maintainable codebase.

- **Inheritance**: Page objects inherit from the `BasePage` class, promoting code reuse and a consistent structure.
- **Encapsulation**: Each page object encapsulates the data (locators) and behavior (methods) of a specific page, hiding the implementation details from the tests.
- **Abstraction**: The tests interact with the application through a high-level abstraction layer provided by the page objects, making the tests more robust and less prone to breaking due to minor UI changes.

## Scalability and Maintainability
The combination of these design principles results in a test infrastructure that is both scalable and maintainable.

- **Scalability**:
  - New tests can be added by creating new test functions in the `tests` directory.
  - Support for new pages can be added by creating new page objects in the `pages` directory.
  - The data-driven approach allows for easy scaling of test scenarios with different data inputs.

- **Maintainability**:
  - The POM makes it easy to update locators when the UI changes.
  - The separation of concerns (test logic, page interactions, and test data) makes the code easier to debug and understand.
  - `pytest` fixtures (`page_setup`) handle the setup and teardown of the browser, reducing code duplication and ensuring a clean state for each test.

## Cleanup Logic
I've added cleanup logic in order to make the test stable and better, even though I know it wasn't part of the assignment.

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
The test configuration is managed in `data/ebay_search_and_cart.json`. You can modify the following parameters:
- `username`: Your eBay login username.
- `password`: Your eBay login password.
- `search_query`: The product to search for.
- `max_price`: The maximum price for items to be added to the cart.
- `items_limit`: The maximum number of items to add to the cart.
