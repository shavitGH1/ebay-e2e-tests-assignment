import allure
from playwright.async_api import Page, TimeoutError  # Import TimeoutError
from pages.base_page import BasePage


class LoginPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.signin_button: str = "//a[text()='Sign in']"
        self.userid_input: str = "//input[@id='userid']"
        self.continue_button: str = "#signin-continue-btn"
        self.password_input: str = "#pass"
        self.signin_submit_button: str = "#sgnBt"
        self.skip_passkey_button: str = "#passkeys-cancel-btn"
        self.main_content: str = "#mainContent"  # A common selector for the main content area

    async def login(self, username: str, password: str) -> None:
        with allure.step(f"Logging in as {username}"):
            await self.utils.click_element(self.signin_button)

            await self.page.wait_for_selector(self.userid_input, state='visible')
            await self.utils.fill_element(self.userid_input, username)
            await self.utils.click_element(self.continue_button)

            await self.utils.fill_element(self.password_input, password)
            await self.utils.click_element(self.signin_submit_button)

            with allure.step("Check for and skip Passkey page if it appears"):
                try:
                    # Wait for the skip button for up to 5 seconds
                    await self.page.wait_for_selector(self.skip_passkey_button, state='visible', timeout=5000)
                    # If it appears, click it. Using direct click as it may not cause a full page load.
                    await self.page.click(self.skip_passkey_button)
                    await self.utils.wait_for_page_load()  # Wait for page to load after clicking skip
                except TimeoutError:
                    # If the button doesn't appear after 5 seconds, just continue.
                    allure.step("Passkey page did not appear. Continuing.")
                    pass
            
            await self.page.wait_for_selector(self.main_content, state='visible')
            await self.take_screenshot("Logged In")
