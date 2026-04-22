# EBay E2E Test Framework - Ness assignment
### Author: Shavit Pollak

## Working Assumptions
* When logging in, if ebay presents the test a "Verify you are a human" page, the test will fail.
* If the account the test uses is not pre-verified, the test might fail due to ebay requiring verification.
* If the user already has something in the cart, the test might fail.