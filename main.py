import pytest
import os
import subprocess

if __name__ == "__main__":
    allure_results_dir = "allure-results"
    
    # Ensure the allure-results directory exists and is empty
    if not os.path.exists(allure_results_dir):
        os.makedirs(allure_results_dir)
    else:
        for file in os.listdir(allure_results_dir):
            os.remove(os.path.join(allure_results_dir, file))

    # Run pytest with allure reporting
    pytest.main(["--alluredir=allure-results", "tests/test_ebay_search_and_cart.py"])

    # Try to generate and open the Allure report, but don't fail if Allure isn't installed.
    print("\nAttempting to generate and open the Allure report...")
    try:
        # This command will start a web server and open the report in a browser.
        # It will keep running until you stop it (e.g., with Ctrl+C in the terminal).
        subprocess.run(["allure", "serve", allure_results_dir], check=True)
    except (FileNotFoundError, subprocess.CalledProcessError):
        # This block runs if the 'allure' command is not found or fails.
        print("\n---")
        print("INFO: Allure command-line tool not found or failed to run.")
        print("The test results have been generated in the 'allure-results' directory.")
        print("To view the HTML report, you need to install the Allure command-line tool.")
        print("\n--- How to Install Allure on Windows ---")
        print("\nOption 1: Using Scoop (Recommended)")
        print("1. Open PowerShell.")
        print("2. Run: scoop install allure")
        print("\nOption 2: Manual Installation")
        print("1. Download the latest .zip file from: https://github.com/allure-framework/allure2/releases")
        print("2. Extract the archive to a permanent location (e.g., C:\\allure).")
        print("3. Add the 'bin' directory of the extracted folder to your system's PATH environment variable (e.g., C:\\allure\\bin).")
        print("\nAfter installation, you can view the report by running this command in your terminal:")
        print(f"allure serve {allure_results_dir}")
        print("---\n")

