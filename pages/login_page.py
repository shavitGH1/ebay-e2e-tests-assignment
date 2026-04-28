import allure
from playwright.async_api import Page, TimeoutError
from pages.base_page import BasePage


class LoginPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.signin_button: str = "//a[text()='Sign in']"
        self.userid_input: str = "#userid"
        self.continue_button: str = "#signin-continue-btn"
        self.password_input: str = "#pass"
        self.signin_submit_button: str = "#sgnBt"
        self.skip_passkey_button: str = "#passkeys-cancel-btn"
        self.main_content: str = "#mainContent"

    async def login(self, username: str, password: str) -> None:
        with allure.step(f"Logging in as {username}"):
            await self.utils.click_element(self.signin_button)

            await self.utils.fill_element(self.userid_input, username)
            await self.utils.click_element(self.continue_button)

            await self.utils.fill_element(self.password_input, password)
            await self.utils.click_element(self.signin_submit_button)

            with allure.step("Check for and skip Passkey page if it appears"):
                try:
                    skip_button = self.page.locator(self.skip_passkey_button)
                    await skip_button.wait_for(state='visible', timeout=5000)
                    await skip_button.click()
                    await self.page.wait_for_load_state("domcontentloaded")
                except TimeoutError:
                    allure.step("Passkey page did not appear. Continuing.")
                    pass
            
            await self.page.locator(self.main_content).wait_for(state='visible')
            await self.take_screenshot("Logged In")
